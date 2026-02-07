def fuse_decisions(rule_result, ml_result, context_result):
    """
    Combines rule-based, ML, and contextual signals
    into a single authoritative verdict.
    """

    score = 0.0
    reasons = []

    # ---- RULES (highest priority) ----
    if rule_result["violated"]:
        score += 0.5
        reasons.extend(rule_result["reasons"])

    # ---- ML ----
    if ml_result["anomaly"]:
        score += 0.3 * ml_result["confidence"]
        reasons.append(ml_result["reason"])

    # ---- CONTEXT ----
    if context_result["risk"] == "high":
        score += 0.2
        reasons.append(context_result["note"])

    score = min(score, 1.0)

    verdict = "PASS"
    if score >= 0.7:
        verdict = "FAIL"
    elif score >= 0.4:
        verdict = "WARNING"

    return {
        "verdict": verdict,
        "confidence": round(score, 2),
        "reasons": reasons
    }
