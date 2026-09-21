#!/usr/bin/env python3
"""MAPE-K flywheel around the resident Laya model."""
import argparse
import json
import sys

import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.dirname(__file__))

from mape.cycle import cycle, seed
from mape.monitor import record
from mape.store import update_event
from runtime import load_agent, questions_for


def main():
    parser = argparse.ArgumentParser(description="Laya MAPE-K flywheel")
    parser.add_argument("--seed", help="corpus JSONL; gold is stored as the human final decision")
    parser.add_argument("--preset", default="default")
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--correct", nargs=2, metavar=("EVENT", "VALUE"), help="human correction")
    args = parser.parse_args()
    if args.correct:
        event_id, raw = args.correct
        value = json.loads(raw) if raw[:1] in "[{0123456789tfn-" else raw
        if raw in ("true", "false"):
            value = raw == "true"
        signals = None
        row = update_event(event_id, human={"value": value})
        if row["prediction"] != value and "human_correction" not in row["signals"]:
            signals = list(row["signals"]) + ["human_correction"]
            row = update_event(event_id, signals=signals)
        print(json.dumps({"corrected": event_id, "value": value}, ensure_ascii=False))
        return
    agent = None
    if args.seed:
        print("monitor: seeding from", args.seed, flush=True)
        agent = load_agent()
        print(json.dumps(seed(agent, args.seed, args.preset), ensure_ascii=False), flush=True)
    summary = cycle(agent, steps=args.steps)
    json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
