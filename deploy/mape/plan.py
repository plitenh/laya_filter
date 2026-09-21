"""Plan: decide whether a regression job should run, and write its JSONL."""
import json

from .store import BASELINE, TRAIN, load_metrics, read_json


def trainable(events):
    """Human final decisions only. Wide choice spaces are refused, not flattened."""
    rows = []
    for event in events:
        if not event.get("human"):
            continue
        if "label_space_too_wide" in event["signals"]:
            continue
        rows.append(event)
    return rows


def triggers(events, report):
    """Any one of: volume, ECE drift, correction rate."""
    reasons = []
    baseline = read_json(BASELINE, {"questions": max(1, len(events))})
    labeled = trainable(events)
    need = max(3, int(round(0.10 * baseline["questions"])))
    if len(labeled) >= need:
        reasons.append("volume:%d>=%d" % (len(labeled), need))
    history = load_metrics()
    if history:
        prev = history[-1].get("by_type", {})
        for dtype, cur in report.items():
            old = (prev.get(dtype) or {}).get("ece")
            if old is not None and cur["ece"] is not None and cur["ece"] > old + 0.02:
                reasons.append("ece:%s +%.3f" % (dtype, cur["ece"] - old))
    for dtype, cur in report.items():
        if cur["n"] >= 8 and cur["correction_rate"] > 0.05:
            reasons.append("corrections:%s %.1f%%" % (dtype, 100 * cur["correction_rate"]))
    return reasons


def build_dataset(events):
    rows = trainable(events)
    with open(TRAIN, "w") as f:
        for row in rows:
            f.write(json.dumps({
                "id": row["id"],
                "state": row["state"],
                "question_id": row["question_id"],
                "question": row["question"],
                "target": row["human"]["value"],
            }, ensure_ascii=False) + "\n")
    return rows
