#!/usr/bin/env python3
"""Filter a corpus, then self-train the decision head with RL."""
import argparse
import json
import sys

from corpus import label_records, structural_filter
from runtime import STATE_DIR, load_agent, questions_for
from train_head import train_head

import os


def _read_jsonl(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _write_jsonl(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _gold_hit(agent, records, questions):
    hits, total = 0, 0
    for rec in records:
        gold = rec.get("gold") or {}
        if not gold:
            continue
        pred = agent.predict(rec["state"], questions)["answers"]
        for qid, truth in gold.items():
            if qid not in pred:
                continue
            ans = pred[qid]
            total += 1
            if ans["type"] == "choice" and ans["choice"] == truth:
                hits += 1
            elif ans["type"] == "noul" and ((ans["noul"] >= 0.5) == bool(truth)):
                hits += 1
            elif ans["type"] == "score" and int(round(ans["score"])) == int(truth):
                hits += 1
    return hits, total


def main():
    parser = argparse.ArgumentParser(description="Filter corpus and RL-train the Laya head")
    parser.add_argument("corpus", nargs="?", default=None)
    parser.add_argument("--preset", default="default")
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--min-conf", type=float, default=0.15)
    parser.add_argument("--filter-only", action="store_true")
    args = parser.parse_args()
    if not args.corpus:
        args.corpus = os.path.join(os.path.dirname(__file__), "..", "agent", "data", "sample.jsonl")

    records = _read_jsonl(args.corpus)
    questions = questions_for(args.preset)
    kept, rejected = structural_filter(records)
    print("structural: %d kept, %d rejected" % (len(kept), len(rejected)), flush=True)
    for rec in rejected:
        print("  drop %-16s %s" % (rec["reason"], rec.get("id", "")), flush=True)

    print("loading INT8 Laya...", flush=True)
    agent = load_agent()
    accepted, review = label_records(agent, kept, questions, args.min_conf)
    print("labels: %d train, %d review" % (len(accepted), len(review)), flush=True)
    for rec in review:
        print("  review %-16s %s" % (rec["reason"], rec.get("id", "")), flush=True)

    out_dir = STATE_DIR
    _write_jsonl(os.path.join(out_dir, "train.jsonl"), accepted)
    _write_jsonl(os.path.join(out_dir, "rejected.jsonl"), rejected + review)
    if args.filter_only or not accepted:
        print("wrote %s" % out_dir)
        return

    gold_rows = [r for r in accepted if r.get("gold")]
    before_hits, before_n = _gold_hit(agent, gold_rows, questions)
    print("RL self-train, %d steps" % args.steps, flush=True)
    stats = train_head(agent, accepted, questions, steps=args.steps)
    after_hits, after_n = _gold_hit(agent, gold_rows, questions)
    summary = {
        "structural_kept": len(kept),
        "structural_rejected": len(rejected),
        "train": len(accepted),
        "review": len(review),
        "gold_before": [before_hits, before_n],
        "gold_after": [after_hits, after_n],
        **stats,
    }
    with open(os.path.join(out_dir, "last_run.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))
    sys.stdout.write(
        "gold %d/%d -> %d/%d   reward %.3f -> %.3f\n"
        % (before_hits, before_n, after_hits, after_n, stats["reward_before"], stats["reward_after"])
    )


if __name__ == "__main__":
    main()
