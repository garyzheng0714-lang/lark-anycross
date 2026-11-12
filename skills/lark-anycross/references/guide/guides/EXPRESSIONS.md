# 表达式语法与引用规范

平台表达式用于计算节点入参，**不是 JavaScript**。以下代码块标为 `text` 的内容是表达式；`〈节点胶囊〉` 是说明性占位，实际应通过 `$` 或 snake 连线插入。

方法与调用签名索引收录在 [表达式方法参考](../reference/platform-using-expressions.md)，完整参数和示例请通过该页的官方来源链接查阅。本章整理高频使用方法，未在平台执行表达式测试。

## 1. 类型与字面量

| 类型 | 写法 | 注意 |
|---|---|---|
| number | `123`、`3.14`、`1.66e10` | 数值比较与字符串比较不同 |
| string | `"hello"` | 字符串拼接的两侧必须是字符串 |
| boolean | `true`、`false` | `"true"` 是字符串 |
| array | `{1, 2, 3}`，空列表 `{}` | 不能照搬 JavaScript 的数组字面量 |
| object | `{"name": "张三"}`，空对象 `{:}` | 可以用胶囊作为键或值 |
| null | `null` | 与未输入、空串、空列表分别处理 |
| date | 通过 `now`、`toDate`、`parseDate` 等产生 | 官方类型表与后续日期章节表述不一致；不要手写假想日期字面量 |

## 2. 三种入参方式

常量用于固定值；胶囊用于数据引用；表达式用于对常量或引用做计算。需要对象的字段不要传一个看起来像 JSON 的字符串；需要 JSON 文本的字段则不能直接假定对象会被自动序列化。

```text
"订单：" + (123).toString()
{1, 2, 3}.size()
{"status": "ready"}.get("status")
```

上例是根据官方语法整理的组合示例，不是运行记录。

## 3. 胶囊与取值

输入 `$` 唤起选择器，选择来源节点和字段。方法调用采用 `subject.method(...)`；在值后输入 `.` 可查看可用方法。静态方法不需要主体，如 `currentTimestamp()`。

```text
〈节点胶囊〉.data.items
〈节点胶囊〉.data.items[0]
〈节点胶囊〉.data.items[0].fields["文档标题"]
〈节点胶囊〉.data.items[0].fields["文档标题"][0].text
〈节点胶囊〉.list[0]["age.a"]
```

`"age.a"` 是一个完整键名，不能写成 `.age.a`。下标从 0 开始；不要在空列表上直接取第 0 项。返回字段不在选择器中时，以实际返回结构继续取值；不能凭界面上未列出字段就判断接口没有返回该字段。

最新运行变量用 `variable.变量名`，如 `variable.hasMore`。项目配置通过选择器引用，配置标识以当前项目为准；本手册不编造其内部序列化路径。

## 4. 条件、比较和空值

```text
true ? "通过" : "拒绝"
null ?: "Unknown"
"a" ?: "Unknown"
```

三元运算符的条件必须为 boolean，不能套用 JavaScript 的 truthy 规则。官方对 `?:` 的说明是 **null 时使用默认值**，不能据此断言空字符串、0 或 false 也会被替换。

常见运算符为 `==`、`!=`、`>`、`>=`、`<`、`<=`、算术运算及逻辑运算；以编辑器类型提示为准。数组和对象的相等比较为深比较，数组顺序影响相等结果。字符串和数字混用可能直接出现类型错误。

可选嵌套字段需要逐层处理缺失。资料没有证明 JavaScript 的 `?.`、`??`、箭头函数和模板字符串可直接使用，因此不将它们作为平台表达式范式。

## 5. 数值、字符串与列表方法

| 类型 | 常用方法 | 用途 |
|---|---|---|
| Number | `toString`、`abs`、`round`、`floor`、`ceil`、`toDate` | 转换、取整、时间戳转日期 |
| String | `contains`、`replace`、`replaceAll`、`toUpperCase`、`toLowerCase` | 包含、替换、大小写 |
| String | `length()`、`substring`、`toNumber`、`parseDate`、`convertDateFormat` | 长度、截取、解析与格式转换 |
| Array | `size()`、`get`、`first`、`last` | 元素数和位置访问 |
| Array | `concat`、`average`、`max`、`min`、`sum` | 字符串拼接和数字聚合 |
| Array | `slice`、`partition`、`flat`、`unique`、`asc`、`desc` | 切割、分区、铺平、去重及排序 |
| Array | `contains`、`appendList`、`append`、`compact` | 包含、拼接、追加与过滤 null |
| Object | `get`、`toString` | 按键取值和字符串化 |

不要把 JavaScript 的 `join`、`map`、`filter`、`sort` 函数名直接搬到表达式中。需要按属性筛选或复杂变换时，先查列表助手；确需自定义计算时，再使用动态脚本。

```text
"hello".contains("lo")
"hello".replace("llo", "LLO")
"hello".length()
"hello".substring(1, 1)
"1.5".toNumber()
{1, 2, 3}.sum()
```

`substring` 的区间行为、列表 `slice`／`partition` 的参数含义见完整函数参考，不能因为名称接近就假定与某个语言库完全相同。`toNumber` 官方调用规则误写为 `toInteger()`，本手册采用其标题和示例一致的 `toNumber()`，实际输入仍应查看编辑器提示。

## 6. 时间与日期

```text
currentTimestamp()
now("Asia/Shanghai")
currentTimestamp().toDate("Asia/Shanghai")
now("Asia/Shanghai").format("yyyy-MM-dd HH:mm:ss")
```

`currentTimestamp()` 返回毫秒时间戳。明确区分秒与毫秒，避免多乘或少乘 1,000。`now` 产生 date 值；格式化产生 string。时区使用 IANA 名称，如 `Asia/Shanghai`、`Asia/Singapore`。

| 格式符 | 含义 |
|---|---|
| `yyyy` / `yy` | 四位／两位年份 |
| `MM` / `M` | 月份 |
| `dd` / `d` | 日期 |
| `HH` / `H` | 24 小时制小时 |
| `hh` / `h` | 12 小时制小时 |
| `mm` / `m` | 分钟 |
| `ss` / `s` | 秒 |
| `SSS` | 毫秒 |

大小写有含义，尤其是月 `MM` 和分 `mm`。其它时区格式符见完整参考。

日期方法还包括 `add`、`subtracts`、`getTimestamp`、`getYear`、`getMonth`、`getDayOfYear`、`getDayOfMonth`、`getDayOfWeek`、`getHour`、`getMinute`、`getSecond`、`isWeekend`、`isBetween` 以及 `durationDays/Hours/Minutes/Seconds`。

`parseDate` 的调用规则和示例对时区参数的展示不一致，`durationDays` 的两个相同示例给出相反结果。遇到日期差正负、边界是否包含、月份／星期起始值等问题，查原始描述后仍有冲突的，不把推断写入生产逻辑。

## 7. 推荐书写规范

1. 一个入参表达式只承担必要转换，长逻辑拆到可观察的处理节点。
2. 对 ID 保持字符串，不因全部由数字组成就转数值。
3. 拼接文本显式转换类型，日期显式指定格式和时区。
4. 把对象、数组、JSON 文本分别处理；来源字段变更后重查路径。
5. 循环条件引用最新变量；循环项引用当前 `item`。
6. 记录表达式对应的节点、操作和版本；不要只存一段脱离上下文的表达式。

## 8. 常见错误定位

| 症状 | 优先检查 |
|---|---|
| 表达式类型报错 | 字符串与数字混用；条件不是 boolean；方法与主体类型不匹配 |
| 取到 null | 字段路径、节点是否执行、数据是否缺失、列表下标 |
| 分页一直重复 | 引用了旧设置变量节点出参；没有更新游标 |
| 中文字段读不到 | 是否使用 `["字段名"]`；实际返回是否为数组 |
| 时间偏移或数量级错误 | 时区与秒／毫秒单位 |
| JSON Parse 报错 | 入参已是对象，或字符串并非合法 JSON |
| 复制后引用异常 | 是否复制了胶囊绑定，节点 ID 是否仍对应新流程 |

相关：[代码环境](CODE_AND_EXPORT.md)、[流程配方](RECIPES.md)、[勘误](EVIDENCE_GAPS.md)。
