import datetime

OUTAGE_START = datetime.date(2026, 5, 16)
OUTAGE_END = datetime.date(2026, 5, 18)


def apply_signals(grant):
    """
    Applies signal rules to a grant record.

    Returns:
        modified_score (int)
        flags (list)
        context (dict)
    """

    score = grant.get("score", 0)
    flags = []
    context = {
        "outage": False,
        "eicmm": False,
        "hhs": False
    }

    today = datetime.date.today()

    # 🚫 RULE 1 — OUTAGE WINDOW
    if OUTAGE_START <= today <= OUTAGE_END:
        context["outage"] = True
        flags.append("OUTAGE_WINDOW")

    # ⚡ RULE 2 — EICMM CATEGORY BOOST
    keywords = (grant.get("keywords") or "").lower()

    eicmm_terms = [
        "energy",
        "infrastructure",
        "critical materials",
        "supply chain"
    ]

    if any(term in keywords for term in eicmm_terms):
        score += 10
        context["eicmm"] = True
        flags.append("EICMM_MATCH")

    # 🧬 RULE 3 — AGENCY PRIORITY (HHS)
    agency = (grant.get("agency") or "").lower()

    if "health" in agency or "hhs" in agency:
        score += 5
        context["hhs"] = True
        flags.append("HHS_PRIORITY")

    return score, flags, context