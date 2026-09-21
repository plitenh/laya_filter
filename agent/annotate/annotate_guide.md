# 新闻集成 · 批注说明

批注用来**矫正正确性**，不是重新写作。对每个字段打标记：

| 标记 | 含义 |
|---|---|
| `keep` | 模型该字段正确，维持 |
| `fix` | 写成 `after`，矫正入库 |
| `flag` | 存疑，不进金标 |

## 事实轴

- **factual**（noul）：Is the article's core claim factually sound as stated (no clear falsehood)?
- **claim_status**（choice）：How should the claim be classified for the news desk?
  - `accurate` supported and currently valid
  - `outdated` was true but is stale or superseded
  - `misleading` technically partial but frames wrongly
  - `unverifiable` cannot check from the given text alone

## 偏好轴

- **channel**（choice）：Which channel should this item go to in the feed?
  - `politics` government, elections, diplomacy
  - `business` markets, companies, economy
  - `tech` science, software, gadgets
  - `society` culture, cities, daily life
  - `sports` athletics and games
  - `other` none of the above
- **publish**（noul）：Should this item be published into the integrated feed?
- **salience**（score）：How prominent should this item be?
  - `0` skip or bury
  - `1` normal slot
  - `2` lead / top story

## 答卷格式

```json
{
  "id": "news-0001",
  "marks": {
    "factual": "fix",
    "channel": "keep"
  },
  "after": {
    "factual": false
  },
  "notes": {
    "factual": "标题夸大，正文未证实"
  }
}
```

只写要动的字段即可；未写的字段默认：与模型相同则 `keep`，不同则 `fix`。
