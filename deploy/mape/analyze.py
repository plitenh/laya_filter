"""Analyze: ECE and accuracy by decision type. High-ECE buckets are the regression targets."""
import numpy as np

from laya.common import ece_score

from .store import load_events


def _correct(event):
    if not event.get("human"):
        return None
    return event["prediction"] == event["human"]["value"]


def summarize(events=None):
    events = load_events() if events is None else events
    by_type = {}
    for event in events:
        bucket = by_type.setdefault(event["decision_type"], [])
        bucket.append(event)
    report = {}
    for dtype, rows in by_type.items():
        labeled = [r for r in rows if _correct(r) is not None]
        conf = np.array([r["confidence"] for r in labeled], dtype=np.float64)
        ok = np.array([1.0 if _correct(r) else 0.0 for r in labeled], dtype=np.float64)
        corrections = sum(1 for r in rows if "human_correction" in r["signals"])
        report[dtype] = {
            "n": len(rows),
            "labeled": len(labeled),
            "accuracy": float(ok.mean()) if len(ok) else None,
            "ece": float(ece_score(conf, ok)) if len(ok) else None,
            "correction_rate": corrections / len(rows) if rows else 0.0,
            "low_confidence": sum(1 for r in rows if "low_confidence" in r["signals"]),
            "flat": sum(1 for r in rows if "flat" in r["signals"]),
            "wide_label_space": sum(1 for r in rows if "label_space_too_wide" in r["signals"]),
        }
    return report
