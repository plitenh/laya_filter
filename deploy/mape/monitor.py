"""Monitor: keep every Laya decision, and flag the three collection signals."""
import math
import uuid
from datetime import datetime, timezone

import numpy as np

from laya.lang import detect_script, guess_latin_language, state_text

from .store import append_event, load_events

FLAT_ENTROPY = 0.6
DEFAULT_P10 = 0.35
MAX_CHOICE_OPTIONS = 20


def model_version():
    from .store import RELEASE, read_json
    rel = read_json(RELEASE, {})
    return rel.get("version", "laya-large-int8")


def _entropy(probs):
    p = np.array([float(v) for v in probs.values()], dtype=np.float64)
    if p.size < 2 or p.sum() <= 0:
        return 0.0
    p = p / p.sum()
    ent = -(p * np.log(np.clip(p, 1e-12, 1.0))).sum()
    return float(ent / math.log(p.size))


def _p10(decision_type):
    vals = [e["confidence"] for e in load_events() if e["decision_type"] == decision_type]
    if len(vals) < 10:
        return DEFAULT_P10
    return float(np.quantile(vals, 0.1))


def _language(state):
    text = state_text(state)
    script = detect_script(text)
    if script not in ("latin", "unknown"):
        return script
    return guess_latin_language(text) or "en"


def _prediction(answer):
    if answer["type"] == "choice":
        return answer["choice"]
    if answer["type"] == "score":
        return int(round(answer["score"]))
    return bool(answer["noul"] >= 0.5)


def _label_space(qdef):
    crit = qdef.get("criteria")
    if isinstance(crit, dict):
        return "|".join(crit.keys())
    if isinstance(crit, list):
        return "levels:%d" % len(crit)
    return "bool"


def record(state, questions, result, human=None):
    """Persist one event per question. Returns the new event ids."""
    version = result.get("model_version") or model_version()
    lang = _language(state)
    ids = []
    for qid, qdef in questions.items():
        answer = result["answers"][qid]
        probs = answer.get("probabilities") or {"false": 1 - answer["noul"], "true": answer["noul"]}
        entropy = _entropy(probs)
        confidence = float(answer["confidence"])
        pred = _prediction(answer)
        signals = []
        if confidence < _p10(answer["type"]):
            signals.append("low_confidence")
        if answer["type"] == "choice" and entropy >= FLAT_ENTROPY:
            signals.append("flat")
        n_opt = len(qdef.get("criteria") or [])
        if answer["type"] == "choice" and n_opt > MAX_CHOICE_OPTIONS:
            signals.append("label_space_too_wide")
        final = None if human is None or qid not in human else human[qid]
        if final is not None and final != pred:
            signals.append("human_correction")
        event = {
            "id": uuid.uuid4().hex[:12],
            "ts": datetime.now(timezone.utc).isoformat(),
            "model_version": version,
            "state": state,
            "question_id": qid,
            "question": qdef,
            "decision_type": answer["type"],
            "label_space": _label_space(qdef),
            "n_options": n_opt if answer["type"] == "choice" else 2,
            "language": lang,
            "probs": probs,
            "confidence": confidence,
            "entropy": round(entropy, 4),
            "prediction": pred,
            "signals": signals,
            "human": None if final is None else {"value": final, "ts": datetime.now(timezone.utc).isoformat()},
        }
        append_event(event)
        ids.append(event["id"])
    return ids
