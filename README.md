# Laya 新闻集成 · 筛选与批注

以 [Laya](https://github.com/NandhaKishorM/laya) 做新闻决策；**批注 = 矫正正确性**（事实轴）并记录版面偏好。字段级 **diff** 方便对照模型输出与人工标记。

仓库：https://github.com/plitenh/laya_filter

## 两轴决策

| 轴 | 字段 | 含义 |
|----|------|------|
| 事实 | `factual` / `claim_status` | 是否站得住、准确/过时/误导/不可核验 |
| 偏好 | `channel` / `publish` / `salience` | 频道、是否进 feed、显著度 |

## 批注 Diff

```
新闻条目 + Laya 预测
        │
        ▼
  编辑打标记  keep | fix | flag
        │
        ▼
  field diff (before → after)
        │
        ├─ diffs.md / diffs.unified.txt   可读对照
        └─ annotated_gold.jsonl           入库金标
```

标记：

- `keep` — 该字段正确，不改  
- `fix` — 写成 `after`，矫正入库  
- `flag` — 存疑，不进金标  

## 快速开始

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1) 种子新闻语料
python agent/m1/generate_news.py --n 120

# 2) 生成批注台（含假 Laya 漂移，便于离线看 diff）
python agent/annotate/desk.py build --corpus agent/data/news_seed.jsonl --limit 40

# 3) 演示批注并出 diff
python agent/annotate/desk.py demo

# 查看
#   agent/annotate/annotate_guide.md
#   agent/annotate/diffs.md
#   agent/annotate/diffs.unified.txt
#   agent/annotate/annotated_gold.jsonl
```

答卷一行示例：

```json
{
  "id": "news-0001",
  "marks": {"factual": "fix", "channel": "keep"},
  "after": {"factual": false},
  "notes": {"factual": "标题夸大，正文未证实"}
}
```

统一 diff 片段示例：

```
--- laya/news-0003
+++ annotate/news-0003
-fact/factual: True
+fact/factual: False
-fact/claim_status: accurate
+fact/claim_status: misleading
 preference/channel: politics
```

## 目录

| 路径 | 内容 |
|------|------|
| `agent/m1/schema.py` | 新闻两轴标签空间 |
| `agent/annotate/diff.py` | 字段 diff / Markdown / unified |
| `agent/annotate/desk.py` | 批注台 CLI |
| `agent/data/news_seed.jsonl` | 种子新闻（生成） |
| `deploy/` | 推理服务与 MAPE-K 骨架 |

接真 Laya：先 `collect` 把 `answers.*.prediction` 写进语料，再 `desk.py build`；有 `answers` 时不再用假漂移。

## 环境变量

| 变量 | 含义 |
|------|------|
| `LAYA_FILTER_ROOT` | 仓库根 |
| `LAYA_MODELS` | 本地 Laya checkpoint |

权重不入库。
