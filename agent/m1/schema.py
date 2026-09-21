"""News integration label space: fact axis + preference axis. Choice ≤ 20."""
MAX_CHOICE_OPTIONS = 20

# Two review axes used by annotation / diff.
AXES = {
    "fact": ["factual", "claim_status"],
    "preference": ["channel", "publish", "salience"],
}

QUESTIONS = {
    # —— 事实轴：正确性 ——
    "factual": {
        "type": "noul",
        "axis": "fact",
        "instructions": "Is the article's core claim factually sound as stated (no clear falsehood)?",
    },
    "claim_status": {
        "type": "choice",
        "axis": "fact",
        "instructions": "How should the claim be classified for the news desk?",
        "criteria": {
            "accurate": "supported and currently valid",
            "outdated": "was true but is stale or superseded",
            "misleading": "technically partial but frames wrongly",
            "unverifiable": "cannot check from the given text alone",
        },
    },
    # —— 偏好轴：集成 / 版面 ——
    "channel": {
        "type": "choice",
        "axis": "preference",
        "instructions": "Which channel should this item go to in the feed?",
        "criteria": {
            "politics": "government, elections, diplomacy",
            "business": "markets, companies, economy",
            "tech": "science, software, gadgets",
            "society": "culture, cities, daily life",
            "sports": "athletics and games",
            "other": "none of the above",
        },
    },
    "publish": {
        "type": "noul",
        "axis": "preference",
        "instructions": "Should this item be published into the integrated feed?",
    },
    "salience": {
        "type": "score",
        "axis": "preference",
        "instructions": "How prominent should this item be?",
        "criteria": ["skip or bury", "normal slot", "lead / top story"],
    },
}


def option_count(qdef):
    crit = qdef.get("criteria")
    if qdef["type"] == "noul":
        return 2
    if isinstance(crit, dict):
        return len(crit)
    if isinstance(crit, list):
        return len(crit)
    return 0


def label_space(qdef):
    crit = qdef.get("criteria")
    if isinstance(crit, dict):
        return list(crit.keys())
    if isinstance(crit, list):
        return ["%d:%s" % (i, c) for i, c in enumerate(crit)]
    return ["false", "true"]


def audit_schema(questions=None):
    questions = questions or QUESTIONS
    rows = []
    blocked = False
    for qid, qdef in questions.items():
        n = option_count(qdef)
        too_wide = qdef["type"] == "choice" and n > MAX_CHOICE_OPTIONS
        blocked = blocked or too_wide
        rows.append({
            "id": qid,
            "type": qdef["type"],
            "axis": qdef.get("axis"),
            "options": n,
            "label_space": label_space(qdef),
            "status": "shrink_or_abandon" if too_wide else "ok",
        })
    return rows, blocked
