"""Screen a decision corpus before self-training.

Drops empty, non-Latin, and near-duplicate states. Gold labels are kept.
Unlabeled rows are kept only when the frozen model is confident enough to
serve as a pseudo-label.
"""
import hashlib
import json
import re

from laya.lang import detect_script, state_text

_SPACE = re.compile(r"\s+")


def _norm(state):
    return _SPACE.sub(" ", state_text(state).lower()).strip()


def _jaccard(a, b):
    if not a or not b:
        return 0.0
    sa, sb = set(a.split()), set(b.split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def structural_filter(records, min_chars=24, dup_jaccard=0.9):
    kept, rejected = [], []
    seen = []
    for rec in records:
        text = _norm(rec.get("state", ""))
        script = detect_script(text)
        if script not in ("latin", "unknown"):
            rejected.append({**rec, "reason": "non_latin:%s" % script})
            continue
        if len(text) < min_chars:
            rejected.append({**rec, "reason": "too_short"})
            continue
        digest = hashlib.sha1(text.encode()).hexdigest()
        if any(digest == prev[0] or _jaccard(text, prev[1]) >= dup_jaccard for prev in seen):
            rejected.append({**rec, "reason": "duplicate"})
            continue
        seen.append((digest, text))
        kept.append(rec)
    return kept, rejected


def _hard_target(qdef, answer):
    kind = qdef["type"]
    if kind == "choice":
        keys = list(qdef["criteria"].keys())
        idx = keys.index(answer["choice"])
        target = [0.0] * len(keys)
        target[idx] = 1.0
        return target
    if kind == "score":
        k = len(qdef["criteria"])
        idx = max(range(k), key=lambda i: answer["probabilities"][str(i)])
        target = [0.0] * k
        target[idx] = 1.0
        return target
    yes = 1.0 if answer["noul"] >= 0.5 else 0.0
    return [1.0 - yes, yes]


def gold_target(qdef, gold):
    kind = qdef["type"]
    if kind == "choice":
        keys = list(qdef["criteria"].keys())
        if gold not in keys:
            raise KeyError(gold)
        target = [0.0] * len(keys)
        target[keys.index(gold)] = 1.0
        return target
    if kind == "score":
        k = len(qdef["criteria"])
        idx = int(round(float(gold)))
        if not 0 <= idx < k:
            raise ValueError(gold)
        target = [0.0] * k
        target[idx] = 1.0
        return target
    yes = 1.0 if gold in (True, 1, "1", "true", "yes") else 0.0
    return [1.0 - yes, yes]


def label_records(agent, records, questions, min_conf):
    """Attach per-question targets. Gold wins. Otherwise keep a confident pseudo-label."""
    accepted, review = [], []
    for rec in records:
        gold = rec.get("gold") or {}
        pred = None
        targets = {}
        confs = {}
        if gold:
            for qid, qdef in questions.items():
                if qid in gold:
                    targets[qid] = gold_target(qdef, gold[qid])
                    confs[qid] = 1.0
        else:
            pred = agent.predict(rec["state"], questions)
            for qid, qdef in questions.items():
                ans = pred["answers"][qid]
                confs[qid] = ans["confidence"]
                if ans["confidence"] >= min_conf:
                    targets[qid] = _hard_target(qdef, ans)
        if not targets:
            review.append({**rec, "reason": "low_confidence", "confidence": confs, "pred": pred})
            continue
        accepted.append({**rec, "targets": targets, "confidence": confs, "source": "gold" if gold else "pseudo"})
    return accepted, review
