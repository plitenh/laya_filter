"""Local operator strings: Chinese + English only (repo docs are French)."""
import os

LANG = os.environ.get("LAYA_LANG", "zh").lower()
if LANG not in ("zh", "en"):
    LANG = "zh"


MARKS = {
    "zh": {
        "keep": "确认该字段正确，不改",
        "fix": "矫正为批注值并入库",
        "flag": "存疑，不入库",
    },
    "en": {
        "keep": "Confirm the field; leave unchanged",
        "fix": "Correct to the annotated value; store as gold",
        "flag": "Unsure; do not store as gold",
    },
}

AXIS = {
    "zh": {"fact": "事实", "preference": "偏好", "other": "其他"},
    "en": {"fact": "fact", "preference": "preference", "other": "other"},
}


def t(block, key):
    return block.get(LANG, block["en"]).get(key, key)


def marks():
    return MARKS[LANG]


def axis_name(axis):
    return AXIS[LANG].get(axis, axis)


def guide_lines(questions, axes):
    if LANG == "zh":
        lines = [
            "# 新闻集成 · 批注说明",
            "",
            "批注用于**矫正正确性**，不是重写全文。每个字段打标记：",
            "",
            "| 标记 | 含义 |",
            "|---|---|",
        ]
        for k, v in marks().items():
            lines.append("| `%s` | %s |" % (k, v))
        lines += ["", "## 事实轴", ""]
        for field in axes["fact"]:
            q = questions[field]
            lines.append("- **%s**（%s）：%s" % (field, q["type"], q["instructions"]))
            _criteria(lines, q)
        lines += ["", "## 偏好轴", ""]
        for field in axes["preference"]:
            q = questions[field]
            lines.append("- **%s**（%s）：%s" % (field, q["type"], q["instructions"]))
            _criteria(lines, q)
        lines += [
            "",
            "## 答卷格式",
            "",
            "只写要改的字段。未写字段：与模型相同 → `keep`；不同 → `fix`。",
            "",
            "English copy: set `LAYA_LANG=en`.",
            "",
        ]
        return lines
    lines = [
        "# News integration · annotation guide",
        "",
        "Annotation **corrects field accuracy**; it is not a rewrite. Mark each field:",
        "",
        "| Mark | Meaning |",
        "|---|---|",
    ]
    for k, v in marks().items():
        lines.append("| `%s` | %s |" % (k, v))
    lines += ["", "## Fact axis", ""]
    for field in axes["fact"]:
        q = questions[field]
        lines.append("- **%s** (%s): %s" % (field, q["type"], q["instructions"]))
        _criteria(lines, q)
    lines += ["", "## Preference axis", ""]
    for field in axes["preference"]:
        q = questions[field]
        lines.append("- **%s** (%s): %s" % (field, q["type"], q["instructions"]))
        _criteria(lines, q)
    lines += [
        "",
        "## Answer sheet",
        "",
        "Only list fields you change. Missing fields: same as model → `keep`; different → `fix`.",
        "",
        "中文：设置 `LAYA_LANG=zh`。",
        "",
    ]
    return lines


def _criteria(lines, q):
    crit = q.get("criteria")
    if isinstance(crit, dict):
        for k, v in crit.items():
            lines.append("  - `%s` %s" % (k, v))
    elif isinstance(crit, list):
        for i, v in enumerate(crit):
            lines.append("  - `%d` %s" % (i, v))


def boundary_lines(rows, blocked, max_opts, axes):
    if LANG == "zh":
        head = [
            "# 新闻集成 · 决策边界",
            "",
            "批注：**矫正正确性**（事实）并记录版面偏好。Diff 见 `agent/annotate/`。",
            "",
            "choice 上限 **%d**。标签空间%s被拒绝。" % (max_opts, "已" if blocked else "未"),
            "",
            "## 两轴",
            "",
            "| 轴 | 字段 |",
            "|---|---|",
            "| 事实 | %s |" % ", ".join(axes["fact"]),
            "| 偏好 | %s |" % ", ".join(axes["preference"]),
            "",
            "## 字段",
            "",
            "| 字段 | 轴 | 原语 | 选项数 | 标签 | 状态 |",
            "|---|---|---|---|---|---|",
        ]
        for row in rows:
            head.append("| %s | %s | %s | %d | %s | %s |" % (
                row["id"], row["axis"], row["type"], row["options"],
                ", ".join(row["label_space"]), row["status"]))
        head += ["", "## 标记", "",
                 "- `keep`：确认正确", "- `fix`：矫正入库", "- `flag`：存疑不入库", ""]
        return head
    head = [
        "# News integration · decision boundary",
        "",
        "Annotation **corrects factual accuracy** and records feed preference. See `agent/annotate/` for diffs.",
        "",
        "choice cap **%d**. Label space %s rejected." % (max_opts, "IS" if blocked else "is not"),
        "",
        "## Axes",
        "",
        "| Axis | Fields |",
        "|---|---|",
        "| fact | %s |" % ", ".join(axes["fact"]),
        "| preference | %s |" % ", ".join(axes["preference"]),
        "",
        "## Fields",
        "",
        "| Field | Axis | Primitive | Options | Labels | Status |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        head.append("| %s | %s | %s | %d | %s | %s |" % (
            row["id"], row["axis"], row["type"], row["options"],
            ", ".join(row["label_space"]), row["status"]))
    head += ["", "## Marks", "",
             "- `keep`: confirm", "- `fix`: correct and store", "- `flag`: hold out", ""]
    return head


def diff_title(doc):
    if LANG == "zh":
        return "# 批注 Diff · %s\n\n批注人：%s · 矫正 %d · 存疑 %d · 确认 %d\n" % (
            doc["id"], doc["annotator"], doc["stats"]["fixes"],
            doc["stats"]["flags"], doc["stats"]["keeps"])
    return "# Annotation diff · %s\n\nAnnotator: %s · fixes %d · flags %d · keeps %d\n" % (
        doc["id"], doc["annotator"], doc["stats"]["fixes"],
        doc["stats"]["flags"], doc["stats"]["keeps"])


def diff_sections():
    if LANG == "zh":
        return {"title": "## 标题", "body": "## 正文", "table": "## 字段对照",
                "gold": "## 入库金标",
                "header": "| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |"}
    return {"title": "## Title", "body": "## Body", "table": "## Field table",
            "gold": "## Gold label",
            "header": "| Axis | Field | Model | After | Mark | Note |"}
