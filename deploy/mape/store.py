"""JSONL event store, bucketed by decision type, label space, and language."""
import json
import os
import re

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import paths as _paths
ROOT = _paths.STATE
EVENTS = os.path.join(ROOT, "events.jsonl")
METRICS = os.path.join(ROOT, "metrics.jsonl")
RELEASE = os.path.join(ROOT, "release.json")
TRAIN = os.path.join(ROOT, "flywheel_train.jsonl")
BASELINE = os.path.join(ROOT, "baseline.json")


def _slug(text):
    s = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return (s or "na")[:48]


def bucket_path(event):
    return os.path.join(
        ROOT, "buckets",
        _slug(event["decision_type"]),
        _slug(event["label_space"]),
        _slug(event["language"]),
        "events.jsonl",
    )


def _append(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def append_event(event):
    os.makedirs(ROOT, exist_ok=True)
    _append(EVENTS, event)
    _append(bucket_path(event), event)


def load_events():
    if not os.path.exists(EVENTS):
        return []
    rows = []
    with open(EVENTS) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def save_events(rows):
    os.makedirs(ROOT, exist_ok=True)
    with open(EVENTS, "w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def update_event(event_id, **fields):
    rows = load_events()
    found = None
    for row in rows:
        if row["id"] == event_id:
            row.update(fields)
            found = row
            break
    if found is None:
        raise SystemExit("unknown event %s" % event_id)
    save_events(rows)
    _append(bucket_path(found), found)
    return found


def append_metrics(row):
    _append(METRICS, row)


def load_metrics():
    if not os.path.exists(METRICS):
        return []
    with open(METRICS) as f:
        return [json.loads(line) for line in f if line.strip()]


def read_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
