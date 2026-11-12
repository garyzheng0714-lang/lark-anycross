# 使用表达式 · 来源导航

[参考目录](README.md) · [白皮书](../WHITEPAPER.md)

[查看官方资料](https://anycross.feishu.cn/documentation/platform/using-expressions)

核对日期：2026-09-21。公开版保留来源入口，不包含官方文章全文或插图。相关知识见 [表达式](../guides/EXPRESSIONS.md)、[代码环境](../guides/CODE_AND_EXPORT.md)、[版本与限制](../guides/VERSIONS_AND_LIMITS.md) 和 [Computer Use](../guides/COMPUTER_USE.md)。

## 方法与调用签名

这是技术标识和调用形式索引。`toNumber` 的签名笔误已纠正；参数约束与示例请查官方来源及本项目勘误。

| 类型 | 方法／运算 | 调用形式 |
| --- | --- | --- |
| 表达式中的条件选择 | 三元运算符 (? :) | 见官方语法说明 |
| 表达式中的条件选择 | 空判断操作符 (? :) | 见官方语法说明 |
| 静态方法 | 获取当前时间戳 (currentTimestamp) | currentTimestamp() |
| 静态方法 | 获取当前日期 (now) | now(timeZone) |
| 数值 (Number) | 数值大于 (&gt;) | 见官方语法说明 |
| 数值 (Number) | 数值大于等于 (&gt;=) | 见官方语法说明 |
| 数值 (Number) | 数值小于 (&lt;) | 见官方语法说明 |
| 数值 (Number) | 数值小于等于 (&lt;=) | 见官方语法说明 |
| 数值 (Number) | 值相等 (==) | 见官方语法说明 |
| 数值 (Number) | 值不相等 (!=) | 见官方语法说明 |
| 数值 (Number) | 数值相加 (+) | 见官方语法说明 |
| 数值 (Number) | 数值相减 (-) | 见官方语法说明 |
| 数值 (Number) | 数值相乘 (*) | 见官方语法说明 |
| 数值 (Number) | 数值相除 (/) | 见官方语法说明 |
| 数值 (Number) | 数值取模 (%) | 见官方语法说明 |
| 数值 (Number) | 数值取反 (-) | 见官方语法说明 |
| 数值 (Number) | 转换为字符串 (toString) | input.toString() |
| 数值 (Number) | 绝对值 (abs) | number.abs() |
| 数值 (Number) | 四舍五入(round) | number.round(precision) |
| 数值 (Number) | 向下取整 (floor) | number.floor() |
| 数值 (Number) | 向上取整 (ceil) | number.ceil() |
| 数值 (Number) | 转换为日期 (toDate) | number.toDate(timeZone) |
| 字符串 (String) | 字符串拼接 (+) | 见官方语法说明 |
| 字符串 (String) | 值相等 (==) | 见官方语法说明 |
| 字符串 (String) | 值不相等 (!=) | 见官方语法说明 |
| 字符串 (String) | 转换为字符串 (toString) | input.toString() |
| 字符串 (String) | 包含 (contains) | string.contains(substring) |
| 字符串 (String) | 转换为数值 (toNumber) | input.toNumber() |
| 字符串 (String) | 替换 (replace) | string.replace(find, replace) |
| 字符串 (String) | 模式替换 (replaceAll) | string.replaceAll(pattern, replace) |
| 字符串 (String) | 转为大写 (toUpperCase) | string.toUpperCase() |
| 字符串 (String) | 转为小写 (toLowerCase) | string.toLowerCase() |
| 字符串 (String) | 获取长度 (length) | string.length() |
| 字符串 (String) | 获取子字符串 (substring) | string.substring(start, end) |
| 字符串 (String) | 解析为为日期 (parseDate) | string.parseDate(value) |
| 字符串 (String) | 转换日期格式 (convertDateFormat) | string.convertDateFormat(value1, value2) |
| 布尔 (Boolean) | 逻辑与 (&amp;&amp;) | 见官方语法说明 |
| 布尔 (Boolean) | 逻辑或 (&#124;&#124;) | 见官方语法说明 |
| 布尔 (Boolean) | 逻辑非 (!) | 见官方语法说明 |
| 布尔 (Boolean) | 值相等 (==) | 见官方语法说明 |
| 布尔 (Boolean) | 值不相等 (!=) | 见官方语法说明 |
| 布尔 (Boolean) | 转换为字符串 (toString) | input.toString() |
| 列表 (Array) | 值相等 (==) | 见官方语法说明 |
| 列表 (Array) | 值不相等 (!=) | 见官方语法说明 |
| 列表 (Array) | 转换为字符串 (toString) | input.toString() |
| 列表 (Array) | 获取元素个数 (size) | list.size() |
| 列表 (Array) | 获取元素 (get) | array.get(index) |
| 列表 (Array) | 字符串拼接 (concat) | array.concat() |
| 列表 (Array) | 计算平均值 (average) | array.average() |
| 列表 (Array) | 获取最大值 (max) | array.max() |
| 列表 (Array) | 获取最小值 (min) | array.min() |
| 列表 (Array) | 计算总和 (sum) | array.sum() |
| 列表 (Array) | 切割列表 (slice) | array.slice(start, end) |
| 列表 (Array) | 获取列表第一个元素 (first) | array.first() |
| 列表 (Array) | 获取列表最后一个元素 (last) | array.last() |
| 列表 (Array) | 列表分区 (partition) | array.partition(length) |
| 列表 (Array) | 列表铺平 (flat) | array.flat() |
| 列表 (Array) | 去重 (unique) | array.unique() |
| 列表 (Array) | 升序排列 (asc) | array.asc() |
| 列表 (Array) | 降序排列 (desc) | array.desc() |
| 列表 (Array) | 列表是否包含某元素(contains) | array.contains(item) |
| 列表 (Array) | 列表拼接(appendList) | array.appendList(list) |
| 列表 (Array) | 追加元素(append) | array.append(item) |
| 列表 (Array) | 过滤null(compact) | array.compact() |
| 对象 (Object) | 值相等 (==) | 见官方语法说明 |
| 对象 (Object) | 值不相等(!=) | 见官方语法说明 |
| 对象 (Object) | 转换为字符串 (toString) | input.toString() |
| 对象 (Object) | 以键取值 (get) | object.get(key) |
| 日期（Date） | 转换为字符串 (toString) | input.toString() |
| 日期（Date） | 日期格式化 (format) | date.format(value) |
| 日期（Date） | 加日期 (add) | date.add(num,unit) |
| 日期（Date） | 减日期 (subtracts) | date.subtracts(num,unit) |
| 日期（Date） | 获取毫秒时间戳 (getTimestamp) | date.getTimestamp(timeZone) |
| 日期（Date） | 获取日期的年份 (getYear) | date.getYear() |
| 日期（Date） | 获取日期的月 (getMonth) | date.getMonth() |
| 日期（Date） | 获取日期是一年中的第几天 (getDayOfYear) | date.getDayOfYear() |
| 日期（Date） | 获取日期是一个月中第几号 (getDayOfMonth) | date.getDayOfMonth() |
| 日期（Date） | 获取日期日期是周几 (getDayOfWeek) | date.getDayOfWeek() |
| 日期（Date） | 获取日期的时 (getHour) | date.getHour() |
| 日期（Date） | 获取日期的分 (getMinute) | date.getMinute() |
| 日期（Date） | 获取日期的秒 (getSecond) | date.getSecond() |
| 日期（Date） | 是否为周末 (isWeekend) | date.isWeekend() |
| 日期（Date） | 是否在两个时间之间 (isBetween) | date.isBetween(start,end) |
| 日期（Date） | 和某个时间间隔的天数 (durationDays) | date.durationDays(targetDate) |
| 日期（Date） | 和某个时间间隔的小时数 (durationHours) | date.durationHours(targetDate) |
| 日期（Date） | 和某个时间间隔的分钟数 (durationMinutes) | date.durationMinutes(targetDate) |
| 日期（Date） | 和某个时间间隔的秒数 (durationSeconds) | date.durationSeconds(targetDate) |
| 空值 (Null) | 值相等 (==) | 见官方语法说明 |
| 空值 (Null) | 值不相等 (!=) | 见官方语法说明 |
| 空值 (Null) | 转换为字符串 (toString) | input.toString() |
