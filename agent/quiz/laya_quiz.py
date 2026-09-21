#!/usr/bin/env python3
"""CLI: build quiz pack from collected samples, or grade a sheet."""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import paths as _paths
sys.path.insert(0, os.path.join(_paths.AGENT, "m1"))
sys.path.insert(0, _paths.QUIZ)

from build import write_pack
from grade import grade

SAMPLES = os.path.join(_paths.OUT, "samples.jsonl")
QUIZ = _paths.QUIZ


def main():
    parser = argparse.ArgumentParser(description="Quiz pack for human review")
    sub = parser.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="generate guide + exam from samples")
    b.add_argument("--samples", default=SAMPLES)
    b.add_argument("--out", default=QUIZ)
    b.add_argument("--per-qid", type=int, default=8)

    g = sub.add_parser("grade", help="grade a filled answer sheet")
    g.add_argument("--sheet", required=True)
    g.add_argument("--grader", default="human")
    g.add_argument("--out", default=QUIZ)

    d = sub.add_parser("demo-sheet", help="auto-fill a sheet (mostly correct) for smoke test")
    d.add_argument("--out", default=QUIZ)
    d.add_argument("--noise", type=float, default=0.25, help="fraction of deliberate wrong answers")

    args = parser.parse_args()
    if args.cmd == "build":
        meta = write_pack(args.samples, args.out, per_qid=args.per_qid)
        print(json.dumps(meta, ensure_ascii=False, indent=2))
    elif args.cmd == "grade":
        print(json.dumps(grade(args.sheet, out_dir=args.out, grader=args.grader), ensure_ascii=False, indent=2))
    else:
        import random
        from build import _load
        key = {r["qid"]: r["answer_key"] for r in _load(os.path.join(args.out, "answer_key.jsonl"))}
        exam = _load(os.path.join(args.out, "exam.jsonl"))
        rng = random.Random(0)
        sheet_path = os.path.join(args.out, "demo_answers.jsonl")
        with open(sheet_path, "w") as f:
            for item in exam:
                ans = key[item["qid"]]
                if rng.random() < args.noise:
                    opts = [o["key"] for o in item["options"] if o["key"] != ans]
                    ans = rng.choice(opts) if opts else ans
                f.write(json.dumps({"qid": item["qid"], "answer": ans, "note": "demo"}, ensure_ascii=False) + "\n")
        print(json.dumps({"sheet": sheet_path, "n": len(exam)}, indent=2))


if __name__ == "__main__":
    main()
