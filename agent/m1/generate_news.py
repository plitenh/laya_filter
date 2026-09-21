#!/usr/bin/env python3
"""Seed news items with fact + preference gold for annotation demos."""
import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import paths as _paths

TEMPLATES = [
    # factual, claim_status, channel, publish, salience, title, body
    (True, "accurate", "tech", True, 2,
     "Chip foundry opens 2nm pilot line",
     "The foundry said its first 2nm pilot wafers passed yield gates this week. Independent analysts confirmed the timeline matches prior guidance."),
    (True, "accurate", "business", True, 1,
     "Retail chain posts steady quarter",
     "Same-store sales rose 3% year over year. The company kept full-year guidance unchanged."),
    (False, "misleading", "politics", False, 0,
     "Lawmakers ban all encryption overnight",
     "A draft memo floated study of messaging apps. No vote was scheduled and no ban was enacted."),
    (False, "outdated", "tech", False, 0,
     "Browser X still has no dark mode",
     "Dark mode shipped two releases ago. The article quotes a 2022 support page."),
    (True, "unverifiable", "society", True, 1,
     "City hall sources hint at park redesign",
     "Anonymous officials say a redesign is under discussion. No documents or named sources are provided."),
    (True, "accurate", "sports", True, 1,
     "Home side wins derby 2-1",
     "Two second-half goals overturned an early deficit. Match logs and league site agree on the score."),
    (False, "misleading", "business", False, 0,
     "Startup valued at one trillion after seed",
     "A blog post mistook a meme screenshot for a term sheet. No filing supports the claim."),
    (True, "accurate", "politics", True, 2,
     "Treaty talks resume next Monday",
     "Both foreign ministries confirmed envoys will meet. The agenda covers trade and border posts."),
]


def generate(n, seed=11):
    rng = random.Random(seed)
    rows = []
    i = 0
    while len(rows) < n:
        factual, status, channel, publish, salience, title, body = TEMPLATES[i % len(TEMPLATES)]
        i += 1
        # light paraphrase noise
        suffix = rng.choice(["", " Editors are watching follow-ups.", " Wire desks flagged it this morning."])
        rows.append({
            "id": "news-%04d" % (len(rows) + 1),
            "state": {
                "title": title,
                "body": body + suffix,
                "source": rng.choice(["wire-a", "wire-b", "blog-c", "desk-d"]),
            },
            "gold": {
                "factual": factual,
                "claim_status": status,
                "channel": channel,
                "publish": publish,
                "salience": salience,
            },
        })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=120)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    out = args.out or os.path.join(_paths.DATA, "sample.jsonl")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    rows = generate(args.n)
    with open(out, "w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(out, len(rows))


if __name__ == "__main__":
    main()
