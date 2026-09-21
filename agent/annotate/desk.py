#!/usr/bin/env python3
"""Annotation desk: build review packs, apply 批注 marks, emit field diffs."""
import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import paths as _paths
sys.path.insert(0, _paths.AGENT)
sys.path.insert(0, os.path.join(_paths.AGENT, "m1"))
sys.path.insert(0, os.path.join(_paths.AGENT, "annotate"))

from schema import AXES, QUESTIONS, label_space
from diff import document_diff, render_markdown, render_unified
from i18n import LANG, guide_lines

ANNOTATE = os.path.join(_paths.AGENT, "annotate")


def _load(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def _dump(path, rows):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _canon(field, value):
    q = QUESTIONS[field]
    if q["type"] == "choice":
        return str(value)
    if q["type"] == "score":
        return int(value)
    if isinstance(value, bool):
        return value
    s = str(value).strip().lower()
    return s in ("1", "true", "yes", "y", "是")


def fake_laya(gold, rng):
    """Offline stand-in: mostly copy gold, sometimes drift so diffs appear."""
    pred = dict(gold)
    if rng.random() < 0.35:
        field = rng.choice(list(QUESTIONS))
        q = QUESTIONS[field]
        if q["type"] == "noul":
            pred[field] = not bool(gold[field])
        elif q["type"] == "score":
            opts = list(range(len(q["criteria"])))
            pred[field] = rng.choice([x for x in opts if x != gold[field]] or opts)
        else:
            opts = list(q["criteria"])
            pred[field] = rng.choice([x for x in opts if x != gold[field]] or opts)
    return pred


def build_pack(corpus_path, out_dir=ANNOTATE, limit=40, seed=0):
    """Create an annotation desk pack: items + blank mark sheet + guide."""
    os.makedirs(out_dir, exist_ok=True)
    rows = _load(corpus_path)[:limit]
    rng = random.Random(seed)
    items = []
    for row in rows:
        gold = {k: _canon(k, v) for k, v in (row.get("gold") or {}).items() if k in QUESTIONS}
        # Prefer real Laya answers if present under answers.*.prediction
        pred = {}
        if row.get("answers"):
            for field, ans in row["answers"].items():
                if field in QUESTIONS:
                    pred[field] = _canon(field, ans.get("prediction", ans.get("gold")))
        if not pred and gold:
            pred = fake_laya(gold, rng)
        items.append({
            "id": row["id"],
            "state": row["state"],
            "prediction": pred,
            "gold_hint": gold,  # only for demo key; strip in public sheet if needed
        })

    guide = guide_lines(QUESTIONS, AXES)
    guide += [
        "```json",
        json.dumps({
            "id": "news-0001",
            "marks": {"factual": "fix", "channel": "keep"},
            "after": {"factual": False},
            "notes": {"factual": "headline overstates the body" if LANG == "en" else "标题夸大，正文未证实"},
        }, ensure_ascii=False, indent=2),
        "```",
        "",
    ]
    guide_path = os.path.join(out_dir, "annotate_guide.md")
    with open(guide_path, "w") as f:
        f.write("\n".join(guide))

    items_path = os.path.join(out_dir, "items.jsonl")
    _dump(items_path, items)

    sheet = []
    for it in items:
        sheet.append({
            "id": it["id"],
            "marks": {},
            "after": {},
            "notes": {},
        })
    sheet_path = os.path.join(out_dir, "sheet.template.jsonl")
    _dump(sheet_path, sheet)

    # preview diffs vs gold_hint for desk QA
    previews = []
    for it in items:
        if not it.get("gold_hint"):
            continue
        doc = document_diff(it["id"], it["state"], it["prediction"], it["gold_hint"], annotator="seed-gold")
        previews.append(doc)
    _dump(os.path.join(out_dir, "preview_diffs.jsonl"), previews)

    meta = {
        "guide": guide_path,
        "items": items_path,
        "sheet_template": sheet_path,
        "n": len(items),
        "axes": AXES,
        "label_spaces": {k: label_space(v) for k, v in QUESTIONS.items()},
    }
    with open(os.path.join(out_dir, "pack.json"), "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    return meta


def apply_sheet(sheet_path, items_path=None, out_dir=ANNOTATE, annotator="human"):
    items_path = items_path or os.path.join(out_dir, "items.jsonl")
    items = {r["id"]: r for r in _load(items_path)}
    sheet = _load(sheet_path)
    diffs, golds, md_pages, unified = [], [], [], []
    for row in sheet:
        item = items.get(row["id"])
        if not item:
            continue
        pred = item["prediction"]
        after = dict(pred)
        raw_after = row.get("after") or {}
        for k, v in raw_after.items():
            if k in QUESTIONS:
                after[k] = _canon(k, v)
        # If after empty but marks say fix, keep prediction (no-op) unless values provided
        doc = document_diff(
            item["id"], item["state"], pred, after,
            marks=row.get("marks") or {},
            notes=row.get("notes") or {},
            annotator=annotator,
        )
        diffs.append(doc)
        if doc["final_gold"]:
            golds.append({
                "id": item["id"],
                "state": item["state"],
                "gold": doc["final_gold"],
                "source": "annotation_diff",
                "annotator": annotator,
                "stats": doc["stats"],
            })
        md_pages.append(render_markdown(doc))
        unified.append(render_unified(doc))

    _dump(os.path.join(out_dir, "diffs.jsonl"), diffs)
    _dump(os.path.join(out_dir, "annotated_gold.jsonl"), golds)
    with open(os.path.join(out_dir, "diffs.md"), "w") as f:
        f.write("\n---\n\n".join(md_pages))
    with open(os.path.join(out_dir, "diffs.unified.txt"), "w") as f:
        f.write("\n".join(unified))
    summary = {
        "items": len(diffs),
        "fixes": sum(d["stats"]["fixes"] for d in diffs),
        "flags": sum(d["stats"]["flags"] for d in diffs),
        "gold_rows": len(golds),
        "diffs_jsonl": os.path.join(out_dir, "diffs.jsonl"),
        "diffs_md": os.path.join(out_dir, "diffs.md"),
        "diffs_unified": os.path.join(out_dir, "diffs.unified.txt"),
        "gold": os.path.join(out_dir, "annotated_gold.jsonl"),
    }
    with open(os.path.join(out_dir, "last_annotate.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    return summary


def demo_sheet(items_path=None, out_dir=ANNOTATE, noise=0.3, seed=1):
    """Fill a sheet that fixes disagreements with seed gold (for smoke tests)."""
    items_path = items_path or os.path.join(out_dir, "items.jsonl")
    items = _load(items_path)
    rng = random.Random(seed)
    sheet = []
    for it in items:
        gold = it.get("gold_hint") or it["prediction"]
        marks, after, notes = {}, {}, {}
        for field, before in it["prediction"].items():
            truth = gold.get(field, before)
            if before != truth:
                if rng.random() < 0.1:
                    marks[field] = "flag"
                    notes[field] = "拿不准，先旗标"
                else:
                    marks[field] = "fix"
                    after[field] = truth
                    notes[field] = "矫正正确性"
            else:
                marks[field] = "keep"
        # occasional preference tweak even when equal
        if rng.random() < noise * 0.2:
            marks["salience"] = "fix"
            after["salience"] = int(not bool(it["prediction"].get("salience", 1))) % 3
            notes["salience"] = "版面偏好调整"
        sheet.append({"id": it["id"], "marks": marks, "after": after, "notes": notes})
    path = os.path.join(out_dir, "demo_sheet.jsonl")
    _dump(path, sheet)
    return {"sheet": path, "n": len(sheet)}


def main():
    parser = argparse.ArgumentParser(description="News annotation desk with field diffs")
    sub = parser.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="build annotation pack from news corpus")
    b.add_argument("--corpus", required=True)
    b.add_argument("--out", default=ANNOTATE)
    b.add_argument("--limit", type=int, default=40)

    a = sub.add_parser("apply", help="apply mark sheet and write diffs")
    a.add_argument("--sheet", required=True)
    a.add_argument("--items", default=None)
    a.add_argument("--out", default=ANNOTATE)
    a.add_argument("--annotator", default="human")

    d = sub.add_parser("demo", help="build demo sheet from gold_hint and apply")
    d.add_argument("--out", default=ANNOTATE)

    args = parser.parse_args()
    if args.cmd == "build":
        print(json.dumps(build_pack(args.corpus, args.out, limit=args.limit), ensure_ascii=False, indent=2))
    elif args.cmd == "apply":
        print(json.dumps(apply_sheet(args.sheet, args.items, args.out, args.annotator), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(demo_sheet(out_dir=args.out), ensure_ascii=False, indent=2))
        print(json.dumps(apply_sheet(os.path.join(args.out, "demo_sheet.jsonl"), out_dir=args.out, annotator="demo"), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
