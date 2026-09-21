"""Field-level diff between Laya predictions and human annotations.

批注 = mark a correction on a decision field. Diff makes before/after visible
so editors can stamp fact and preference fixes without rewriting the whole row.
"""
import json
from datetime import datetime, timezone

from schema import AXES, QUESTIONS


MARKS = {
    "keep": "确认模型正确，不改",
    "fix": "矫正为批注值",
    "flag": "存疑，先记下不入库",
}


def _axis(field):
    return QUESTIONS.get(field, {}).get("axis", "other")


def field_diff(field, before, after, mark="fix", note=""):
    changed = before != after
    if mark == "keep":
        after = before
        changed = False
    return {
        "field": field,
        "axis": _axis(field),
        "before": before,
        "after": after,
        "changed": changed,
        "mark": mark,
        "note": note or "",
    }


def document_diff(sample_id, state, prediction, annotation, marks=None, notes=None, annotator="human"):
    """Build a full annotation diff for one news item.

    prediction / annotation: {field: value}
    marks: {field: keep|fix|flag}  default fix when values differ, else keep
    """
    marks = marks or {}
    notes = notes or {}
    fields = sorted(set(prediction) | set(annotation) | set(QUESTIONS))
    diffs = []
    for field in fields:
        if field not in QUESTIONS:
            continue
        before = prediction.get(field)
        after = annotation.get(field, before)
        if field in marks:
            mark = marks[field]
        elif before == after:
            mark = "keep"
        else:
            mark = "fix"
        diffs.append(field_diff(field, before, after, mark=mark, note=notes.get(field, "")))

    n_fix = sum(1 for d in diffs if d["mark"] == "fix" and d["changed"])
    n_flag = sum(1 for d in diffs if d["mark"] == "flag")
    by_axis = {ax: [] for ax in AXES}
    for d in diffs:
        by_axis.setdefault(d["axis"], []).append(d)

    final = {}
    for d in diffs:
        if d["mark"] == "flag":
            continue
        final[d["field"]] = d["after"] if d["mark"] == "fix" else d["before"]

    return {
        "id": sample_id,
        "ts": datetime.now(timezone.utc).isoformat(),
        "annotator": annotator,
        "state": state,
        "prediction": prediction,
        "annotation": annotation,
        "diffs": diffs,
        "by_axis": {k: v for k, v in by_axis.items() if v},
        "stats": {
            "fields": len(diffs),
            "fixes": n_fix,
            "flags": n_flag,
            "keeps": sum(1 for d in diffs if d["mark"] == "keep"),
        },
        "final_gold": final,
    }


def render_markdown(diff_doc):
    lines = [
        "# 批注 Diff · %s" % diff_doc["id"],
        "",
        "批注人：%s · 矫正 %d · 存疑 %d · 确认 %d"
        % (diff_doc["annotator"], diff_doc["stats"]["fixes"],
           diff_doc["stats"]["flags"], diff_doc["stats"]["keeps"]),
        "",
    ]
    state = diff_doc.get("state") or {}
    if isinstance(state, dict):
        if state.get("title"):
            lines += ["## 标题", "", state["title"], ""]
        if state.get("body"):
            lines += ["## 正文", "", state["body"], ""]
    lines += ["## 字段对照", "", "| 轴 | 字段 | 模型 | 批注后 | 标记 | 说明 |", "|---|---|---|---|---|---|"]
    for d in diff_doc["diffs"]:
        arrow = "`%s` → `%s`" % (d["before"], d["after"]) if d["changed"] else "`%s`" % d["before"]
        if d["changed"]:
            cell = "%s ~~%s~~ **%s**" % ("", d["before"], d["after"])
        else:
            cell = "`%s`" % d["before"]
        lines.append("| %s | %s | `%s` | %s | **%s** | %s |" % (
            d["axis"], d["field"], d["before"],
            ("**%s**" % d["after"]) if d["changed"] else "`%s`" % d["after"],
            d["mark"], d["note"] or MARKS.get(d["mark"], "")))
    lines += ["", "## 入库金标", "", "```json", json.dumps(diff_doc["final_gold"], ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)


def render_unified(diff_doc):
    """Unified-diff style block for terminals / PR review habits."""
    lines = ["--- laya/%s" % diff_doc["id"], "+++ annotate/%s" % diff_doc["id"]]
    for d in diff_doc["diffs"]:
        path = "%s/%s" % (d["axis"], d["field"])
        if not d["changed"] and d["mark"] == "keep":
            lines.append(" %s: %s" % (path, d["before"]))
        elif d["mark"] == "flag":
            lines.append("? %s: %s  # FLAG %s" % (path, d["before"], d["note"]))
        else:
            lines.append("-%s: %s" % (path, d["before"]))
            lines.append("+%s: %s" % (path, d["after"]))
            if d["note"]:
                lines.append(" # %s" % d["note"])
    return "\n".join(lines) + "\n"
