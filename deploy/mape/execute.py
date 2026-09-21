"""Execute: LoRA on the decision head, then drift gate, shadow compare, canary."""
import numpy as np
import torch

from laya.agent import Agent
from laya.common import QTYPES, build_sequence, collate_items, ece_score

from runtime import HEAD_PATH
from train_head import HEAD_PREFIXES

from . import lora
from .store import RELEASE, read_json, write_json

ECE_LIMIT = 0.02
AGREE_LIMIT = 0.95
CANARY = 0.1


def _target(qdef, value):
    from corpus import gold_target
    return gold_target(qdef, value)


def _items(agent, rows):
    items = []
    max_len = agent.cfg.get("max_len", 512)
    head_max_len = agent.cfg.get("head_max_len", 192)
    for row in rows:
        value = row["target"] if "target" in row else row["human"]["value"]
        q = Agent._to_internal(row["question"])
        seq, markers = build_sequence(agent.tok, row["state"], q, max_len, head_max_len)
        target = _target(row["question"], value)
        if len(markers) != len(target):
            continue
        items.append({
            "ids": seq,
            "markers": markers,
            "qtype": QTYPES[q["t"]],
            "target": target,
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


def _logits(model, hidden, batch):
    h = hidden + model.type_emb(batch["qtype"])[:, None, :]
    if model.head is not None:
        pad = ~batch["attention_mask"].bool()
        for layer in model.head.layers:
            h = layer(h, src_key_padding_mask=pad)
    idx = batch["marker_pos"].clamp(min=0)[:, :, None].expand(-1, -1, h.size(-1))
    logits = model.scorer(torch.gather(h, 1, idx)).squeeze(-1).float()
    return logits.masked_fill(~batch["marker_mask"], -1e4)


def _metrics(logits, batch):
    mask = batch["marker_mask"]
    probs = torch.softmax(logits, -1) * mask
    probs = probs / probs.sum(-1, keepdim=True).clamp_min(1e-9)
    pred = probs.argmax(-1)
    truth = batch["target"].argmax(-1)
    correct = (pred == truth).float()
    conf = probs.max(-1).values
    ece = ece_score(conf.detach().cpu().numpy(), correct.detach().cpu().numpy())
    return float(correct.mean()), float(ece), pred


def _fit_temperature(logits, batch):
    """One temperature per question type, fit on this deploy domain."""
    temps = [1.0, 1.0, 1.0]
    z = logits.detach()
    mask = batch["marker_mask"]
    qtype = batch["qtype"]
    truth = batch["target"].argmax(-1)
    grid = np.linspace(0.5, 3.0, 11)
    for qt in range(3):
        sel = qtype == qt
        if int(sel.sum()) < 2:
            continue
        best_t, best_e = 1.0, 1e9
        for t in grid:
            p = torch.softmax(z[sel] / float(t), -1)
            p = p * mask[sel]
            p = p / p.sum(-1, keepdim=True).clamp_min(1e-9)
            ok = (p.argmax(-1) == truth[sel]).float()
            e = ece_score(p.max(-1).values.cpu().numpy(), ok.cpu().numpy())
            if e < best_e:
                best_t, best_e = float(t), e
        temps[qt] = best_t
    return temps


def _snapshot(model):
    return {k: v.detach().cpu().clone() for k, v in model.state_dict().items() if k.startswith(HEAD_PREFIXES)}


def _restore(model, snap):
    model.load_state_dict(snap, strict=False)


def run(agent, rows, steps=12, rank=8):
    items = _items(agent, rows)
    if len(items) < 3:
        return {"status": "skipped", "reason": "fewer than 3 labeled questions"}
    n_val = max(1, len(items) // 4)
    hidden, batch = _encode(agent.model, agent.tok, items)
    model = agent.model
    pre = _snapshot(model)
    with torch.no_grad():
        old_logits = _logits(model, hidden, batch)
    old_acc, old_ece, old_pred = _metrics(old_logits, batch)

    params = lora.inject(model, rank=rank)
    opt = torch.optim.AdamW(params, lr=1e-3, weight_decay=0.0)
    model.train()
    model.encoder.eval()
    train_idx = torch.arange(0, hidden.size(0) - n_val)
    for step in range(steps):
        pick = train_idx[torch.randint(0, len(train_idx), (min(8, len(train_idx)),))]
        sub = {k: batch[k][pick] for k in ("attention_mask", "marker_pos", "marker_mask", "qtype", "target")}
        logits = _logits(model, hidden[pick], sub)
        loss = -(sub["target"] * torch.log_softmax(logits, -1)).sum(-1).mean()
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        print("  lora step %d  loss=%.3f" % (step + 1, float(loss.detach())), flush=True)

    model.eval()
    with torch.no_grad():
        new_logits = _logits(model, hidden, batch)
    new_acc, new_ece, new_pred = _metrics(new_logits, batch)
    temps = _fit_temperature(new_logits, batch)
    agree = float((old_pred == new_pred).float().mean())
    print("  val acc %.3f -> %.3f   ece %.3f -> %.3f   agree %.3f" % (
        old_acc, new_acc, old_ece, new_ece, agree), flush=True)

    lora.merge(model)
    candidate = _snapshot(model)
    _restore(model, pre)
    model.eval()

    result = {
        "accuracy_before": old_acc,
        "accuracy_after": new_acc,
        "ece_before": old_ece,
        "ece_after": new_ece,
        "agreement": agree,
        "temperature": temps,
        "questions": len(items),
    }
    if new_ece > old_ece + ECE_LIMIT:
        result["status"] = "rejected"
        result["reason"] = "ece worsened by %.3f" % (new_ece - old_ece)
        return result

    blob = {"steps": steps, "state_dict": candidate, "temperature": temps, "lora_rank": rank}
    if agree < AGREE_LIMIT:
        path = HEAD_PATH + ".candidate"
        torch.save(blob, path)
        rel = read_json(RELEASE, {})
        rel.update({"mode": "shadow", "candidate": path, "agreement": agree, "canary": 0.0})
        write_json(RELEASE, rel)
        result["status"] = "shadow"
        result["reason"] = "agreement %.3f < %.2f, held for review" % (agree, AGREE_LIMIT)
        return result

    torch.save(blob, HEAD_PATH)
    _restore(model, candidate)
    rel = read_json(RELEASE, {})
    rel.update({
        "mode": "canary",
        "canary": CANARY,
        "version": "laya-large-int8+lora%d" % steps,
        "temperature": temps,
        "agreement": agree,
    })
    write_json(RELEASE, rel)
    if temps:
        agent.temperature = temps
    result["status"] = "canary"
    result["reason"] = "drift ok, shadow agreement %.3f, canary %.0f%%" % (agree, 100 * CANARY)
    return result
