# 客服决策批阅讲义

根据已收集的 Laya 样本整理。先读规则与例题，再答 `exam.jsonl`。

## 总规则

1. 只根据给定原文判断，不要脑补。
2. choice 只能选标签空间内的一项；score 选 0/1/2；noul 答 true/false。
3. 与 Laya 不一致时，以讲义规则为准；你的答案会覆盖模型。

## department（choice）

题干：Which department should handle this request?

选项：
- `billing` invoices, payments, refunds
- `technical` bugs, outages, system errors
- `sales` pricing, new contracts
- `other` everything else

### 标准例

- **m1-0104**

  主题: technical request 104
  正文: checkout has been returning HTTP 500 for 10 minutes. Customers cannot complete checkout. Page on-call.

  标准答案：`technical`（Laya=technical, conf=0.480）

- **m1-0217**

  主题: sales request 217
  正文: Please send enterprise pricing for 50 seats of SSO. We have not purchased yet.

  标准答案：`sales`（Laya=sales, conf=0.619）

### 易错例

- **m1-0326**（Laya 答错）

  主题: technical request 326
  正文: Login is down for the whole starter workspace. If this is not fixed today we will move off the platform.

  标准答案：`technical`；Laya：`billing`（conf=0.016）

- **m1-0060**（Laya 答错）

  主题: other request 60
  正文: Please update the billing contact email for account 1059 to ops-1059@example.com. Not a refund request.

  标准答案：`other`；Laya：`billing`（conf=0.215）

## urgency（score）

题干：How urgent is this request?

选项：
- `0` not urgent
- `1` soon
- `2` critical deadline or blocking issue

### 标准例

- **m1-0011**

  主题: billing request 11
  正文: Invoice 1010 was charged twice on Friday. Refund the duplicate today or we cancel the enterprise plan.

  标准答案：`2`（Laya=2, conf=0.207）

- **m1-0171**

  主题: billing request 171
  正文: Invoice 1170 was charged twice on Thursday. Refund the duplicate today or we cancel the growth plan.

  标准答案：`2`（Laya=2, conf=0.243）

### 易错例

- **m1-0131**（Laya 答错）

  主题: billing request 131
  正文: Invoice 1130 was charged twice on Monday. Refund the duplicate today or we cancel the enterprise plan.

  标准答案：`2`；Laya：`1`（conf=0.117）

- **m1-0360**（Laya 低置信度）

  主题: other request 360
  正文: Please update the billing contact email for account 1359 to ops-1359@example.com. Not a refund request.

  标准答案：`1`；Laya：`1`（conf=0.029）

## churn_risk（noul）

题干：Does the user threaten to cancel or leave?

选项：
- `false` 否
- `true` 是

### 标准例

- **m1-0117**

  主题: sales request 117
  正文: Please send enterprise pricing for 200 seats of checkout. We have not purchased yet.

  标准答案：`false`（Laya=false, conf=0.221）

- **m1-0145**

  主题: technical request 145
  正文: The checkout webhook has been timing out since Friday. No double charge, we only need the bug fixed.

  标准答案：`false`（Laya=false, conf=0.382）

### 易错例

- **m1-0336**（Laya 低置信度）

  主题: technical request 336
  正文: Login is down for the whole growth workspace. If this is not fixed today we will move off the platform.

  标准答案：`true`；Laya：`true`（conf=0.023）

- **m1-0362**（Laya 答错）

  主题: billing request 362
  正文: The Thursday invoice includes a growth seat we already cancelled. Please correct the bill and refund the difference.

  标准答案：`false`；Laya：`true`（conf=0.583）

## refund_requested（noul）

题干：Does the user explicitly request a refund?

选项：
- `false` 否
- `true` 是

### 标准例

- **m1-0451**

  主题: billing request 451
  正文: Invoice 1450 was charged twice on Thursday. Refund the duplicate today or we cancel the growth plan.

  标准答案：`true`（Laya=true, conf=0.485）

- **m1-0018**

  主题: sales request 18
  正文: We are comparing vendors for a new growth contract. A analytics quote this month is enough, no rush.

  标准答案：`false`（Laya=false, conf=0.482）

### 易错例

- **m1-0351**（Laya 答错）

  主题: billing request 351
  正文: Invoice 1350 was charged twice on Wednesday. Refund the duplicate today or we cancel the enterprise plan.

  标准答案：`true`；Laya：`false`（conf=0.042）

- **m1-0393**（Laya 低置信度）

  主题: billing request 393
  正文: Can you explain the tax line on invoice 1392? We are not asking for a refund, just a breakdown.

  标准答案：`false`；Laya：`false`（conf=0.004）
