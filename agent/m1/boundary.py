#!/usr/bin/env python3
"""Write local decision-boundary doc (zh/en via LAYA_LANG)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import paths as _paths
sys.path.insert(0, os.path.join(_paths.AGENT, "m1"))
sys.path.insert(0, _paths.AGENT)

from schema import AXES, MAX_CHOICE_OPTIONS, audit_schema
from i18n import boundary_lines


def write_boundary(dest=None):
    dest = dest or os.path.join(_paths.OUT, "decision_boundary.md")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    rows, blocked = audit_schema()
    lines = boundary_lines(rows, blocked, MAX_CHOICE_OPTIONS, AXES)
    with open(dest, "w") as f:
        f.write("\n".join(lines))
    return dest


if __name__ == "__main__":
    print(write_boundary())
