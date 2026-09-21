"""Field-level diff: annotation corrects accuracy; before/after for marking."""
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "m1"))

from schema import AXES, QUESTIONS
from i18n import axis_name, diff_sections, diff_title, marks as mark_labels


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
    sec = diff_sections()
    labels = mark_labels()
    lines = [diff_title(diff_doc).rstrip(), ""]
    state = diff_doc.get("state") or {}
    if isinstance(state, dict):
        if state.get("title"):
            lines += [sec["title"], "", state["title"], ""]
        if state.get("body"):
            lines += [sec["body"], "", state["body"], ""]
    lines += [sec["table"], "", sec["header"], "|---|---|---|---|---|---|"]
    for d in diff_doc["diffs"]:
        after = ("**%s**" % d["after"]) if d["changed"] else "`%s`" % d["after"]
        lines.append("| %s | %s | `%s` | %s | **%s** | %s |" % (
            axis_name(d["axis"]), d["field"], d["before"], after,
            d["mark"], d["note"] or labels.get(d["mark"], "")))
    lines += ["", sec["gold"], "", "```json",
              json.dumps(diff_doc["final_gold"], ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)


def render_unified(diff_doc):
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
