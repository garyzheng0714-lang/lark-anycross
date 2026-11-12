# AnyCross Guide

飞书集成平台 AnyCross 的非官方中文操作白皮书，面向可视化工作流搭建与浏览器 Computer Use。

资料快照：2026-09-21。覆盖逻辑、助手、触发器、AI、飞书和业务连接器。本版来自只读研究，尚未逐项执行平台操作。

## 从这里开始

| 目标 | 入口 |
| --- | --- |
| 理解运行机制、数据流和组件配合 | [白皮书](WHITEPAPER.md) |
| 按组件或业务目标查找 | [分类与任务索引](INDEX.md) |
| 搜索事件、动作和版本 | [操作索引](OPERATIONS.md) |
| 查看步骤、字段摘要和来源 | [124 份组件手册](manuals/README.md) |
| 拖拽节点、引用胶囊、配置与调试 | [Computer Use 手册](guides/COMPUTER_USE.md) |
| 写表达式与字段路径 | [表达式指南](guides/EXPRESSIONS.md) · [方法签名索引](reference/platform-using-expressions.md) |
| 使用脚本、连接器映射与插件 | [代码与导出](guides/CODE_AND_EXPORT.md) |
| 动手建自建连接器、批量建操作、把 MCP 服务封装成连接器 | [自建连接器实操](guides/CONNECTOR_DEVKIT.md) |
| 组合分页、卡片、Webhook 等流程 | [搭配配方](guides/RECIPES.md) |
| 核对兼容性和容量 | [版本与限制](guides/VERSIONS_AND_LIMITS.md) |
| 查看冲突、未验证事项及资料范围 | [勘误](guides/EVIDENCE_GAPS.md) · [覆盖报告](COVERAGE.md) |
| 回到官方资料 | [来源导航](reference/README.md) |

## 怎么查

在本文件夹里搜：

```sh
rg -n '发送普通消息|创建记录|pageToken' OPERATIONS.md manuals guides
```

纯 Markdown 与 JSON，无安装依赖、服务或构建步骤。操作数据也可直接读取 [operation-index.json](sources/operation-index.json)。

公开版保留原创整理、操作名称、字段类型摘要和来源地址。官方全文、第三方图示及已登录浏览器截图不在本仓库；完整参数契约与示例通过各组件的官方链接查阅。

## 证据与使用边界

文档区分官方记载、界面观察、整理建议与待验证项。已知笔误和冲突单独列出，未验证的导出 schema、旧版本行为和字段不会被编造成确定结论。执行工作流仍需用户对目标项目及动作的有效授权。

欢迎带着组件、操作、版本和来源提交勘误，见 [贡献说明](https://github.com/garyzheng0714-lang/anycross-guide/blob/main/.github/CONTRIBUTING.md)。

## 许可证

本项目原创整理和示例采用 [MIT](../../LICENSE)。飞书、AnyCross 及第三方产品名称、接口标识和外部资料的权利归各自权利人；本项目并非官方产品或官方背书，详见 [NOTICE](NOTICE.md)。
