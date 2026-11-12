# 查看、盘点与排错

全程只读。看完写一份诚实的记录文档，每条结论标实测、代码或推断，之后有新发现就回写这份文档。

## ID 和地址的样子

- 项目、工作流、版本、连接器 ID 都是 19 位数字。凭证 ID 是 13 位字母数字。
- 工作流页：`https://anycross.feishu.cn/console/integration/<项目ID>/workflow/<工作流ID>`
- 运行日志：`https://anycross.feishu.cn/console/integration/log`
- 凭证：`https://anycross.feishu.cn/console/integration/credential`（`/console/credential` 会 404，从左侧导航进最稳）
- 自建连接器：`https://anycross.feishu.cn/console/devkit/connector-v2/<连接器ID>/detail`
- 回调地址：`https://open.feishu.cn/anycross/trigger/callback/<一串 base64 样字符>`。这就是密钥。
- 步骤 ID 形如 `webhook-trigger-1`、`http-client-3`、`bitable-2`、`script-1`、`loop-3`、`branch-1`。表达式要引用这个 ID，不是显示名称。

## 页面自己的只读接口

官方没有导出和管理的 API，界面上能在工作流页手动导出单条，见 [导出与读懂](export.md)。已登录的控制台页面自己调用一组 `/webapi/*` 接口，能读出完整定义。在 `anycross.feishu.cn` 的页面里执行 `fetch(url, {credentials: 'include'})` 就能用页面的登录状态。只用读接口：GET，加上查日志、列项目、读项目配置这几个只读的 POST。这些是内部接口，随时可能变。（实测，2026-10）

| 用途 | 接口 | 要点 |
|---|---|---|
| 项目内文件树 | `GET /webapi/projects/<项目ID>/files` | 递归 `childResourceNodes`。`type===2` 是工作流，`resourceID` 是工作流 ID |
| 工作流草稿 | `GET /webapi/v2/flows/<工作流ID>` | `data.draft.definition` 是 JSON 字符串，要再 parse 一次。里面有 `steps[]`（id、type、operation、name、auth、parameters）。另有 `isPublished`、`isEnabled`、`latestVersion.id` |
| 已发布版本 | `GET /webapi/flows/<工作流ID>/versions/<版本ID>` | 返回 `flowDefinition` 和 `referencedVariables`（对象，多数是 `{}`，不是数组）。写成 `/v2/.../versions` 会 404 |
| 运行日志 | `POST /webapi/flow_log/search_flow_log` | 见下一节 |
| 项目配置 | `POST /webapi/project/variable`，体 `{projectID}`，带 `x-csrf-token` | `data.variableNames` 是配置名。`variableGroups[].variables` 是 JSON 字符串，含值，别输出。流程里引用写成 `$.config.<配置名>`（实测，2026-11） |
| 凭证列表 | `GET /webapi/connection_profiles` | `data.connProfiles`，有 `generation`（g1 旧版、g2 新版）、`authType`、`owner`。凭证不分项目，列表和详情都没有项目字段（实测，2026-11） |
| 凭证详情 | 新版 `GET /webapi/v2/connections/<凭证ID>?stage=draft`，旧版 `GET /webapi/connections/<凭证ID>` | 含密钥副本，只看长度或指纹 |

列全部项目有接口：`POST /webapi/project/detail/batch`，带 `x-csrf-token`，请求体 `{param: "", filterQuery: {projectType: "normal", ignoreQueryDesc: true}, pageQuery: {page, pageSize: 40}, sortType: 1}`，`tenantId` 可以不带，别人分享来的项目（`role: fullEdit`）也在里面。（实测，2026-11）另一个办法是打开编辑页的项目切换下拉，从 React 组件数据（fiber 的 `memoizedProps`）里读，这里能看到 `role`。从全量日志反推只能拿到跑过的项目。（实测）

想知道页面调了什么接口，先调用一次抓网络请求的工具，再在界面上点一下。抓包从第一次调用时才开始。（实测）

## 查运行日志

请求体字段：`timeRange{left,right}`（毫秒）、`projectList`、`flowList`、`status`、`pageSize`、`page`、`asc`、`debug:false`。请求头只要 `content-type: application/json`。（实测）

- `projectList` 必须是二维数组 `[["<项目ID>"]]`。写成一维会报 `cannot unmarshal string into []string`。查多个项目，全放进同一个内层数组 `[["<项目1>","<项目2>"]]`；写成 `[["<项目1>"],["<项目2>"]]` 返回 0 条。不带 `projectList` 返回「参数无效」。（实测，2026-11-12）
- 算全租户同时在跑几个：拉一段时间所有项目的运行记录，按 `startAt`、`endAt` 排成进出事件扫一遍，同时在跑的最大数就是峰值。突然冒出几万次运行的流程，也是这样一眼看出来的。（实测，2026-11-12）
- `count` 最多 10000，超过时 `tooMany=true`，按时间段或项目拆开查。
- 每条有 `flowName`、`flowDisabled`、`projectName`、`status`、`statusCode`、`cost`、`errorCnt`。
- 日志实际留约 32 天，文档写 30 天。「监控」页（`/webapi/dashboard/runStates`）也一样，查 40～400 天前整个租户全是 0。所以 32 天以前的最后运行时间哪里都查不到，只能写「无」，再附草稿 `updatedAt`（最后修改）估计闲置多久。（实测，2026-11）
- 找死流程：按流程汇总 32 天内的运行和失败次数。启用中但 0 次运行的，就是候选。
- 按单条流程查：`flowList: [["<工作流ID>"]]`、`pageSize: 1`，取 `count`。没有记录时返回 `code 15100002 未查询到数据`，按 0 次算。（实测，2026-11）
- 只查失败：`status: [["failed"]]`，也是二维数组。写成一维、字符串或数字都返回 `15000000 服务内部错误`。（实测，2026-11）
- 看一次运行里每个节点的入参出参：`POST /webapi/flow_log/search_node_log`，体 `{flowInstanceID, pageSize: 100, page}`，返回 `nodeLogList[]`（`nodeID`、`input`、`output`、`cost`）。能数出每次实际写了几行。点「调试」跑出来的运行，查运行日志和节点日志都要带 `debug: true`，否则查不到。（实测，2026-11-12）
- 把一条流程的运行按日期、耗时排一排，能看出藏着的外部定时调用（例：每周六 03:00 起连跑 356 次、每次约 1 分钟）。翻页超过总数会返回重复记录，按 `flowInstanceID` 去重。（实测，2026-11-12）
- 每条运行记录里：`flowInstanceID`（拿它查节点日志）、`flowID`、`flowName`、`status`、`startAt`（毫秒；草稿的 `updatedAt` 却是秒）、`errorCnt`（被「忽略」接住的错误也算进去）。按名字筛流程时用全名精确比，别用「包含」：名字里带「全量」的流程可能好几条。（实测，2026-11-12）
- 改写同步流程前，先用老流程的节点日志验新写法：取老流程最近几次成功运行，把循环节点收到的原始记录喂给新写法的转换代码，算出的每个字段和老「新增/更新记录」节点输出里表中实际存下的值逐个比。订单流程 6 次运行 263 行，0 处不同。没日志可比的表，至少把字段取法和老节点的表达式逐条对一遍。（实测，2026-11-12）
- 判断一条流程有没有被人改过，看 `updatedAt` 和 `latestVersion.id`，别对 `draft.definition` 求哈希：同一份草稿每次读出来，键的顺序可能不一样。（实测，2026-11-12）
- `pageSize` 最大 100，填 200 返回 `10000006 参数无效`。`asc: true` 也照样新的在前，自己按 `startAt` 排。（实测，2026-11-12）
- 查定时有没有漏跑：按流程把开始时间排好，相邻间隔超过中位数 1.5 倍的就是漏跑或停跑。再按天比一下这条流程和整个租户的次数：租户有日志、它是 0，就是真没跑。定时停跑没有失败记录，只能这样查。（实测，2026-11-12）

## 盘点整个租户

全部只读，229 条约几分钟。（实测，2026-11）

1. 项目列表：打开项目切换下拉，从 fiber 的 `memoizedProps` 里找同时带 `projectType` 和 `role` 的数组（数组可能嵌在 props 的对象里，要往下找两三层）。`role` 是 `fullEdit` 的项目不是自己的，删不了。单个项目的名称、描述、图标用 `POST /webapi/project/<项目ID>`（体 `{}`，带 `x-csrf-token`）读 `data.project`。
2. 每个项目读文件树，`type===2` 是工作流，其余有名字的节点是文件夹。
3. 每条读 `/webapi/v2/flows/<工作流ID>`：`isPublished`、`isEnabled`，`steps[].operation` 是对象 `{connectorId, operationId}`。网址触发器的 `hook.hookKey` 为空，回调地址不在定义里，要看触发器的「设置」页。
4. 每条按上一节查 32 天运行和失败次数。
5. 子流程依赖：「调用子流程」步骤（ID 前缀 `subflow-caller`）的 `parameters.sub_flow_id.value` 是被调流程 ID。告警流程（`alert_trigger`）的 `parameters.alertRules` 里有它盯着的流程 ID。（实测，2026-11）
6. 步骤类型看步骤 ID 去掉末尾数字：触发器有 `webhook-trigger`、`cronjob_trigger`、`manual-trigger`、`subflow-trigger`、`alert_trigger`、`approval`、`work_wechat`；`storage` 是数据存储。（实测，2026-11）
7. 比草稿和线上：两边 `steps` 按 `id` 排序，`operation` 只留 `connectorId`、`operationId`，转成键名排序的 JSON 再比。（实测，2026-11，235 条里 14 条不一样）

## 排错先问这几件事

1. **请求真的进来了吗？** 异步触发器收到就回 200，要看日志里有没有这次运行。（实测）
2. **调用方在白名单里吗？** 白名单外返回 403（`code: 7`）。换参数没用。（实测）
3. **走的是哪条分支？** 分支条件要照真实写法拼请求，见 [触发器与回调](triggers-and-callbacks.md#分支条件)。
4. **下游真的成功了吗？** 步骤标成功，对方可能返回「服务已下线」。要看返回内容。曾有一条分支的下游从半年前就下线了，平台一直显示成功。（实测）
5. **下游的证书过期了吗？** HTTP 步骤报「TLS/SSL 连接失败：x509: certificate has expired」时，是被调用那台服务器的证书过期了，集成平台这边改不了。本机用 `openssl s_client -connect <域名>:443 -servername <域名> | openssl x509 -noout -enddate` 看到期日，再对照最后一次成功的时间。第三方服务只能等对方续证书，或者换掉它。曾有人事证明生成靠第三方，对方证书过期三周没人发现。（实测，2026-11）
6. **平台是不是卡住了？** 偶尔会一步一直不返回，后面的步骤不触发，只能手动终止。重要流程要有定时对账兜底。（实测）
7. **事件被别人收走了吗？** 同一飞书应用的事件只交给一个接收方。（文档加推断）
8. **逻辑是不是分散在几处？** 集成平台、多维表格自动化、服务端代码常常串成一条链。先画出整条链，再跨三套日志查。（实测）

## 扫明文密钥和依赖

- 全量扫：所有项目的草稿和已发布版本，再加凭证。只扫一部分会漏，曾经从「1 处」扫成「3 处」。（实测）
- 最常见的写法：HTTP 节点里先用 `app_id` 加 `app_secret` 换 `tenant_access_token`，再调开放平台。能看这条流程的人都能拿到密钥，日志里可能也有。只有轮换密钥能让旧值作废。（实测）
- 查「谁在用这个飞书应用的密钥」时，必须单独扫集成平台的凭证和流程。只查服务器和代码仓库会漏。一个应用可能对应好几个凭证，新版旧版都有。（实测）
- 飞书应用加了 IP 白名单，会挡住跑在飞书机器上的东西，包括集成平台和多维表格插件。加白名单和换密钥一样可能弄断流程。（文档加推断）
- 多维表格授权码（`pt-` 开头）是某个人在某张表上的个人钥匙，谁拿到都能以这个人的名义读写整张表。修改记录里显示的是授权码主人的名字，分不出是本人改的还是外部服务改的。读取不留任何记录，管理后台的「成员行为审计」要另外付费。修改记录也只能查到几个月前，2026-11 查时最早只到 2026-05。（实测，2026-11）
- 撤授权码：打开那张表，依次点「插件」「自定义插件」「获取授权码」，取消勾选「启用授权码」，再点「确定」。只有授权码主人本人能关。验证方法：用旧码调 `https://base-api.feishu.cn/open-apis/bitable/v1/apps/<表ID>/tables`，返回 `code 1011 personal token is invalid` 才算撤掉。表的主人是别人时，AI 去点会被安全检查拦下，要用户本人点。（实测，2026-11）

## 输出时别泄露

- JS 输出不要带 auth、token、secret、cookie 这类字段名，也不要带查询串。浏览器扩展会把整段输出换成 `[BLOCKED: ...]`。给字段换短名，只输出长度或 sha256 前 8 位。
- 网址先打码再输出。打码正则要覆盖嵌套 JSON 里的网址。
- 凭证接口会返回负责人的名字、头像和 ID，过滤掉 owner、creator、avatar 字段。
- 外部接口 401 时可能把请求里的 token 原样回显。验证时只看 HTTP 状态码和 code。
