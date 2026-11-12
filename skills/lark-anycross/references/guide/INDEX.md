# 组件与任务总索引

[白皮书](WHITEPAPER.md) · [操作索引](OPERATIONS.md) · [逐组件手册](manuals/README.md) · [覆盖与缺口](COVERAGE.md)

## 按任务查找

| 目标 | 常用组件 |
| --- | --- |
| 调试一条流程／定时执行／接收 HTTP | [手动触发器](manuals/triggers/7020663004324757532.md)、[定时任务](manuals/triggers/6991656024193138689.md)、[网址触发器](manuals/triggers/6984230219439718402.md) |
| 条件路由／逐项处理／分页 | [分支](manuals/logic/7207004557832912898.md)、[循环](manuals/logic/7207004558092976129.md)、[While 循环](manuals/logic/7207004558394916866.md)、[设置变量](manuals/helpers/7211043533062029313.md) |
| 文字、列表、对象和类型处理 | [字符串助手](manuals/helpers/7174679275541725188.md)、[列表助手](manuals/helpers/6966220108586876932.md)、[Object 助手](manuals/helpers/7177664485316935682.md)、[JSON 助手](manuals/helpers/6966220589052739585.md)、[数据转换](manuals/helpers/6966219829472657411.md) |
| 时间、随机值与加解密 | [时间和日期助手](manuals/helpers/7041870175393562625.md)、[随机数助手](manuals/helpers/7205086263668703235.md)、[加解密助手](manuals/helpers/7023188879897313308.md) |
| 文件、CSV、XML 与 HTTP 接口 | [文件助手](manuals/helpers/6985120860495429660.md)、[CSV助手](manuals/helpers/7329872248653758468.md)、[XML助手](manuals/helpers/7225949795609526274.md)、[HTTP Client](manuals/helpers/7020662045452304412.md) |
| 保存跨运行状态／复用子流程 | [数据存储](manuals/helpers/7211134173963403292.md)、[调用子流程](manuals/logic/7090593491864010754.md)、[子流程触发器](manuals/triggers/7090592763460223004.md)、[子流程响应](manuals/logic/7090592083936821276.md) |
| 组装卡片、发消息、管群 | [消息卡片助手](manuals/helpers/7203195743648284700.md)、[飞书消息](manuals/feishu/6966220145001758723.md)、[飞书群组](manuals/feishu/7437014603689050114.md)、[邮件助手](manuals/helpers/7238813954103967748.md) |
| 多维表格／云文件／电子表格 | [飞书多维表格](manuals/feishu/7021056008860499970.md)、[飞书云文档文件管理](manuals/feishu/7104160406830350337.md)、[Microsoft Excel](manuals/business/7365717587433259012.md) |
| 员工、日历、会议、审批与任务 | [飞书通讯录](manuals/feishu/6979047605984559106.md)、[飞书人事（企业版）](manuals/feishu/7044123525371658242.md)、[飞书日历](manuals/feishu/6992872018618155009.md)、[飞书视频会议](manuals/feishu/7140833841618796546.md)、[飞书审批](manuals/feishu/6980900692974125057.md)、[飞书任务](manuals/feishu/7046648901651234817.md) |
| 数据库查询及同步 | [MySQL](manuals/business/7158704055215325187.md)、[Microsoft SQL Server](manuals/business/7169502362674249732.md)、[Oracle Database](manuals/business/7169494619368488964.md)、[PostgreSQL](manuals/business/7246738374529236995.md) |
| ERP 与 CRM | [金蝶云星空](manuals/business/7189498496475086852.md)、[金蝶云星辰](manuals/business/7480086480004726812.md)、[用友 U8](manuals/business/7236713304717246492.md)、[用友 U9 Cloud](manuals/business/7474891894193963012.md)、[Salesforce](manuals/business/7143817151856623620.md)、[纷享销客](manuals/business/7142797547675844636.md) |
| 研发和监控事件 | [GitHub](manuals/business/7145026798546386948.md)、[GitLab](manuals/business/7145397718192668673.md)、[Jira Cloud](manuals/business/7145395332698914819.md)、[Jira Server](manuals/business/7171342540484984834.md)、[Jenkins](manuals/triggers/7303842867158892548.md)、[Grafana](manuals/triggers/7304198911202820099.md)、[Prometheus](manuals/triggers/7307150369699053572.md) |
| AI 跨分类入口 | [DeepSeek（火山方舟版）](manuals/ai/7468955142491963394.md)、[火山方舟大模型](manuals/ai/7346043115309957124.md)、[飞书 AI](manuals/feishu/7104162315897143298.md)、[飞书 Aily](manuals/feishu/7339802645187264515.md)、[月之暗面（Moonshot）](manuals/business/7387234086508593155.md) |

分类沿用官方目录；AI 能力不只在 AI 分类，事件也不只在触发器分类。版本是文档页快照，未标注不代表无版本。

<a id="logic"></a>

## 逻辑组件（8）

| 组件 | 文档最新版本 | 事件 | 动作／逻辑模式 |
| --- | --- | ---: | ---: |
| [分支](manuals/logic/7207004557832912898.md) | 未标注 | 0 | 2 |
| [循环](manuals/logic/7207004558092976129.md) | 未标注 | 0 | 2 |
| [While 循环](manuals/logic/7207004558394916866.md) | 未标注 | 0 | 1 |
| [延迟](manuals/logic/7017038996752613404.md) | 1.1 | 0 | 1 |
| [终止](manuals/logic/7012976537360171036.md) | 1.1 | 0 | 1 |
| [同步网址触发回调](manuals/logic/6984229898000793602.md) | 1.3 | 0 | 1 |
| [调用子流程](manuals/logic/7090593491864010754.md) | 1.1 | 0 | 2 |
| [子流程响应](manuals/logic/7090592083936821276.md) | 1.1 | 0 | 1 |

<a id="helpers"></a>

## 助手组件（18）

| 组件 | 文档最新版本 | 事件 | 动作／逻辑模式 |
| --- | --- | ---: | ---: |
| [时间和日期助手](manuals/helpers/7041870175393562625.md) | 1.8 | 0 | 9 |
| [消息卡片助手](manuals/helpers/7203195743648284700.md) | 1.2 | 0 | 2 |
| [加解密助手](manuals/helpers/7023188879897313308.md) | 1.5 | 0 | 11 |
| [字符串助手](manuals/helpers/7174679275541725188.md) | 1.2 | 0 | 20 |
| [列表助手](manuals/helpers/6966220108586876932.md) | 1.3 | 0 | 21 |
| [Object 助手](manuals/helpers/7177664485316935682.md) | 1.1 | 0 | 13 |
| [JSON 助手](manuals/helpers/6966220589052739585.md) | 1.3 | 0 | 2 |
| [文件助手](manuals/helpers/6985120860495429660.md) | 1.5 | 0 | 8 |
| [邮件助手](manuals/helpers/7238813954103967748.md) | 1.0 | 0 | 1 |
| [XML助手](manuals/helpers/7225949795609526274.md) | 1.0 | 0 | 3 |
| [CSV助手](manuals/helpers/7329872248653758468.md) | 1.0 | 0 | 3 |
| [随机数助手](manuals/helpers/7205086263668703235.md) | 1.0 | 0 | 6 |
| [逻辑助手](manuals/helpers/7182772801559117852.md) | 1.1 | 0 | 2 |
| [HTTP Client](manuals/helpers/7020662045452304412.md) | 2.2 | 0 | 5 |
| [动态脚本](manuals/helpers/6966220415769280540.md) | 2.1 | 0 | 1 |
| [设置变量](manuals/helpers/7211043533062029313.md) | 1.2 | 0 | 10 |
| [数据存储](manuals/helpers/7211134173963403292.md) | 1.1 | 0 | 12 |
| [数据转换](manuals/helpers/6966219829472657411.md) | 1.1 | 0 | 6 |

<a id="triggers"></a>

## 触发器（8）

| 组件 | 文档最新版本 | 事件 | 动作／逻辑模式 |
| --- | --- | ---: | ---: |
| [网址触发器](manuals/triggers/6984230219439718402.md) | 1.5 | 2 | 0 |
| [手动触发器](manuals/triggers/7020663004324757532.md) | 1.0 | 1 | 0 |
| [定时任务](manuals/triggers/6991656024193138689.md) | 1.5 | 5 | 0 |
| [子流程触发器](manuals/triggers/7090592763460223004.md) | 1.1 | 1 | 0 |
| [告警触发器](manuals/triggers/7066028102404554780.md) | 1.4 | 1 | 0 |
| [Prometheus](manuals/triggers/7307150369699053572.md) | 1.0 | 1 | 0 |
| [Jenkins](manuals/triggers/7303842867158892548.md) | 1.1 | 1 | 0 |
| [Grafana](manuals/triggers/7304198911202820099.md) | 1.1 | 1 | 0 |

<a id="ai"></a>

## AI（9）

| 组件 | 文档最新版本 | 事件 | 动作／逻辑模式 |
| --- | --- | ---: | ---: |
| [DeepSeek（火山方舟版）](manuals/ai/7468955142491963394.md) | 1.1 | 0 | 1 |
| [MiniMax](manuals/ai/7368373083013971971.md) | 1.2 | 0 | 14 |
| [豆包大模型（尝鲜版）](manuals/ai/7384026548515143683.md) | 1.2 | 0 | 1 |
| [火山方舟大模型](manuals/ai/7346043115309957124.md) | 1.3 | 0 | 1 |
| [扣子（Coze）](manuals/ai/7367254784327073796.md) | 1.2 | 0 | 1 |
| [通义千问](manuals/ai/7386939794292490243.md) | 1.3 | 0 | 2 |
| [通义千问（开源版）](manuals/ai/7387667245655965699.md) | 1.2 | 0 | 1 |
| [通义万相](manuals/ai/7387707175126384644.md) | 1.2 | 0 | 4 |
| [文心一言](manuals/ai/7387236685641089026.md) | 1.2 | 0 | 7 |

<a id="feishu"></a>

## 飞书连接器（18）

| 组件 | 文档最新版本 | 事件 | 动作／逻辑模式 |
| --- | --- | ---: | ---: |
| [飞书消息](manuals/feishu/6966220145001758723.md) | 2.18 | 13 | 46 |
| [飞书群组](manuals/feishu/7437014603689050114.md) | 1.3 | 0 | 43 |
| [飞书通讯录](manuals/feishu/6979047605984559106.md) | 2.12 | 13 | 69 |
| [飞书日历](manuals/feishu/6992872018618155009.md) | 1.15 | 6 | 47 |
| [飞书视频会议](manuals/feishu/7140833841618796546.md) | 1.7 | 18 | 52 |
| [飞书审批](manuals/feishu/6980900692974125057.md) | 2.14 | 12 | 34 |
| [飞书任务](manuals/feishu/7046648901651234817.md) | 1.18 | 3 | 79 |
| [飞书多维表格](manuals/feishu/7021056008860499970.md) | 2.19 | 0 | 44 |
| [飞书云文档文件管理](manuals/feishu/7104160406830350337.md) | 1.16 | 9 | 62 |
| [飞书 aPaaS](manuals/feishu/7309041693369122817.md) | 1.9 | 0 | 64 |
| [飞书 Aily](manuals/feishu/7339802645187264515.md) | 1.8 | 0 | 22 |
| [飞书人事（企业版）](manuals/feishu/7044123525371658242.md) | 1.16 | 16 | 203 |
| [飞书 AI](manuals/feishu/7104162315897143298.md) | 1.9 | 0 | 27 |
| [飞书 OKR](manuals/feishu/6998449338766622721.md) | 1.11 | 0 | 12 |
| [飞书应用信息](manuals/feishu/7143122700784058369.md) | 1.12 | 7 | 33 |
| [飞书个人设置](manuals/feishu/7182821073413586948.md) | 1.3 | 0 | 6 |
| [飞书项目](manuals/feishu/7140897584851206147.md) | 2.4 | 0 | 89 |
| [飞书绩效](manuals/feishu/7508701248502267923.md) | 1.0 | 0 | 21 |

<a id="business"></a>

## 业务连接器（63）

| 组件 | 文档最新版本 | 事件 | 动作／逻辑模式 |
| --- | --- | ---: | ---: |
| [Figma](manuals/business/7304189419610898436.md) | 1.4 | 2 | 8 |
| [FireCrawl](manuals/business/7387666044279930883.md) | 1.1 | 0 | 4 |
| [GitHub](manuals/business/7145026798546386948.md) | 1.10 | 4 | 17 |
| [GitLab](manuals/business/7145397718192668673.md) | 1.7 | 12 | 31 |
| [Jira Cloud](manuals/business/7145395332698914819.md) | 1.10 | 0 | 40 |
| [Jira Server](manuals/business/7171342540484984834.md) | 1.3 | 0 | 19 |
| [Microsoft Excel](manuals/business/7365717587433259012.md) | 1.2 | 0 | 33 |
| [Microsoft SQL Server](manuals/business/7169502362674249732.md) | 1.5 | 0 | 2 |
| [Microsoft Teams](manuals/business/7343917765155536900.md) | 1.3 | 0 | 37 |
| [Moka](manuals/business/7145059205416861699.md) | 1.9 | 0 | 11 |
| [MySQL](manuals/business/7158704055215325187.md) | 1.6 | 0 | 2 |
| [Netsuite](manuals/business/7322387847708852228.md) | 1.2 | 0 | 7 |
| [Oracle Database](manuals/business/7169494619368488964.md) | 1.4 | 0 | 2 |
| [PostgreSQL](manuals/business/7246738374529236995.md) | 1.4 | 0 | 2 |
| [RocketMQ](manuals/business/7506361381482315777.md) | 1.0 | 0 | 3 |
| [SAP OData](manuals/business/7179137268861435905.md) | 1.0 | 0 | 3 |
| [SAP RFC](manuals/business/7216234093166641156.md) | 1.0 | 0 | 2 |
| [SAP SuccessFactors](manuals/business/7293478892214419458.md) | 1.1 | 0 | 12 |
| [Salesforce](manuals/business/7143817151856623620.md) | 1.14 | 2 | 11 |
| [TAPD](manuals/business/7174982538933338114.md) | 1.7 | 10 | 39 |
| [Zabbix](manuals/business/7274932733506453507.md) | 1.3 | 1 | 1 |
| [北森组织员工](manuals/business/7119387275368103938.md) | 1.8 | 0 | 20 |
| [差旅壹号](manuals/business/7478585456216997907.md) | 1.0 | 0 | 17 |
| [禅道](manuals/business/7263013589974482948.md) | 1.2 | 0 | 12 |
| [畅捷通 T+](manuals/business/7671933009943088417.md) | 1.1 | 0 | 33 |
| [滴答清单](manuals/business/7148398266105806850.md) | 1.4 | 0 | 6 |
| [抖音](manuals/business/7174981833351151617.md) | 1.14 | 0 | 1 |
| [抖音电商](manuals/business/7144984334766784540.md) | 1.7 | 9 | 10 |
| [抖音飞鱼](manuals/business/7171049871401713668.md) | 1.4 | 0 | 3 |
| [抖音生活服务](manuals/business/7174975290601373724.md) | 1.4 | 0 | 7 |
| [e签宝](manuals/business/7171049560100421635.md) | 2.3 | 0 | 16 |
| [分贝通](manuals/business/7044785906154307612.md) | 1.4 | 0 | 8 |
| [纷享销客](manuals/business/7142797547675844636.md) | 1.8 | 4 | 25 |
| [高德地图](manuals/business/7145348891720843268.md) | 1.5 | 0 | 5 |
| [管家婆云财贸](manuals/business/7319341275810709507.md) | 1.2 | 0 | 19 |
| [合思费控](manuals/business/7000943391668240385.md) | 1.4 | 0 | 11 |
| [红瓦 BIM](manuals/business/7268213198627880963.md) | 1.1 | 2 | 10 |
| [汇联易](manuals/business/7212555788261277700.md) | 1.0 | 0 | 13 |
| [伙伴云](manuals/business/7175059818565419011.md) | 1.6 | 0 | 9 |
| [简道云](manuals/business/7170992974405353474.md) | 1.6 | 15 | 22 |
| [金蝶云星辰](manuals/business/7480086480004726812.md) | 1.1 | 0 | 64 |
| [金蝶云星空](manuals/business/7189498496475086852.md) | 1.17 | 0 | 215 |
| [巨量本地推](manuals/business/7405141274673889282.md) | 1.1 | 0 | 4 |
| [巨量千川](manuals/business/7174984716536315932.md) | 1.14 | 0 | 48 |
| [巨量星图](manuals/business/7174977912960155676.md) | 1.5 | 0 | 7 |
| [聚水潭](manuals/business/7241457682522112004.md) | 1.7 | 0 | 27 |
| [kafka](manuals/business/7494120807644299292.md) | 1.0 | 0 | 3 |
| [快递100](manuals/business/7174995310329167873.md) | 1.3 | 1 | 2 |
| [每刻](manuals/business/7145065551629385729.md) | 1.5 | 0 | 6 |
| [企查查](manuals/business/7395127184777543708.md) | 1.4 | 0 | 7 |
| [企业微信](manuals/business/7278886741396783107.md) | 1.9 | 2 | 114 |
| [天眼查](manuals/business/7398060493959495684.md) | 1.1 | 0 | 6 |
| [同程商旅](manuals/business/7328326782552997891.md) | 1.2 | 0 | 7 |
| [旺店通旗舰版](manuals/business/7242575222021160963.md) | 1.10 | 0 | 16 |
| [旺店通企业版](manuals/business/7294245207649058844.md) | 1.3 | 0 | 11 |
| [西门子 Teamcenter](manuals/business/7250386746410598404.md) | 1.2 | 0 | 9 |
| [薪人薪事](manuals/business/6985356262837878788.md) | 1.11 | 9 | 24 |
| [炎黄 BPM（AWS PaaS）](manuals/business/7143499728880173057.md) | 1.5 | 0 | 4 |
| [用友 U8](manuals/business/7236713304717246492.md) | 1.1 | 2 | 4 |
| [用友 U8 Cloud](manuals/business/7262619997644947460.md) | 1.5 | 0 | 6 |
| [用友 U9 Cloud](manuals/business/7474891894193963012.md) | 0.1 | 0 | 24 |
| [月之暗面（Moonshot）](manuals/business/7387234086508593155.md) | 1.2 | 0 | 9 |
| [云学堂](manuals/business/7174985628592177180.md) | 1.6 | 0 | 6 |
