# 代码环境、自建连接器与导出结构

## 1. 先确定代码放在哪里

| 环境 | 入口／语法 | 用途 | 不能直接混用的内容 |
|---|---|---|---|
| 节点入参表达式 | 胶囊、`subject.method()` | 简单取值和计算 | JavaScript 数组、箭头函数、`require` |
| 动态脚本 | `function handler(input)` | 同步数据计算，结果包装到 `result` | HTTP／RPC、异步网络访问、Workflow Skill 入口 |
| Workflow Skill 代码节点 | 文档示例为 `module.exports = async function main(arg1)` 或 Python `main` | 对特定渠道上下文进行处理 | 不能据此给普通动态脚本添加 Node.js 或 Python 能力 |
| 自建连接器 API 映射 | `{{input.name}}`、`{{body.code}}` 等 | 把表单和响应映射到接口配置 | 普通工作流表达式的胶囊表示法 |
| 自建认证请求前插件 | `handler(req, ctx)` | 认证参数、令牌与签名处理 | 普通动态脚本的 `input/result` 约定 |
| 自建认证响应后插件 | `handler(resp)` | 解析或转换认证响应 | 直接将 `resp.body` 当对象 |
| 工作流导出文件 | 本次未取得实际文件 | 保存编排、配置及资源引用 | 不能当成内置组件实现源码 |

## 2. 动态脚本

官方最新公开版本：2.1。组件支持 ES2020；页面开头的 ES6 描述是较宽泛说明。运行是同步的，执行时间限制为 1 秒；入参与出参之和不建议超过 4 MB；系统时间为 UTC；不支持 HTTP、RPC 等 IO。

配置流程：选择“执行 JavaScript 代码” → 定义 `Input` → 通过上游胶囊映射所需字段 → 写 `function handler(input)` → 下游引用该节点的 `result`。

### 2.1 最小结构

```javascript
function handler(input) {
  return input;
}
```

若 `handler` 返回 `{"count": 3}`，官方约定节点输出为 `{"result": {"count": 3}}`。后续引用应从 `result` 继续取值，不能把函数返回值直接当成节点输出的根对象。

### 2.2 把 CSV 行映射成对象

入参由两个字段组成：`headers` 为列名列表，`rows` 为二维字符串数组。下例是本手册编写的示例，未在平台运行；处理的数据量仍应符合脚本限时和容量限制。

```javascript
function handler(input) {
  const headers = input.headers;
  return input.rows.map(function (row) {
    const record = Object.create(null);
    headers.forEach(function (name, index) {
      record[name] = index < row.length ? row[index] : null;
    });
    return record;
  });
}
```

例如 `headers=["商品","数量"]`、`rows=[["牛奶","3"]]`，函数预期返回 `[{"商品":"牛奶","数量":"3"}]`。数量仍是字符串；需要数值时另行明确转换。表头重复会覆盖同名属性，因此业务输入应先保证列名唯一。CSV 官方例子使用 `new Map()` 后按普通对象赋值，容易混淆 Map 与对象，本手册使用普通可序列化键值对象。

### 2.3 按映射表转换列表

```javascript
function handler(input) {
  return input.list.map(function (key) {
    return Object.prototype.hasOwnProperty.call(input.mapping, key)
      ? input.mapping[key]
      : null;
  });
}
```

入参契约是 `list` 与 `mapping`，缺失映射在本例中返回 null；这是一项明确的示例选择，不能自动用于所有业务。若缺失必须失败，应显式报错。

### 2.4 标准正则捕获

```javascript
function handler(input) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(input);
  if (!match) return null;
  return { year: match[1], month: match[2], day: match[3] };
}
```

这是格式拆分，不是日历合法性校验。版本 2.0 及以后应使用标准正则返回值，不能依赖 `RegExp.$1` 至 `$9`。官方替代示例中的 `cont` 是拼写错误，不可原样复制。

### 2.5 内置能力

版本 2.0 及以后公开支持 `atob`、`btoa`、`TextEncoder`、`TextDecoder`、`URL`、`URLSearchParams` 和 `anycross.CryptoJS`。不应因名称与浏览器 API 相同就假定整个浏览器或 Node.js 环境可用。

```javascript
function handler(input) {
  return anycross.CryptoJS.SHA256(input).toString();
}
```

这个示例展示访问入口。真实协议涉及 HMAC、编码、密钥、IV 和填充方式时，应逐项与对端规范匹配。官方说明脚本助手不支持真随机数生成，依赖随机数的参数需由调用方提供；不能自行假定具备 `crypto.randomBytes`。

标准 Web API 的方向是：`TextEncoder` 把字符串编码为字节，`TextDecoder` 把字节解码为字符串。官方动态脚本页面的两句解释方向写反，见勘误。

### 2.6 版本兼容

| 版本范围 | 官方记录 | 对迁移的影响 |
|---|---|---|
| ≤1.2 | 旧输入表单以 name/value 列表表现，FAQ 展示了转换为对象的本地调试方法 | 不直接把旧日志外壳当作新版 `input` |
| >1.2 | FAQ 说明可以直接复制对象输入 | 仍以实际节点 Input 为准 |
| ≤1.5 | 仅执行 handler 内函数，多个同级函数不能正确执行 | 不能直接导入依赖外部同级函数的示例 |
| ≥2.0 | 以 handler 为入口，支持同级函数；新增常用库；限制非标准 RegExp 写法 | 升级前保留原脚本和输入，升级后核对表单与输出 |
| 2.1 | 当前公开最新版本标识 | 未找到完整逐修订变更表，不推测 2.1 的所有差异 |

本地 JavaScript 调试只能验证普通逻辑，不能证明平台限时、内置库、输入绑定或版本兼容已通过。

## 3. 自建连接器的构成

实际动手时的界面流程、背后的接口、表单定义写法和批量建操作的办法，见 [自建连接器实操](CONNECTOR_DEVKIT.md)（2026-11-11 实测）。

官方开发流程包括：选择／创建服务 → 设置图标、名称、标识符与说明 → 设置 Base URL → 建立操作分组 → 用请求／响应样例创建操作 → 调整表单 → 配置 API 映射、认证和成功判断 → 发布版本。

| 部分 | 需要理解的内容 |
|---|---|
| 基本信息 | 展示名称、说明、支持的认证方式 |
| 入参表单 | 顺序、显示名、类型、控件与校验 |
| 出参结构 | 返回层级、字段显示名，决定胶囊选择器能提供什么 |
| API 配置 | 方法、URL、Path、Query、Header、Body 及映射 |
| 认证 | 表单输入、认证步骤、认证数据、令牌添加或签名 |
| 状态码 | HTTP 层和业务层的成功／失败判断 |
| 动态下拉 | 使用 API 结果提供可选项，不等于存储固定枚举 |
| 版本 | 新版本与修订版的发布约束 |

表单新增或重命名字段后，API 映射需同步调整。右侧模拟器展示的是表单效果，不等于已成功调用真实接口。

### 3.1 API 映射语法

```text
{{input.name}}
{{input.objectName.fieldName}}
{{body.code}}
{{body.msg}}
{{ input.room_ids | toMultiParams() }}
```

最后一个写法是官方用于 `room_ids=aaa&room_ids=bbb` 这类重复 Query 参数的规则。它属于连接器映射模板，不属于普通节点表达式函数。

### 3.2 成功判断

飞书 API 示例同时要求 HTTP 状态码处于 200–299 且业务 `code=0`。应用状态码路径可配置为 `{{body.code}}`，错误描述为 `{{body.msg}}`。操作级状态码规则优先，未匹配再判断连接器级规则，最后应用默认策略。

### 3.3 请求前插件

```javascript
function handler(req, ctx) {
  if (!req.headers) req.headers = {};
  req.headers.Authorization = 'Bearer ' + ctx.authData.accessToken;
  return req;
}
```

这是官方同类示例的简化展示，不包含真实凭证。`req` 可包含 `url`、`method`、`headers`、`queryParams`、`bodyType`、`body`；`ctx` 内容依执行阶段不同，认证流程可访问 `authInput`、`authData`，添加令牌／加签场景还包含操作 `input`。

### 3.4 响应后插件

```javascript
function handler(resp) {
  const body = JSON.parse(resp.body);
  body.status = 'ok';
  resp.body = JSON.stringify(body);
  return resp;
}
```

此例仅说明序列化机制，不建议在实际业务中无条件把失败改成成功。官方定义 `resp.body` 为字符串；还包含 `headers`、`statusCode`、`appStatusCode`。完整上下文、文件 API 和类型定义见 [插件能力参考](../reference/platform-plugin_introduction.md)。

## 4. Workflow Skill 与 Channel Context

Channel Context 文档描述的是 Workflow Skill 发布到 LarkBot、MyAI 等渠道后提供的聊天上下文。LarkBot 样例包含 `chat_id`、`chat_type`、`message_id` 和 `sender_id`，其中 `sender_id` 为 open_id；内容随渠道不同。

该页面给出的 JS 示例入口是 `module.exports = async function main(arg1)`，另有 Python `main` 示例。**这不是普通业务集成动态脚本的入口。**本次研究使用的空项目并未验证 Workflow Skill 功能可用性，不能据此把 Python、axios 或 Node.js 模块引入普通动态脚本。

## 5. 工作流导出、复制和模板

### 已有证据

- 项目管理文档确认支持在项目中导入工作流；创建副本时可选择复制到其他项目，不支持直接转移某个工作流。
- 实测（2026-11-11）：界面菜单只有「移动到文件夹」（本项目内）和「创建副本」；跨项目副本的网址触发器回调地址是新的。见 [盘点和整理项目](COMPUTER_USE.md#12-盘点和整理项目)。
- 更新简报确认“生成模板”能力，以及跨工作流、项目、浏览器页面复制粘贴节点，并自动调整被粘贴节点之间的引用关系。
- 这些记录不等于已经掌握导出文件格式。本次未从空项目取得导出物，也未导出其他项目。

### 取得真实导出后应查看什么

1. 文件类型、格式版本与导出时间。
2. 节点实例 ID、连接器 ID、操作 ID 及组件版本。
3. 触发器、顺序边、分支条件、循环体和子流程调用。
4. 常量与表达式绑定，尤其是跨节点引用。
5. 凭证引用、项目配置、数据集合、卡片模板、文件和业务资源依赖。
6. 错误处理与重试设置，以及发布状态是否包含在文件中。
7. 导入后是否重新分配 ID、丢失凭证或改变引用，需通过专属项目的实际导入行为确认。

以上是审阅维度，不是平台 JSON schema。本手册不提供虚构的可导入 JSON，不声称导出会包含内置实现源码、凭证明文或全部外部资源。

来源：[动态脚本](../manuals/helpers/6966220415769280540.md)、[脚本调试 FAQ](../reference/faq-Use_JavaScript_in_AnyCross.md)、[开发连接器操作](../reference/platform-develop-connector-actions.md)、[自定义认证](../reference/platform-develop_authentication.md)、[插件能力](../reference/platform-plugin_introduction.md)、[项目管理](../reference/platform-project-management.md)、[更新简报](../reference/updates-release-notes.md)。
