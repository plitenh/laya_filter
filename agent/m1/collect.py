#!/usr/bin/env python3
"""Collect Laya decisions. Low-confidence rows enter the pool; disagreements are corrections."""
import argparse
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import paths as _paths
sys.path.insert(0, _paths.DEPLOY)
sys.path.insert(0, os.path.join(_paths.AGENT, "m1"))

from laya.agent import Agent
from laya.common import QTYPES, build_sequence, collate_items, confidence_from_probs, temp_bucket
from runtime import load_agent
from schema import QUESTIONS, option_count
from boundary import write_boundary

OUT = _paths.OUT
CHUNK = 16


def _read(path):
    rows = []
    with open(path) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _predict_chunk(agent, states, questions):
    """Same scoring as Agent.predict, several states in one forward."""
    items, meta = [], []
    max_len = agent.cfg.get("max_len", 512)
    head_max_len = agent.cfg.get("head_max_len", 192)
    qids = list(questions.keys())
    for state in states:
        for qid in qids:
            q = Agent._to_internal(questions[qid])
            seq, markers = build_sequence(agent.tok, state, q, max_len, head_max_len)
            if len(markers) != option_count(questions[qid]):
                raise ValueError("question %s exceeds the head budget" % qid)
            items.append({"ids": seq, "markers": markers, "qtype": QTYPES[q["t"]]})
            meta.append((qid, q))
    batch = collate_items([items], agent.tok.pad_token_id)
    with torch.no_grad():
        logits, _act = agent.model(
            batch["input_ids"],
            batch["attention_mask"],
            batch["marker_pos"],
            batch["marker_mask"],
            batch["qtype"],
        )
    logits = logits.float().cpu().numpy()
    per_state = [{} for _ in states]
    nq = len(qids)
    for r, (qid, q) in enumerate(meta):
        si = r // nq
        k = len(items[r]["markers"])
        qt = QTYPES[q["t"]]
        scale = agent.temperature_by_options.get(temp_bucket(qt, k), agent.temperature[qt])
        z = logits[r, :k] / max(1e-3, float(scale))
        p = np.exp(z - z.max())
        p = p / p.sum()
        conf = round(float(confidence_from_probs(p, k)), 4)
        if q["t"] == "choice":
            keys = list(q["crit"].keys())
            packed = {
                "type": "choice",
                "prediction": keys[int(p.argmax())],
                "probabilities": {kk: round(float(v), 4) for kk, v in zip(keys, p)},
            }
        elif q["t"] == "score":
            score = float((np.arange(k) * p).sum())
            packed = {
                "type": "score",
                "prediction": int(round(score)),
                "score": round(score, 4),
                "probabilities": {str(i): round(float(v), 4) for i, v in enumerate(p)},
            }
        else:
            packed = {
                "type": "noul",
                "prediction": bool(float(p[1]) >= 0.5),
                "noul": round(float(p[1]), 4),
                "probabilities": {"false": round(float(p[0]), 4), "true": round(float(p[1]), 4)},
            }
        packed["confidence"] = conf
        packed["options"] = k
        per_state[si][qid] = packed
    return per_state


def _gold_match(answer, gold):
    if answer["type"] == "choice":
        return answer["prediction"] == gold
    if answer["type"] == "score":
        return int(answer["prediction"]) == int(gold)
    return bool(answer["prediction"]) == bool(gold)


def collect(agent, rows, questions, out_dir=OUT):
    os.makedirs(out_dir, exist_ok=True)
    preds = []
    states = [row["state"] for row in rows]
    for start in range(0, len(states), CHUNK):
        preds.extend(_predict_chunk(agent, states[start:start + CHUNK], questions))
        print("collected %d/%d" % (min(start + CHUNK, len(states)), len(states)), flush=True)

    samples = []
    for i, (row, answers) in enumerate(zip(rows, preds), 1):
        gold = row.get("gold") or {}
        packed = {}
        for qid, ans in answers.items():
            g = gold.get(qid)
            correct = None if g is None else _gold_match(ans, g)
            packed[qid] = dict(ans, gold=g, correct=correct, human_correction=bool(correct is False))
        samples.append({
            "id": row.get("id", "s%04d" % i),
            "state": row["state"],
            "gold": gold,
            "answers": packed,
        })

    flat = [a for s in samples for a in s["answers"].values()]
    buckets = {}
    for ans in flat:
        buckets.setdefault(ans["type"], []).append(ans["confidence"])
    p10 = {k: float(np.quantile(v, 0.1)) for k, v in buckets.items()}

    pool, corrections = [], []
    for sample in samples:
        low = [qid for qid, ans in sample["answers"].items() if ans["confidence"] < p10[ans["type"]]]
        for qid, ans in sample["answers"].items():
            if ans["human_correction"]:
                corrections.append({
                    "id": sample["id"],
                    "question_id": qid,
                    "state": sample["state"],
                    "prediction": ans["prediction"],
                    "gold": ans["gold"],
                    "confidence": ans["confidence"],
                    "signal": "human_correction",
                })
        if low:
            pool.append({
                "id": sample["id"],
                "state": sample["state"],
                "low_confidence": low,
                "answers": sample["answers"],
            })

    def dump(name, payload):
        path = os.path.join(out_dir, name)
        with open(path, "w") as f:
            for row in payload:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        return path

    samples_path = dump("samples.jsonl", samples)
    dump("pool.jsonl", pool)
    dump("corrections.jsonl", corrections)
    with open(os.path.join(out_dir, "p10.json"), "w") as f:
        json.dump(p10, f, indent=2)
    doc = write_boundary(samples_path, os.path.join(out_dir, "decision_boundary.md"))
    return {
        "labeled": len(samples),
        "pool": len(pool),
        "corrections": len(corrections),
        "p10": p10,
        "boundary": doc,
    }


def main():
    parser = argparse.ArgumentParser(description="Milestone 1 Laya sample collector")
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--out", default=OUT)
    args = parser.parse_args()
    print("loading Laya...", flush=True)
    agent = load_agent()
    summary = collect(agent, _read(args.corpus), QUESTIONS, args.out)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
