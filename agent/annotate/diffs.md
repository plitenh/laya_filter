# 批注 Diff · news-0001

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Chip foundry opens 2nm pilot line

## 正文

The foundry said its first 2nm pilot wafers passed yield gates this week. Independent analysts confirmed the timeline matches prior guidance. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `tech` | `tech` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `2` | `2` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "tech",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 2
}
```

---

# 批注 Diff · news-0002

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Retail chain posts steady quarter

## 正文

Same-store sales rose 3% year over year. The company kept full-year guidance unchanged. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `business` | `business` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `1` | `1` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "business",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0003

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Lawmakers ban all encryption overnight

## 正文

A draft memo floated study of messaging apps. No vote was scheduled and no ban was enacted.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `politics` | `politics` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `misleading` | `misleading` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | `0` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "politics",
  "claim_status": "misleading",
  "factual": false,
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0004

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Browser X still has no dark mode

## 正文

Dark mode shipped two releases ago. The article quotes a 2022 support page. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `tech` | `tech` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `outdated` | `outdated` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `2` | **0** | **fix** | 矫正正确性 |

## 入库金标

```json
{
  "channel": "tech",
  "claim_status": "outdated",
  "factual": false,
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0005

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

City hall sources hint at park redesign

## 正文

Anonymous officials say a redesign is under discussion. No documents or named sources are provided.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `society` | `society` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `unverifiable` | `unverifiable` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `1` | `1` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "society",
  "claim_status": "unverifiable",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0006

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Home side wins derby 2-1

## 正文

Two second-half goals overturned an early deficit. Match logs and league site agree on the score. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `sports` | `sports` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `1` | `1` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "sports",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0007

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Startup valued at one trillion after seed

## 正文

A blog post mistook a meme screenshot for a term sheet. No filing supports the claim.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `business` | `business` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `misleading` | `misleading` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | **False** | **fix** | 矫正正确性 |
| preference | salience | `0` | `0` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "business",
  "claim_status": "misleading",
  "factual": false,
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0008

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Treaty talks resume next Monday

## 正文

Both foreign ministries confirmed envoys will meet. The agenda covers trade and border posts. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `politics` | `politics` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `2` | **0** | **fix** | 版面偏好调整 |

## 入库金标

```json
{
  "channel": "politics",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 0
}
```

---

# 批注 Diff · news-0009

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Chip foundry opens 2nm pilot line

## 正文

The foundry said its first 2nm pilot wafers passed yield gates this week. Independent analysts confirmed the timeline matches prior guidance. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `tech` | `tech` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `2` | `2` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "tech",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 2
}
```

---

# 批注 Diff · news-0010

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Retail chain posts steady quarter

## 正文

Same-store sales rose 3% year over year. The company kept full-year guidance unchanged. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `business` | `business` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `misleading` | **accurate** | **fix** | 矫正正确性 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `1` | `1` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "business",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0011

批注人：demo · 矫正 0 · 存疑 1 · 确认 4

## 标题

Lawmakers ban all encryption overnight

## 正文

A draft memo floated study of messaging apps. No vote was scheduled and no ban was enacted. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `politics` | `politics` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `misleading` | `misleading` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **flag** | 拿不准，先旗标 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | `0` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "politics",
  "claim_status": "misleading",
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0012

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Browser X still has no dark mode

## 正文

Dark mode shipped two releases ago. The article quotes a 2022 support page.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `tech` | `tech` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `outdated` | `outdated` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | `0` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "tech",
  "claim_status": "outdated",
  "factual": false,
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0013

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

City hall sources hint at park redesign

## 正文

Anonymous officials say a redesign is under discussion. No documents or named sources are provided.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `society` | `society` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `unverifiable` | `unverifiable` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | **1** | **fix** | 矫正正确性 |

## 入库金标

```json
{
  "channel": "society",
  "claim_status": "unverifiable",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0014

批注人：demo · 矫正 2 · 存疑 0 · 确认 3

## 标题

Home side wins derby 2-1

## 正文

Two second-half goals overturned an early deficit. Match logs and league site agree on the score. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `sports` | `sports` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | **True** | **fix** | 矫正正确性 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `1` | **0** | **fix** | 版面偏好调整 |

## 入库金标

```json
{
  "channel": "sports",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 0
}
```

---

# 批注 Diff · news-0015

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Startup valued at one trillion after seed

## 正文

A blog post mistook a meme screenshot for a term sheet. No filing supports the claim. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `business` | `business` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `misleading` | `misleading` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | **1** | **fix** | 版面偏好调整 |

## 入库金标

```json
{
  "channel": "business",
  "claim_status": "misleading",
  "factual": false,
  "publish": false,
  "salience": 1
}
```

---

# 批注 Diff · news-0016

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Treaty talks resume next Monday

## 正文

Both foreign ministries confirmed envoys will meet. The agenda covers trade and border posts. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `politics` | `politics` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `2` | `2` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "politics",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 2
}
```

---

# 批注 Diff · news-0017

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Chip foundry opens 2nm pilot line

## 正文

The foundry said its first 2nm pilot wafers passed yield gates this week. Independent analysts confirmed the timeline matches prior guidance. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `tech` | `tech` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `2` | `2` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "tech",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 2
}
```

---

# 批注 Diff · news-0018

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Retail chain posts steady quarter

## 正文

Same-store sales rose 3% year over year. The company kept full-year guidance unchanged. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `business` | `business` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | **True** | **fix** | 矫正正确性 |
| preference | salience | `1` | `1` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "business",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0019

批注人：demo · 矫正 2 · 存疑 0 · 确认 3

## 标题

Lawmakers ban all encryption overnight

## 正文

A draft memo floated study of messaging apps. No vote was scheduled and no ban was enacted. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `politics` | `politics` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `unverifiable` | **misleading** | **fix** | 矫正正确性 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | **1** | **fix** | 版面偏好调整 |

## 入库金标

```json
{
  "channel": "politics",
  "claim_status": "misleading",
  "factual": false,
  "publish": false,
  "salience": 1
}
```

---

# 批注 Diff · news-0020

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Browser X still has no dark mode

## 正文

Dark mode shipped two releases ago. The article quotes a 2022 support page. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `tech` | `tech` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `outdated` | `outdated` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | `0` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "tech",
  "claim_status": "outdated",
  "factual": false,
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0021

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

City hall sources hint at park redesign

## 正文

Anonymous officials say a redesign is under discussion. No documents or named sources are provided. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `society` | `society` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `unverifiable` | `unverifiable` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `1` | `1` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "society",
  "claim_status": "unverifiable",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0022

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Home side wins derby 2-1

## 正文

Two second-half goals overturned an early deficit. Match logs and league site agree on the score. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `sports` | `sports` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | **1** | **fix** | 矫正正确性 |

## 入库金标

```json
{
  "channel": "sports",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0023

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Startup valued at one trillion after seed

## 正文

A blog post mistook a meme screenshot for a term sheet. No filing supports the claim. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `business` | `business` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `misleading` | `misleading` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | **False** | **fix** | 矫正正确性 |
| preference | salience | `0` | `0` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "business",
  "claim_status": "misleading",
  "factual": false,
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0024

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Treaty talks resume next Monday

## 正文

Both foreign ministries confirmed envoys will meet. The agenda covers trade and border posts. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `politics` | `politics` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `2` | `2` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "politics",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 2
}
```

---

# 批注 Diff · news-0025

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Chip foundry opens 2nm pilot line

## 正文

The foundry said its first 2nm pilot wafers passed yield gates this week. Independent analysts confirmed the timeline matches prior guidance. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `tech` | `tech` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `2` | `2` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "tech",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 2
}
```

---

# 批注 Diff · news-0026

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Retail chain posts steady quarter

## 正文

Same-store sales rose 3% year over year. The company kept full-year guidance unchanged.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `business` | `business` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `1` | **0** | **fix** | 版面偏好调整 |

## 入库金标

```json
{
  "channel": "business",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 0
}
```

---

# 批注 Diff · news-0027

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Lawmakers ban all encryption overnight

## 正文

A draft memo floated study of messaging apps. No vote was scheduled and no ban was enacted. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `politics` | `politics` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `misleading` | `misleading` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | `0` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "politics",
  "claim_status": "misleading",
  "factual": false,
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0028

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Browser X still has no dark mode

## 正文

Dark mode shipped two releases ago. The article quotes a 2022 support page. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `tech` | `tech` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `outdated` | `outdated` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | `0` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "tech",
  "claim_status": "outdated",
  "factual": false,
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0029

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

City hall sources hint at park redesign

## 正文

Anonymous officials say a redesign is under discussion. No documents or named sources are provided. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `politics` | **society** | **fix** | 矫正正确性 |
| fact | claim_status | `unverifiable` | `unverifiable` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `1` | `1` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "society",
  "claim_status": "unverifiable",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0030

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Home side wins derby 2-1

## 正文

Two second-half goals overturned an early deficit. Match logs and league site agree on the score.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `sports` | `sports` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | **1** | **fix** | 矫正正确性 |

## 入库金标

```json
{
  "channel": "sports",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0031

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Startup valued at one trillion after seed

## 正文

A blog post mistook a meme screenshot for a term sheet. No filing supports the claim. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `business` | `business` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `unverifiable` | **misleading** | **fix** | 矫正正确性 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | `0` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "business",
  "claim_status": "misleading",
  "factual": false,
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0032

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Treaty talks resume next Monday

## 正文

Both foreign ministries confirmed envoys will meet. The agenda covers trade and border posts.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `politics` | `politics` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `2` | `2` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "politics",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 2
}
```

---

# 批注 Diff · news-0033

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Chip foundry opens 2nm pilot line

## 正文

The foundry said its first 2nm pilot wafers passed yield gates this week. Independent analysts confirmed the timeline matches prior guidance.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `other` | **tech** | **fix** | 矫正正确性 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `2` | `2` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "tech",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 2
}
```

---

# 批注 Diff · news-0034

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Retail chain posts steady quarter

## 正文

Same-store sales rose 3% year over year. The company kept full-year guidance unchanged. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `business` | `business` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `1` | `1` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "business",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0035

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Lawmakers ban all encryption overnight

## 正文

A draft memo floated study of messaging apps. No vote was scheduled and no ban was enacted. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `politics` | `politics` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `misleading` | `misleading` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | `0` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "politics",
  "claim_status": "misleading",
  "factual": false,
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0036

批注人：demo · 矫正 1 · 存疑 0 · 确认 4

## 标题

Browser X still has no dark mode

## 正文

Dark mode shipped two releases ago. The article quotes a 2022 support page. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `politics` | **tech** | **fix** | 矫正正确性 |
| fact | claim_status | `outdated` | `outdated` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | `0` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "tech",
  "claim_status": "outdated",
  "factual": false,
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0037

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

City hall sources hint at park redesign

## 正文

Anonymous officials say a redesign is under discussion. No documents or named sources are provided. Wire desks flagged it this morning.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `society` | `society` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `unverifiable` | `unverifiable` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `1` | `1` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "society",
  "claim_status": "unverifiable",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0038

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Home side wins derby 2-1

## 正文

Two second-half goals overturned an early deficit. Match logs and league site agree on the score. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `sports` | `sports` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `1` | `1` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "sports",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 1
}
```

---

# 批注 Diff · news-0039

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Startup valued at one trillion after seed

## 正文

A blog post mistook a meme screenshot for a term sheet. No filing supports the claim. Editors are watching follow-ups.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `business` | `business` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `misleading` | `misleading` | **keep** | 确认模型正确，不改 |
| fact | factual | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | publish | `False` | `False` | **keep** | 确认模型正确，不改 |
| preference | salience | `0` | `0` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "business",
  "claim_status": "misleading",
  "factual": false,
  "publish": false,
  "salience": 0
}
```

---

# 批注 Diff · news-0040

批注人：demo · 矫正 0 · 存疑 0 · 确认 5

## 标题

Treaty talks resume next Monday

## 正文

Both foreign ministries confirmed envoys will meet. The agenda covers trade and border posts.

## 字段对照

| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |
|---|---|---|---|---|---|
| preference | channel | `politics` | `politics` | **keep** | 确认模型正确，不改 |
| fact | claim_status | `accurate` | `accurate` | **keep** | 确认模型正确，不改 |
| fact | factual | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | publish | `True` | `True` | **keep** | 确认模型正确，不改 |
| preference | salience | `2` | `2` | **keep** | 确认模型正确，不改 |

## 入库金标

```json
{
  "channel": "politics",
  "claim_status": "accurate",
  "factual": true,
  "publish": true,
  "salience": 2
}
```
