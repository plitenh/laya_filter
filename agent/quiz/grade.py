#!/usr/bin/env python3
"""Grade a filled answer sheet against the quiz key; write human-reviewed gold back."""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import paths as _paths
sys.path.insert(0, os.path.join(_paths.AGENT, "m1"))
sys.path.insert(0, _paths.QUIZ)

from build import _canon, _load
from schema import QUESTIONS

QUIZ = _paths.QUIZ


def _parse_answer(decision, raw):
    return _canon(decision, raw)


def grade(sheet_path, exam_path=None, key_path=None, out_dir=QUIZ, grader="human"):
    exam_path = exam_path or os.path.join(out_dir, "exam.jsonl")
    key_path = key_path or os.path.join(out_dir, "answer_key.jsonl")
    exam = {r["qid"]: r for r in _load(exam_path)}
    keys = {r["qid"]: r["answer_key"] for r in _load(key_path)}
    sheet = _load(sheet_path)
    if not sheet:
        raise SystemExit("empty answer sheet")

    results = []
    score = {"total": 0, "correct": 0, "wrong": 0, "blank": 0, "by_decision": {}}
    gold_rows = []

    for row in sheet:
        qid = row["qid"]
        item = exam.get(qid)
        if item is None:
            continue
        decision = item["decision"]
        key = keys[qid]
        raw = row.get("answer", "")
        score["total"] += 1
        bucket = score["by_decision"].setdefault(decision, {"total": 0, "correct": 0})
        bucket["total"] += 1
        if raw is None or str(raw).strip() == "":
            score["blank"] += 1
            status = "blank"
            user = None
            ok = False
        else:
            user = _parse_answer(decision, raw)
            ok = user == key
            if ok:
                score["correct"] += 1
                bucket["correct"] += 1
                status = "correct"
            else:
                score["wrong"] += 1
                status = "wrong"
        result = {
            "qid": qid,
            "sample_id": item["sample_id"],
            "decision": decision,
            "material": item["material"],
            "prompt": item["prompt"],
            "user_answer": user,
            "answer_key": key,
            "laya_prediction": item["laya_prediction"],
            "status": status,
            "points": 1 if ok else 0,
            "note": row.get("note", ""),
            "grader": grader,
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        results.append(result)
        # 批阅通过：用户答案成为人工最终标签（对错都写，错的仍以标准答案入库训练）
        final = key if status != "blank" else None
        if final is not None:
            gold_rows.append({
                "id": item["sample_id"],
                "state": {"body": item["material"]} if isinstance(item["material"], str) else item["material"],
                "gold": {decision: _typed(decision, final)},
                "source": "quiz_graded",
                "grader": grader,
                "user_agreed_with_key": ok,
                "laya_prediction": item["laya_prediction"],
            })

    pct = 100.0 * score["correct"] / max(1, score["total"] - score["blank"])
    report = {
        "grader": grader,
        "score": score,
        "percent": round(pct, 1),
        "pass": pct >= 80.0,
        "n_gold_written": len(gold_rows),
    }

    graded_path = os.path.join(out_dir, "graded.jsonl")
    with open(graded_path, "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    gold_path = os.path.join(out_dir, "graded_gold.jsonl")
    # merge same sample_id golds into one row
    merged = {}
    for g in gold_rows:
        m = merged.setdefault(g["id"], {"id": g["id"], "state": g["state"], "gold": {}, "source": "quiz_graded", "grader": grader})
        m["gold"].update(g["gold"])
    with open(gold_path, "w") as f:
        for g in merged.values():
            f.write(json.dumps(g, ensure_ascii=False) + "\n")

    md = [
        "# 批阅成绩单",
        "",
        "阅卷人：%s" % grader,
        "得分：**%d / %d**（有效题不计空白），正确率 **%.1f%%**，%s。"
        % (score["correct"], score["total"] - score["blank"], pct, "及格" if report["pass"] else "未及格"),
        "",
        "| 决策 | 题数 | 正确 |",
        "|---|---|---|",
    ]
    for d, b in score["by_decision"].items():
        md.append("| %s | %d | %d |" % (d, b["total"], b["correct"]))
    md += ["", "## 错题", ""]
    for r in results:
        if r["status"] != "wrong":
            continue
        md += [
            "### %s / %s" % (r["qid"], r["decision"]),
            "",
            r["material"],
            "",
            "- 你的答案：`%s`" % r["user_answer"],
            "- 标准答案：`%s`" % r["answer_key"],
            "- Laya：`%s`" % r["laya_prediction"],
            "",
        ]
    report_path = os.path.join(out_dir, "report.md")
    with open(report_path, "w") as f:
        f.write("\n".join(md))

    report["graded"] = graded_path
    report["gold"] = gold_path
    report["report"] = report_path
    with open(os.path.join(out_dir, "last_grade.json"), "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return report


def _typed(decision, canon):
    q = QUESTIONS[decision]
    if q["type"] == "choice":
        return canon
    if q["type"] == "score":
        return int(canon)
    return canon == "true"


def main():
    parser = argparse.ArgumentParser(description="Grade quiz answer sheet")
    parser.add_argument("--sheet", required=True, help="filled answer_sheet.jsonl")
    parser.add_argument("--grader", default="human")
    parser.add_argument("--out", default=QUIZ)
    args = parser.parse_args()
    report = grade(args.sheet, out_dir=args.out, grader=args.grader)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
