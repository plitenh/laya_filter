# 新闻集成 · 决策边界

批注含义：**用标记矫正正确性**（事实）并记录版面偏好。字段级 diff 见 `agent/annotate/`。

choice 选项上限 **20**。当前标签空间未被拒绝。

## 两轴

| 轴 | 字段 |
|---|---|
| 事实 fact | factual, claim_status |
| 偏好 preference | channel, publish, salience |

## 字段

| 字段 | 轴 | 原语 | 选项数 | 标签 | 状态 |
|---|---|---|---|---|---|
| factual | fact | noul | 2 | false, true | ok |
| claim_status | fact | choice | 4 | accurate, outdated, misleading, unverifiable | ok |
| channel | preference | choice | 6 | politics, business, tech, society, sports, other | ok |
| publish | preference | noul | 2 | false, true | ok |
| salience | preference | score | 3 | 0:skip or bury, 1:normal slot, 2:lead / top story | ok |

## 批注标记

- `keep`：确认模型该字段正确
- `fix`：矫正为批注值，写入金标
- `flag`：存疑，不入库
