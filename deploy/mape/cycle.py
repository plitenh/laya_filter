"""One MAPE-K turn: Monitor is fed by predict; this runs Analyze, Plan, Execute."""
import json

from corpus import structural_filter

from .analyze import summarize
from .execute import run as execute
from .monitor import record
from .plan import build_dataset, triggers
from .store import BASELINE, append_metrics, load_events, read_json, write_json

from runtime import load_agent, questions_for


def seed(agent, path, preset="default"):
    """Run Laya over a corpus and treat gold labels as the operator's final decision."""
    questions = questions_for(preset)
    rows = []
    with open(path) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    kept, rejected = structural_filter(rows)
    labeled = 0
    for rec in kept:
        result = agent.predict(rec["state"], questions)
        record(rec["state"], questions, result, human=rec.get("gold"))
        if rec.get("gold"):
            labeled += len(rec["gold"])
    base = read_json(BASELINE, {"questions": 0})
    base["questions"] = max(base["questions"], labeled)
    write_json(BASELINE, base)
    return {"kept": len(kept), "rejected": len(rejected), "labeled_questions": labeled}


def cycle(agent=None, steps=12):
    events = load_events()
    report = summarize(events)
    reasons = triggers(events, report)
    dataset = build_dataset(events) if reasons else []
    print("analyze", json.dumps(report, ensure_ascii=False), flush=True)
    print("plan", reasons or ["no trigger"], "train", len(dataset), flush=True)
    execution = {"status": "idle"}
    if reasons and dataset:
        if agent is None:
            agent = load_agent()
        execution = execute(agent, dataset, steps=steps)
        print("execute", execution["status"], execution.get("reason", ""), flush=True)
    append_metrics({"by_type": report, "triggers": reasons, "execution": execution.get("status")})
    return {"analyze": report, "triggers": reasons, "execute": execution}
