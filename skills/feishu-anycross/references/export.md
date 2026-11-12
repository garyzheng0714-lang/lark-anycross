# 导出与读懂工作流

改一条已有的工作流之前，先在界面上把它导出来。导出的 zip 既是备份，也是读懂整条流程最快的办法，不用一个个节点点开看。（实测，2026-10）

资料库里「没取得过导出文件、结构未知」的说法已经过时，以本页为准。

## 怎么导出

1. 打开工作流页，右上角「…」→「导出」。这一步只是下载，不改流程，不用先问用户。
2. 弹窗显示工作流名称和一份连接器列表，点「导出」。列表不全：一条 6 个步骤的流程，弹窗只列了 2 个。以 zip 里的为准。（实测）
3. 浏览器把 `<工作流名称>.zip` 下到「下载」文件夹。

## 放哪

导出文件里有明文密钥：网址触发器的回调地址、HTTP 节点请求头里写死的 Authorization，都原样在里面。（实测）把这个 zip 当密钥对待：只放本机私有目录，不进 Git，不上传，不发群。

统一放在 `~/.anycross-backups/<工作流名称>/<导出时间>.zip`，目录 700、文件 600。同一条流程改几次就留几份，回头能对出每次改了什么。

```sh
B=~/.anycross-backups/<工作流名>
mkdir -p -m 700 ~/.anycross-backups "$B"
mv ~/Downloads/<工作流名>.zip "$B/$(date +%Y%m%d-%H%M).zip"
chmod 600 "$B"/*.zip
```

## 读懂它

用技能自带的 [scripts/read-export.py](../scripts/read-export.py) 读成大纲。不要直接 cat 或解压后整份读，原文里的密钥会进聊天记录。

```sh
python3 -I <技能目录>/scripts/read-export.py ~/.anycross-backups/<工作流名>/20261030-0756.zip
```

大纲里有：步骤的先后和嵌套、每条分支路径的条件、每步的参数和表达式、出参字段样例、谁用了谁的输出，最后列出要留意的地方（写死的密钥在哪、出错被忽略但下游还在用的步骤、没起名的步骤）。长串和密钥只显示长度和 sha256 前 8 位，所以值变了也看得出来。

改完再导出一份，两份一起给脚本，只输出差异：

```sh
python3 -I <技能目录>/scripts/read-export.py 改前.zip 改后.zip
```

## 导出文件长什么样

zip 里只有一个 `flow.json`。（实测，导出格式 `2.0`）

| 字段 | 内容 |
|---|---|
| `name`、`flowID` | 工作流名称和 ID。没看到项目 ID、线上版本号和工作流描述 |
| `version` | 导出格式版本，见过 `2.0` |
| `structure` | 步骤的先后和嵌套，每项只有 `id`、`type`、`subSteps`。顺序只在这里看得出来 |
| `steps` | 每个步骤的完整配置，平铺一列，靠 `id` 和 `structure` 对上 |

`steps[]` 每项：

- `operation`：`connectorName`（如 `http-client`）和 `connectorVersion`。这里的 `connectorId` 和资料库手册的文件名不是同一个 ID，查手册按组件名在 [INDEX.md](guide/INDEX.md) 里找。见过的对应：`webhook-trigger` 网址触发器，`await-webhook-trigger` 同步网址触发回调，`http-client` HTTP Client，`datetime-helper` 时间和日期助手，`terminate` 终止，`branch` 分支。
- `name`、`description`：显示名称和描述。
- `parameters`：每个参数都包成 `{"type": ..., "value": ...}`。`type` 是 `spel` 时是表达式，原文在 `value.expression`，如 `_("$.webhook-trigger-1.body")`。
- `dynamicSchema`：JSON 字符串，要再 parse 一次。里面的 `manualOutputSchema` 是出参字段样例，看得出上游实际传了哪些字段。字段上的 `format`（比如把单号标成 `utc-millisec`）是平台自己猜的，不用管。
- `errorHandler.defaultStrategy.action`：`terminate` 出错就停，`ignore` 出错忽略、接着往下。
- `auth`：`key`、`parameters`、`credentials`。

分支：

- 父步骤 `type` 是 `branch_exclusive_parent`（互斥分支），每条路径是一个 `branch_exclusive_child`，路径里的步骤在它的 `subSteps` 里。
- 条件写在父步骤的 `parameters.branches.value.<路径ID>` 里：`label` 是路径名称，`operator` 是 and 或 or，`conditions[]` 每条有 `comparison.left`、`comparison.right`（判空这类没有）和 `operator`（如 `notPresent`）。
- 默认路径的 ID 是 `<分支ID>.default`，没有条件，也没有名称字段。

## 还没验证的

- 导出的是草稿还是线上版本。两者不一致时结果会不同。核对办法：用 [只读接口](inspect-and-debug.md#页面自己的只读接口) 分别读草稿和线上版本，和 `flow.json` 的 `steps` 比。验证过就把结论写回这里。
- 用了凭证、项目变量、数据存储的流程，导出里怎么表示，会不会带出明文。目前见过的流程没用凭证，`auth` 里全是空的。
- 导出的 zip 能不能原样导入回去。

## 别把旧导出当成现状

导出只代表导出那一刻，之后可能有人在界面上改过。每次动手前重新导出一份，和上一份比一下。

改过的工作流在 [workflows/](workflows/README.md) 里留一份档案：它做什么、谁调它、每步做什么、密钥在哪（只写位置）、改之前要知道的坑、怎么验证。档案按导出整理，和新导出对不上时以新导出为准，改完回写档案。
