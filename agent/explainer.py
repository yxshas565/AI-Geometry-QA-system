# agent/explainer.py

def explain_issue(rule_flag, ml_flag, context_flag, features, abnormal_segments):
    explanations = []

    if rule_flag:
        explanations.append(
            "Geometry violates basic structural rules (abnormal segment or invalid shape)."
        )

    if ml_flag:
        explanations.append(
            "Geometry is statistically unusual compared to the majority of map features."
        )

    if context_flag:
        explanations.append(
            "Geometry behaves abnormally compared to similar features of the same type."
        )

    if abnormal_segments:
        for idx, length in abnormal_segments:
            explanations.append(
                f"Abnormal segment detected at index {idx} with length {round(length, 2)}."
            )

    if not explanations:
        explanations.append("No issues detected. Geometry appears normal.")

    return explanations


# agent/explainer.py (continue in same file)

def suggest_actions(severity):
    if severity == "CRITICAL":
        return [
            "Immediate manual inspection required.",
            "Check geometry creation or import process.",
            "Verify coordinate system and precision."
        ]

    if severity == "HIGH RISK":
        return [
            "Inspect generalization or simplification logic.",
            "Compare with neighboring geometries."
        ]

    if severity == "MEDIUM RISK":
        return [
            "Review geometry if time permits.",
            "Monitor similar features for patterns."
        ]

    if severity == "LOW RISK":
        return [
            "Optional review.",
            "Likely acceptable but slightly inconsistent."
        ]

    return ["No action required."]


# agent/explainer.py (continue)

def agent_response(
    line_id,
    severity,
    explanations,
    actions
):
    return {
        "line_id": line_id,
        "severity": severity,
        "explanation": explanations,
        "recommended_actions": actions
    }
