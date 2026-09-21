#!/usr/bin/env python3
"""Write news decision-boundary doc from schema (+ optional annotated stats)."""
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import paths as _paths
sys.path.insert(0, os.path.join(_paths.AGENT, "m1"))

from schema import AXES, MAX_CHOICE_OPTIONS, audit_schema


def write_boundary(dest=None):
    dest = dest or os.path.join(_paths.OUT, "decision_boundary.md")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    rows, blocked = audit_schema()
    lines = [
        "# 新闻集成 · 决策边界",
        "",
        "批注含义：**用标记矫正正确性**（事实）并记录版面偏好。字段级 diff 见 `agent/annotate/`。",
        "",
        "choice 选项上限 **%d**。当前标签空间%s被拒绝。"
        % (MAX_CHOICE_OPTIONS, "已" if blocked else "未"),
        "",
        "## 两轴",
        "",
        "| 轴 | 字段 |",
        "|---|---|",
        "| 事实 fact | %s |" % ", ".join(AXES["fact"]),
        "| 偏好 preference | %s |" % ", ".join(AXES["preference"]),
        "",
        "## 字段",
        "",
        "| 字段 | 轴 | 原语 | 选项数 | 标签 | 状态 |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append("| %s | %s | %s | %d | %s | %s |" % (
            row["id"], row["axis"], row["type"], row["options"],
            ", ".join(row["label_space"]), row["status"]))
    lines += [
        "",
        "## 批注标记",
        "",
        "- `keep`：确认模型该字段正确",
        "- `fix`：矫正为批注值，写入金标",
        "- `flag`：存疑，不入库",
        "",
    ]
    with open(dest, "w") as f:
        f.write("\n".join(lines))
    return dest


if __name__ == "__main__":
    print(write_boundary())
