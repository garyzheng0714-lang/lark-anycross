# AnyCross Guide

让 AI 智能体照一套实测过的流程操作飞书集成平台（AnyCross）：查、搭、改工作流，配触发器、回调和单点登录，自建连接器，和多维表格搭配做自动化。附 124 个组件的离线资料库。

## 安装

**Claude Code**

```bash
claude plugin install feishu-anycross --marketplace garyzheng0714-lang/anycross-guide
```

Claude Code 2.1.275 以前的版本分两步：先 `claude plugin marketplace add garyzheng0714-lang/anycross-guide`，再 `claude plugin install feishu-anycross@anycross-guide`。

更新：`claude plugin marketplace update anycross-guide`，再 `claude plugin update feishu-anycross@anycross-guide`。

**Codex**

```bash
git clone https://github.com/garyzheng0714-lang/anycross-guide.git ~/anycross-guide
ln -s ~/anycross-guide/skills/feishu-anycross ~/.codex/skills/feishu-anycross
```

更新：`git -C ~/anycross-guide pull`。

**Claude 桌面版或网页版**

下载 [feishu-anycross.zip](https://github.com/garyzheng0714-lang/anycross-guide/releases/download/skill/feishu-anycross.zip)，在设置的技能（Skills）页面上传。

装好后直接说「帮我看看集成平台里这个工作流为什么没跑」这类话，智能体会自己用上它。

## 里面有什么

| 内容 | 入口 |
| --- | --- |
| 守则、按任务找参考、最容易栽的坑 | [SKILL.md](../skills/feishu-anycross/SKILL.md) |
| 实测经验：排错、搭建、导出、触发器、单点登录、浏览器操作、选型 | [references](../skills/feishu-anycross/references/) |
| 组件资料库：事件与动作索引、表达式、平台限制、官方来源 | [资料库](../skills/feishu-anycross/references/guide/README.md) |

每条经验标了证据等级：实测、文档、推断。

## 说明

非官方整理，和飞书没有隶属关系。平台会更新，和当前界面冲突时以界面为准。勘误见 [贡献说明](CONTRIBUTING.md)。许可证 MIT，见 [LICENSE](../LICENSE)，第三方资料的权利见 [NOTICE](../skills/feishu-anycross/references/guide/NOTICE.md)。

觉得有用，可以在 [爱发电](https://afdian.com/a/garyzheng) 请我喝杯咖啡。
