"""RL self-training of the Laya decision head.

The INT8 encoder stays frozen. Updates follow Laya's RLCD loop: sample a group
of noisy logit policies, score them with a strictly proper reward, and apply a
GRPO-style advantage. Soft cross-entropy keeps the head on the filtered target.
"""
import os

import torch

from laya.agent import Agent
from laya.common import QTYPES, build_sequence, collate_items, proper_reward

from runtime import HEAD_PATH, STATE_DIR

HEAD_PREFIXES = ("head.", "type_emb.", "scorer.", "act_head.")


def head_parameters(model):
    return [p for n, p in model.named_parameters() if n.startswith(HEAD_PREFIXES) and p.requires_grad]


def save_head(model, steps):
    os.makedirs(STATE_DIR, exist_ok=True)
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items() if k.startswith(HEAD_PREFIXES)}
    torch.save({"steps": steps, "state_dict": sd}, HEAD_PATH)


def _items_for(agent, record, questions):
    items = []
    max_len = agent.cfg.get("max_len", 512)
    head_max_len = agent.cfg.get("head_max_len", 192)
    for qid, qdef in questions.items():
        if qid not in record["targets"]:
            continue
        q = Agent._to_internal(qdef)
        seq, markers = build_sequence(agent.tok, record["state"], q, max_len, head_max_len)
        if len(markers) != len(record["targets"][qid]):
            continue
        items.append({
            "ids": seq,
            "markers": markers,
            "qtype": QTYPES[q["t"]],
            "target": record["targets"][qid],
            "qid": qid,
            "rid": record.get("id"),
        })
    return items


def _encode(model, tok, items):
    model.encoder.eval()
    batch = collate_items([items], tok.pad_token_id)
    with torch.no_grad():
        hidden = model.encoder(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
        ).last_hidden_state
    return hidden, batch


def _head_forward(model, hidden, batch):
    h = hidden + model.type_emb(batch["qtype"])[:, None, :]
    if model.head is not None:
        pad = ~batch["attention_mask"].bool()
        for layer in model.head.layers:
            h = layer(h, src_key_padding_mask=pad)
    idx = batch["marker_pos"].clamp(min=0)[:, :, None].expand(-1, -1, h.size(-1))
    logits = model.scorer(torch.gather(h, 1, idx)).squeeze(-1).float()
    return logits.masked_fill(~batch["marker_mask"], -1e4)


def _reward(model, hidden, batch):
    model.eval()
    with torch.no_grad():
        logits = _head_forward(model, hidden, batch)
        mask = batch["marker_mask"]
        q = torch.softmax(logits, -1) * mask
        q = q / q.sum(-1, keepdim=True).clamp_min(1e-9)
        r = proper_reward(q, batch["target"], batch["qtype"], mask, w_sph=0.75, w_rps=1.0)
    return float(r.mean())


def train_head(agent, records, questions, steps=8, group_size=4, lr=1e-4, sigma=0.3):
    items = []
    for rec in records:
        items.extend(_items_for(agent, rec, questions))
    if not items:
        raise SystemExit("no trainable questions after filtering")

    model = agent.model
    for p in model.encoder.parameters():
        p.requires_grad = False
    hidden, batch = _encode(model, agent.tok, items)
    before = _reward(model, hidden, batch)

    params = head_parameters(model)
    if not params:
        raise SystemExit("decision head has no trainable parameters")
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.01)
    model.head.train()
    model.type_emb.train()
    model.scorer.train()
    model.act_head.train()
    model.encoder.eval()

    n = hidden.size(0)
    last = None
    for step in range(steps):
        pick = torch.randint(0, n, (min(8, n),))
        h = hidden[pick]
        sub = {k: batch[k][pick] for k in ("attention_mask", "marker_pos", "marker_mask", "qtype", "target")}
        logits = _head_forward(model, h, sub)
        mask = sub["marker_mask"]
        k = mask.sum(-1, keepdim=True).float().clamp_min(2)
        target = sub["target"]

        eps = torch.randn((group_size,) + logits.shape) * sigma * mask
        eps = (eps - eps.sum(-1, keepdim=True) / k) * mask
        z = logits.detach().unsqueeze(0) + eps
        q = torch.softmax(z.masked_fill(~mask, -1e4), -1)
        with torch.no_grad():
            r = proper_reward(q, target.unsqueeze(0), sub["qtype"], mask, w_sph=0.75, w_rps=1.0)
            adv = r - r.mean(0, keepdim=True)
            adv = adv / (adv.std() + 1e-6)
        logp = -(((z - logits.unsqueeze(0)) ** 2) * mask).sum(-1) / (2 * sigma ** 2)
        loss_rl = -(adv * logp).mean()
        loss_ce = -(target * torch.log_softmax(logits, -1)).sum(-1).mean()
        loss = loss_rl + loss_ce
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        last = (float(loss.detach()), float(r.detach().mean()))
        print("  step %d  loss=%.3f  reward=%.3f" % (step + 1, last[0], last[1]), flush=True)

    model.eval()
    after = _reward(model, hidden, batch)
    prev = 0
    if os.path.exists(HEAD_PATH):
        prev = int(torch.load(HEAD_PATH, map_location="cpu", weights_only=False).get("steps", 0))
    save_head(model, prev + steps)
    return {"questions": len(items), "steps": steps, "reward_before": before, "reward_after": after, "last_loss": last[0]}
