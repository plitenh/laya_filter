"""Build a complete study pack + quiz from the collected Laya sample pool."""
import json
import os
import random
import sys
from collections import defaultdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import paths as _paths
sys.path.insert(0, os.path.join(_paths.AGENT, "m1"))

from schema import QUESTIONS, label_space

OUT = _paths.QUIZ


def _load(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def _state_text(state):
    if isinstance(state, str):
        return state
    if isinstance(state, dict):
        bits = []
        if state.get("subject"):
            bits.append("主题: %s" % state["subject"])
        if state.get("body"):
            bits.append("正文: %s" % state["body"])
        return "\n".join(bits) if bits else json.dumps(state, ensure_ascii=False)
    return json.dumps(state, ensure_ascii=False)


def _options(qid):
    q = QUESTIONS[qid]
    if q["type"] == "choice":
        return [{"key": k, "text": "%s — %s" % (k, v)} for k, v in q["criteria"].items()]
    if q["type"] == "score":
        return [{"key": str(i), "text": "%d — %s" % (i, c)} for i, c in enumerate(q["criteria"])]
    return [{"key": "false", "text": "否"}, {"key": "true", "text": "是"}]


def _canon(qid, value):
    q = QUESTIONS[qid]
    if q["type"] == "choice":
        return str(value)
    if q["type"] == "score":
        return str(int(value))
    if isinstance(value, bool):
        return "true" if value else "false"
    s = str(value).strip().lower()
    if s in ("1", "yes", "y", "true", "是"):
        return "true"
    return "false"


def _pick_examples(samples, qid, n_good=2, n_hard=2, rng=None):
    rng = rng or random.Random(0)
    good, hard = [], []
    for s in samples:
        ans = s["answers"][qid]
        if ans.get("gold") is None:
            continue
        item = {
            "id": s["id"],
            "text": _state_text(s["state"]),
            "gold": _canon(qid, ans["gold"]),
            "laya": _canon(qid, ans["prediction"]),
            "confidence": ans["confidence"],
            "agreed": bool(ans.get("correct")),
        }
        if ans.get("correct") and ans["confidence"] >= 0.2:
            good.append(item)
        elif ans.get("human_correction") or ans["confidence"] < 0.05:
            hard.append(item)
    rng.shuffle(good)
    rng.shuffle(hard)
    return good[:n_good], hard[:n_hard]


def _quiz_items(samples, per_qid=8, prefer_hard=True, rng=None):
    rng = rng or random.Random(1)
    by_qid = defaultdict(list)
    for s in samples:
        for qid, ans in s["answers"].items():
            if ans.get("gold") is None:
                continue
            by_qid[qid].append(s)
    items = []
    for qid, rows in by_qid.items():
        hard = [r for r in rows if r["answers"][qid].get("human_correction") or r["answers"][qid]["confidence"] < 0.05]
        easy = [r for r in rows if r not in hard]
        rng.shuffle(hard)
        rng.shuffle(easy)
        chosen = (hard if prefer_hard else []) + easy
        seen = set()
        for r in chosen:
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            ans = r["answers"][qid]
            items.append({
                "qid": "%s__%s" % (r["id"], qid),
                "sample_id": r["id"],
                "decision": qid,
                "type": QUESTIONS[qid]["type"],
                "prompt": QUESTIONS[qid]["instructions"],
                "material": _state_text(r["state"]),
                "options": _options(qid),
                "answer_key": _canon(qid, ans["gold"]),
                "laya_prediction": _canon(qid, ans["prediction"]),
                "laya_confidence": ans["confidence"],
                "was_correction": bool(ans.get("human_correction")),
            })
            if sum(1 for it in items if it["decision"] == qid) >= per_qid:
                break
    rng.shuffle(items)
    return items


def write_pack(samples_path, out_dir=OUT, per_qid=8):
    os.makedirs(out_dir, exist_ok=True)
    samples = _load(samples_path)
    rng = random.Random(42)

    # --- 完整资料：讲义 ---
    lines = [
        "# 客服决策批阅讲义",
        "",
        "根据已收集的 Laya 样本整理。先读规则与例题，再答 `exam.jsonl`。",
        "",
        "## 总规则",
        "",
        "1. 只根据给定原文判断，不要脑补。",
        "2. choice 只能选标签空间内的一项；score 选 0/1/2；noul 答 true/false。",
        "3. 与 Laya 不一致时，以讲义规则为准；你的答案会覆盖模型。",
        "",
    ]
    for qid, qdef in QUESTIONS.items():
        good, hard = _pick_examples(samples, qid, rng=rng)
        lines += [
            "## %s（%s）" % (qid, qdef["type"]),
            "",
            "题干：%s" % qdef["instructions"],
            "",
            "选项：",
        ]
        for opt in _options(qid):
            lines.append("- `%s` %s" % (opt["key"], opt["text"].split(" — ", 1)[-1] if " — " in opt["text"] else opt["text"]))
        lines += ["", "### 标准例", ""]
        for ex in good:
            lines += [
                "- **%s**" % ex["id"],
                "",
                "  %s" % ex["text"].replace("\n", "\n  "),
                "",
                "  标准答案：`%s`（Laya=%s, conf=%.3f）" % (ex["gold"], ex["laya"], ex["confidence"]),
                "",
            ]
        lines += ["### 易错例", ""]
        for ex in hard:
            note = "Laya 答错" if not ex["agreed"] else "Laya 低置信度"
            lines += [
                "- **%s**（%s）" % (ex["id"], note),
                "",
                "  %s" % ex["text"].replace("\n", "\n  "),
                "",
                "  标准答案：`%s`；Laya：`%s`（conf=%.3f）" % (ex["gold"], ex["laya"], ex["confidence"]),
                "",
            ]
    guide_path = os.path.join(out_dir, "guide.md")
    with open(guide_path, "w") as f:
        f.write("\n".join(lines))

    # --- 试卷 ---
    exam = _quiz_items(samples, per_qid=per_qid, rng=rng)
    exam_path = os.path.join(out_dir, "exam.jsonl")
    with open(exam_path, "w") as f:
        for item in exam:
            public = {k: v for k, v in item.items() if k != "answer_key"}
            f.write(json.dumps(public, ensure_ascii=False) + "\n")
    key_path = os.path.join(out_dir, "answer_key.jsonl")
    with open(key_path, "w") as f:
        for item in exam:
            f.write(json.dumps({"qid": item["qid"], "answer_key": item["answer_key"]}, ensure_ascii=False) + "\n")

    # --- 空白答卷模板 ---
    sheet_path = os.path.join(out_dir, "answer_sheet.template.jsonl")
    with open(sheet_path, "w") as f:
        for item in exam:
            f.write(json.dumps({"qid": item["qid"], "answer": "", "note": ""}, ensure_ascii=False) + "\n")

    meta = {
        "guide": guide_path,
        "exam": exam_path,
        "answer_key": key_path,
        "answer_sheet_template": sheet_path,
        "n_questions": len(exam),
        "by_decision": {qid: sum(1 for it in exam if it["decision"] == qid) for qid in QUESTIONS},
        "label_spaces": {qid: label_space(q) for qid, q in QUESTIONS.items()},
    }
    with open(os.path.join(out_dir, "pack.json"), "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    return meta
