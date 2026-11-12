#!/usr/bin/env python3
"""把集成平台导出的工作流（.zip 或里面的 flow.json）读成大纲：步骤顺序、分支条件、
每步的参数和表达式、出参样例、谁用了谁的输出、要留意的地方。

写死的长串和敏感值只显示长度和 sha256 前 8 位，输出可以贴进聊天，也能拿改前改后两份导出直接比：
    python3 -I read-export.py 改前.zip            # 大纲
    python3 -I read-export.py 改前.zip 改后.zip   # 只看差异
"""
import difflib
import hashlib
import json
import re
import sys
import zipfile

TOKEN = re.compile(r"[A-Za-z0-9_+=]{16,}")
SENSITIVE_KEY = re.compile(r"(?i)secret|password|passwd|token|appcode|api_?key|cookie|signature|webhook")
SAFE_HEADERS = {"content-type", "accept", "accept-encoding", "user-agent"}
REF = re.compile(r"\$\.([\w-]+)((?:\.[\w-]+)*)")
LITERAL = re.compile(r'"((?:[^"\\]|\\.)*)"')
ERROR_ACTIONS = {"ignore": "出错忽略、接着往下", "retry": "出错重试"}


def fingerprint(s):
    return f"<隐藏 {len(s)} 字 #{hashlib.sha256(s.encode()).hexdigest()[:8]}>"


def plain(p):
    """参数都包成 {"type": ..., "value": ...}，剥到里面的值。"""
    while isinstance(p, dict) and "type" in p and set(p) <= {"type", "value"}:
        p = p.get("value")
    return p


def fields(schema, depth=0):
    out = []
    for k, v in ((schema or {}).get("properties") or {}).items():
        if v.get("properties") and depth < 3 and k != "headers":
            out.append(f"{k}{{{fields(v, depth + 1)}}}")
        else:
            out.append(k)
    return ", ".join(out)


class Outline:
    def __init__(self, flow):
        self.flow = flow
        self.steps = {s["id"]: s for s in flow.get("steps") or []}
        self.lines = []
        self.secrets = []  # 写死了长串或敏感值的位置
        self.reads = {}  # 步骤 ID -> 它读了哪些上游字段

    def text(self, s, where, sensitive=False):
        if sensitive:
            self.secrets.append(where)
            return fingerprint(s)
        if s.startswith(("http://", "https://")) and "?" in s:
            s = s.split("?", 1)[0] + "?…"
        masked = TOKEN.sub(lambda m: fingerprint(m.group(0)), s)
        if masked != s:
            self.secrets.append(where)
        return masked

    def expr(self, e, where, sid):
        for m in REF.finditer(e):
            self.reads.setdefault(sid, set()).add(m.group(1) + m.group(2))
        return "= " + LITERAL.sub(lambda m: m.group(0) if m.group(1).startswith("$.") else f'"{self.text(m.group(1), where)}"', e)

    def value(self, p, where, sid, sensitive=False):
        while isinstance(p, dict) and "type" in p and set(p) <= {"type", "value"}:
            if p["type"] == "spel":
                return self.expr((p.get("value") or {}).get("expression", ""), where, sid)
            p = p.get("value")
        if isinstance(p, dict):
            if set(p) == {"key", "value"}:  # 请求头、查询参数这类键值对
                name = self.value(p["key"], where, sid)
                hide = sensitive or name.lower() not in SAFE_HEADERS
                return f"{name}: {self.value(p['value'], f'{where}.{name}', sid, hide)}"
            return "{" + ", ".join(f"{k}: {self.value(v, f'{where}.{k}', sid, sensitive or bool(SENSITIVE_KEY.search(k)))}" for k, v in p.items()) + "}"
        if isinstance(p, list):
            return "[" + ", ".join(self.value(v, where, sid, sensitive) for v in p) + "]"
        if isinstance(p, str):
            return self.text(p, where, sensitive)
        return json.dumps(p, ensure_ascii=False)

    def head(self, s):
        op = s.get("operation") or {}
        bits = [s.get("name") or "（没起名）", s["id"], f"{op.get('connectorName', '?')} {op.get('connectorVersion', '')}".strip()]
        action = ((s.get("errorHandler") or {}).get("defaultStrategy") or {}).get("action")
        if action and action != "terminate":
            bits.append(ERROR_ACTIONS.get(action, f"出错时 {action}"))
        return " · ".join(bits)

    def condition(self, branch, child_id):
        b = plain(plain((branch.get("parameters") or {}).get("branches") or {}).get(child_id))
        if b is None:
            return "其余情况（默认路径）"
        joiner = f" {plain(b.get('operator')) or 'and'} "
        conds = []
        for c in plain(b.get("conditions")) or []:
            comp = plain(c.get("comparison")) or {}
            parts = [self.value(comp.get("left"), branch["id"], branch["id"]), str(plain(c.get("operator")))]
            if "right" in comp:
                parts.append(self.value(comp["right"], branch["id"], branch["id"]))
            conds.append(" ".join(parts))
        return f"「{plain(b.get('label')) or '没起名'}」：{joiner.join(conds)}"

    def params(self, s, pad):
        sid = s["id"]
        for k, v in (s.get("parameters") or {}).items():
            self.lines.append(f"{pad}{k}: {self.value(v, f'{sid}.{k}', sid, bool(SENSITIVE_KEY.search(k)))}")
        try:
            schema = json.loads(s.get("dynamicSchema") or "{}").get("manualOutputSchema")
        except ValueError:
            schema = None
        if schema:
            self.lines.append(f"{pad}出参样例：{fields(schema)}")

    def walk(self, nodes, depth, parent=None):
        pad = "  " * depth
        for n in nodes:
            s = self.steps.get(n["id"], {"id": n["id"]})
            if n["type"].endswith("_child"):
                is_branch = parent and parent.get("type", "").startswith("branch")
                self.lines.append(f"{pad}- 路径{self.condition(parent, n['id'])}" if is_branch else f"{pad}- （{n['type']}）")
            else:
                self.lines.append(f"{pad}- {self.head(s)}")
                if not s.get("type", "").startswith("branch"):
                    self.params(s, pad + "    ")
            self.walk(n.get("subSteps") or [], depth + 1, s)

    def build(self):
        f = self.flow
        self.lines += [f"{f.get('name')}（flowID {f.get('flowID')}，导出格式 {f.get('version')}）", ""]
        self.walk(f.get("structure") or [], 0)
        used_by = {}
        for reader, paths in self.reads.items():
            for p in paths:
                src = p.split(".", 1)[0]
                if src != reader:
                    used_by.setdefault(src, set()).add(reader)
        if used_by:
            self.lines += ["", "谁用了谁的输出（删改一步之前先看这里）："]
            self.lines += [f"  {src} ← {', '.join(sorted(used_by[src]))}" for src in sorted(used_by)]
        notes = []
        if self.secrets:
            notes.append("写死的长串或敏感值（已隐藏）：" + ", ".join(dict.fromkeys(self.secrets)))
        for sid, s in self.steps.items():
            action = ((s.get("errorHandler") or {}).get("defaultStrategy") or {}).get("action")
            if action == "ignore" and used_by.get(sid):
                notes.append(f"{sid} 出错会被忽略，但 {', '.join(sorted(used_by[sid]))} 用到了它的输出")
            if not s.get("name") and not s.get("type", "").endswith("_child"):
                notes.append(f"{sid} 没起显示名称")
        if notes:
            self.lines += ["", "要留意："] + [f"  - {n}" for n in notes]
        return self.lines


def load(path):
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            name = next((n for n in z.namelist() if n.endswith("flow.json")), None)
            if name is None:
                sys.exit(f"{path} 里没有 flow.json")
            return json.loads(z.read(name))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main(paths):
    if len(paths) not in (1, 2):
        sys.exit(__doc__)
    outlines = [Outline(load(p)).build() for p in paths]
    if len(outlines) == 1:
        print("\n".join(outlines[0]))
    else:
        print("\n".join(difflib.unified_diff(*outlines, *paths, lineterm="", n=2)) or "两份导出没有差别")


if __name__ == "__main__":
    main(sys.argv[1:])
