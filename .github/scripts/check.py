#!/usr/bin/env python3
"""Check what this repo is about to publish: skill frontmatter, relative links, secrets, private words.

Usage:
  python3 .github/scripts/check.py          # 检查暂存区（下一次提交的内容）
  python3 .github/scripts/check.py <rev> [<base>]   # 检查某个提交，连同 base..rev 的提交说明；pre-push 钩子用这个

只看 git 会公开的文件，不看本机私有文件。仓库根目录有 .public-denylist 时，
每行一个正则，命中即报错；这个文件本身不进 git。
"""
import json
import re
import subprocess
import sys
from pathlib import PurePosixPath
from urllib.parse import unquote

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
TEXT_SUFFIXES = {".md", ".json", ".py", ".txt", ".yml", ".yaml", ".sh", ".js", ".mjs", ".ts"}
LINK = re.compile(r"\]\(([^)\s]+)\)")
PUBLIC_IPV4 = re.compile(
    r"(?<![A-Za-z]/)\b(?!(?:10|127|0)\.)(?!192\.168\.)(?!172\.(?:1[6-9]|2\d|3[01])\.)"
    r"(?!192\.0\.2\.|198\.51\.100\.|203\.0\.113\.)(?:\d{1,3}\.){3}\d{1,3}\b"
)
SECRET_PATTERNS = {
    "anycross callback": re.compile(r"anycross/trigger/callback/[A-Za-z0-9_\-+/=]{20,}"),
    "secret assignment": re.compile(r"(?i)\b\w*(secret|password|passwd|token)\w*\s*[=:]\s*[\"']?(?![\"'<$({])[A-Za-z0-9_\-+/]{24,}"),
    "feishu token": re.compile(r"\b(t|u)-[A-Za-z0-9_\-.]{30,}"),
    "feishu app id": re.compile(r"\bcli_[a-f0-9]{16}\b"),
    "github token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}"),
    "api key": re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@(?!example\.)[A-Za-z0-9-]+\.[A-Za-z0-9.-]*[A-Za-z]\b"),
    "public ipv4": PUBLIC_IPV4,
}
IP_ALLOWED_FILES = {"platform-anycross-public-ips.md", "updates-ip.md"}
WORKFLOW_ARCHIVES = re.compile(r"^skills/[^/]+/references/workflows/(?!README\.md$)")


def git(*args, data=None):
    return subprocess.run(["git", *args], cwd=ROOT, input=data, capture_output=True, check=True).stdout


def published_files(rev):
    if rev:
        lines = git("ls-tree", "-r", rev).decode().splitlines()
        entries = [(l.split("\t", 1)[1], l.split()[2]) for l in lines]
    else:
        lines = git("ls-files", "-s").decode().splitlines()
        entries = [(l.split("\t", 1)[1], l.split()[1]) for l in lines]
    blobs = git("cat-file", "--batch", data="\n".join(sha for _, sha in entries).encode() + b"\n")
    files, pos = {}, 0
    for path, _ in entries:
        header_end = blobs.index(b"\n", pos)
        size = int(blobs[pos:header_end].split()[2])
        files[path] = blobs[header_end + 1:header_end + 1 + size]
        pos = header_end + 1 + size + 1
    return files


def load_denylist():
    try:
        lines = open(f"{ROOT}/.public-denylist", encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        return []
    return [re.compile(l) for l in lines if l.strip() and not l.startswith("#")]


def check(rev=None, base=None):
    files = published_files(rev)
    dirs = {str(p) for path in files for p in PurePosixPath(path).parents}
    denylist = load_denylist()
    errors = []
    for path, blob in files.items():
        if WORKFLOW_ARCHIVES.match(path) or path.endswith("flow.json") or PurePosixPath(path).name.startswith(".env"):
            errors.append(f"{path}: must not be published")
        if PurePosixPath(path).suffix not in TEXT_SUFFIXES:
            continue
        text = blob.decode("utf-8", errors="ignore")
        if path.endswith("/SKILL.md"):
            m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            fields = dict(l.split(":", 1) for l in (m.group(1).splitlines() if m else []) if ":" in l and not l.startswith(" "))
            if fields.get("name", "").strip() != PurePosixPath(path).parent.name:
                errors.append(f"{path}: frontmatter name must equal folder name")
            if not fields.get("description", "").strip():
                errors.append(f"{path}: missing description")
        if path.endswith(".json"):
            try:
                json.loads(text)
            except ValueError as e:
                errors.append(f"{path}: invalid JSON: {e}")
        if path.endswith(".md"):
            for target in LINK.findall(text):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue
                rel = unquote(target.split("#", 1)[0]).rstrip("/")
                resolved = str(PurePosixPath(path).parent / rel) if rel else ""
                parts = []
                for part in resolved.split("/"):
                    if part == "..":
                        parts = parts[:-1]
                    elif part not in ("", "."):
                        parts.append(part)
                resolved = "/".join(parts)
                if rel and resolved not in files and resolved not in dirs:
                    errors.append(f"{path}: broken link {target}")
        for label, pattern in SECRET_PATTERNS.items():
            if label == "public ipv4" and PurePosixPath(path).name in IP_ALLOWED_FILES:
                continue
            for m in pattern.finditer(text):
                errors.append(f"{path}: possible {label}: {m.group(0)[:60]}")
        for pattern in denylist:
            for m in pattern.finditer(text):
                errors.append(f"{path}: private word: {m.group(0)[:60]}")
    if rev and denylist:
        span = rev if not base or set(base) == {"0"} else f"{base}..{rev}"
        for entry in git("log", "--format=%h %B%x00", span).decode().split("\0"):
            for pattern in denylist:
                for m in pattern.finditer(entry):
                    errors.append(f"commit {entry.strip()[:7]} message: private word: {m.group(0)[:60]}")
    for e in errors:
        print(e)
    print(f"checked {len(files)} files ({'staged' if rev is None else rev[:12]}), "
          f"{len(denylist)} private words, {len(errors)} problems")
    return not errors


if __name__ == "__main__":
    args = sys.argv[1:] + [None, None]
    sys.exit(0 if check(args[0], args[1]) else 1)
