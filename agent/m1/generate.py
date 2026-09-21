#!/usr/bin/env python3
"""Seed 500 labeled support tickets for the milestone-1 sample pool."""
import argparse
import json
import os
import random
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import paths as _paths

TEMPLATES = [
    ("billing", 2, True, True,
     "Invoice {n} was charged twice on {day}. Refund the duplicate today or we cancel the {plan} plan."),
    ("billing", 1, False, True,
     "The {day} invoice includes a {plan} seat we already cancelled. Please correct the bill and refund the difference."),
    ("billing", 1, False, False,
     "Can you explain the tax line on invoice {n}? We are not asking for a refund, just a breakdown."),
    ("technical", 2, False, False,
     "{product} has been returning HTTP 500 for {mins} minutes. Customers cannot complete checkout. Page on-call."),
    ("technical", 1, False, False,
     "The {product} webhook has been timing out since {day}. No double charge, we only need the bug fixed."),
    ("technical", 2, True, False,
     "Login is down for the whole {plan} workspace. If this is not fixed today we will move off the platform."),
    ("sales", 1, False, False,
     "Please send enterprise pricing for {seats} seats of {product}. We have not purchased yet."),
    ("sales", 0, False, False,
     "We are comparing vendors for a new {plan} contract. A {product} quote this month is enough, no rush."),
    ("other", 0, False, False,
     "Where do I change the timezone for user {n} in {product}? No rush, this is only a how-to."),
    ("other", 1, False, False,
     "Please update the billing contact email for account {n} to ops-{n}@example.com. Not a refund request."),
]

PLANS = ["starter", "growth", "enterprise"]
PRODUCTS = ["checkout", "webhooks", "SSO", "analytics"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def generate(n, seed=7):
    rng = random.Random(seed)
    rows = []
    i = 0
    while len(rows) < n:
        dept, urgency, churn, refund, pattern = TEMPLATES[i % len(TEMPLATES)]
        i += 1
        text = pattern.format(
            n=1000 + len(rows),
            day=rng.choice(DAYS),
            plan=rng.choice(PLANS),
            product=rng.choice(PRODUCTS),
            mins=rng.choice([10, 20, 45]),
            seats=rng.choice([50, 200, 800]),
        )
        rows.append({
            "id": "m1-%04d" % (len(rows) + 1),
            "state": {"subject": "%s request %d" % (dept, len(rows) + 1), "body": text},
            "gold": {
                "department": dept,
                "urgency": urgency,
                "churn_risk": churn,
                "refund_requested": refund,
            },
        })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=500)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    if not args.out:
        args.out = os.path.join(_paths.DATA, "seed_500.jsonl")
    rows = generate(args.n)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(args.out, len(rows))


if __name__ == "__main__":
    main()
