# # decision/fusion_engine.py

# def fuse_decision(rule_flag, ml_flag, context_flag):
#     """
#     Returns:
#     - severity
#     - explanation
#     """

#     if rule_flag and ml_flag:
#         return (
#             "CRITICAL",
#             "Rule violation and ML anomaly detected"
#         )

#     if ml_flag and context_flag:
#         return (
#             "HIGH RISK",
#             "ML anomaly confirmed by contextual deviation"
#         )

#     if ml_flag or rule_flag:
#         return (
#             "MEDIUM RISK",
#             "Single-source anomaly detected"
#         )

#     if context_flag:
#         return (
#             "LOW RISK",
#             "Minor contextual deviation"
#         )

#     return (
#         "SAFE",
#         "No anomalies detected"
#     )



def fuse_decision(rule_flag: bool, ml_flag: bool, context_flag: bool):
    """
    Decision fusion with STRICT verdict contract.

    Returns:
        severity (str): descriptive label
        verdict  (str): PASS | WARNING | FAIL
    """

    score = 0
    reasons = []

    if rule_flag:
        score += 2
        reasons.append("Rule violation detected")

    if ml_flag:
        score += 1
        reasons.append("ML anomaly detected")

    if context_flag:
        score += 1
        reasons.append("Contextual anomaly detected")

    # ---- FINAL DECISION ----
    if score >= 3:
        return "HIGH RISK", "FAIL"

    if score == 2:
        return "MEDIUM RISK", "WARNING"

    if score == 1:
        return "LOW RISK", "WARNING"

    return "PASS", "PASS"
