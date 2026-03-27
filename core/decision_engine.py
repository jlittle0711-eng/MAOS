def determine_priority(score):
    if score >= 85:
        return "HIGH"
    elif score >= 70:
        return "MEDIUM"
    elif score >= 50:
        return "LOW"
    else:
        return "IGNORE"


def determine_action(priority):
    mapping = {
        "HIGH": "APPLY",
        "MEDIUM": "MONITOR",
        "LOW": "HOLD",
        "IGNORE": "IGNORE"
    }
    return mapping.get(priority, "IGNORE")


def apply_overrides(priority, action, context, flags):
    """
    Applies override logic (e.g., outage suppression)
    """

    if context.get("outage"):
        if priority == "HIGH":
            flags.append("OUTAGE_OVERRIDE")
            return "MEDIUM", "MONITOR"
        elif priority == "MEDIUM":
            flags.append("OUTAGE_OVERRIDE")
            return "LOW", "HOLD"

    return priority, action


def build_reason(grant, context):
    reasons = []

    keywords = (grant.get("keywords") or "").lower()

    if context.get("eicmm"):
        reasons.append("alignment with infrastructure/energy priorities")

    if context.get("hhs"):
        reasons.append("agency priority boost (HHS/Health)")

    if "workforce" in keywords:
        reasons.append("workforce development relevance")

    if not reasons:
        return "Standard evaluation based on score."

    return "High alignment with " + " + ".join(reasons) + "."


def evaluate_grant(grant, score, flags, context):
    priority = determine_priority(score)
    action = determine_action(priority)

    priority, action = apply_overrides(priority, action, context, flags)

    reason = build_reason(grant, context)

    return {
        "title": grant.get("title", ""),
        "agency": grant.get("agency", ""),
        "score": score,
        "priority": priority,
        "action": action,
        "reason": reason,
        "flags": flags
    }