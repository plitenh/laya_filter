"""Load the persisted INT8 Laya-large agent, quantizing once if needed."""
import json
import os

import torch
import torch.nn as nn

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import paths as _paths
ROOT = _paths.MODELS
INT8_PATH = os.path.join(ROOT, "model.int8.pt")
STATE_DIR = _paths.STATE
HEAD_PATH = os.path.join(STATE_DIR, "head.pt")
HOST = "127.0.0.1"
PORT = 8765

DEFAULT_QUESTIONS = {
    "department": {
        "type": "choice",
        "instructions": "Which department should handle this request?",
        "criteria": {
            "billing": "invoices, payments, refunds",
            "technical": "bugs, outages, system errors",
            "sales": "pricing, new contracts",
            "other": "everything else",
        },
    },
    "urgency": {
        "type": "score",
        "instructions": "How urgent is this request?",
        "criteria": ["not urgent", "soon", "critical deadline or blocking issue"],
    },
    "churn_risk": {
        "type": "noul",
        "instructions": "Does the user threaten to cancel or leave?",
    },
    "refund_requested": {
        "type": "noul",
        "instructions": "Does the user explicitly request a refund?",
    },
}


def questions_for(preset):
    import laya

    if not preset or preset == "default":
        return DEFAULT_QUESTIONS
    if preset == "triage":
        return laya.triage_questions()
    if preset == "email":
        return laya.email_questions()
    if preset == "guard":
        return laya.guard_questions()
    if preset == "moderation":
        return laya.moderation_questions()
    raise SystemExit(f"unknown preset {preset!r} (default, triage, email, guard, moderation)")


def _attach(model):
    from laya.agent import Agent, _fix_tokenizer_config
    from transformers import AutoTokenizer

    _fix_tokenizer_config(ROOT)
    agent = object.__new__(Agent)
    with open(os.path.join(ROOT, "rl_agent_config.json")) as f:
        agent.cfg = json.load(f)
    agent.tok = AutoTokenizer.from_pretrained(os.path.join(ROOT, "tokenizer"))
    agent.model = model
    agent.device = torch.device("cpu")
    agent.dtype = torch.float32
    agent.temperature = agent.cfg.get("temperature", [1.0, 1.0, 1.0])
    agent.temperature_by_options = agent.cfg.get("temperature_by_options", {})
    return agent


def quantize_and_save():
    from torch.ao.quantization import quantize_dynamic
    import laya

    print("quantizing Laya-large encoder to INT8 (one time)...", flush=True)
    agent = laya.load(ROOT, device="cpu")
    agent.model.encoder = quantize_dynamic(agent.model.encoder, {nn.Linear}, dtype=torch.qint8)
    agent.model.eval()
    torch.save(agent.model, INT8_PATH)
    print(f"saved {INT8_PATH}", flush=True)
    return agent


def apply_saved_head(agent):
    """Overlay a self-trained decision head onto the frozen INT8 encoder."""
    if not os.path.exists(HEAD_PATH):
        return 0
    blob = torch.load(HEAD_PATH, map_location="cpu", weights_only=False)
    sd = blob["state_dict"]
    keep = ("head.", "type_emb.", "scorer.", "act_head.")
    sd = {k: v for k, v in sd.items() if k.startswith(keep)}
    params = dict(agent.model.named_parameters())
    buffers = dict(agent.model.named_buffers())
    with torch.no_grad():
        for key, value in sd.items():
            if key in params and params[key].shape == value.shape:
                params[key].copy_(value)
            elif key in buffers and buffers[key].shape == value.shape:
                buffers[key].copy_(value)
    if blob.get("temperature"):
        agent.temperature = blob["temperature"]
    return int(blob.get("steps", 0))


def load_agent():
    torch.set_num_threads(int(os.environ.get("LAYA_THREADS", "8")))
    if not os.path.exists(INT8_PATH):
        agent = quantize_and_save()
    else:
        model = torch.load(INT8_PATH, map_location="cpu", weights_only=False)
        model.eval()
        agent = _attach(model)
    apply_saved_head(agent)
    agent.model.eval()
    return agent
