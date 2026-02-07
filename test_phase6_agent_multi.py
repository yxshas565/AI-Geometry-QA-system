from agent.explainer import (
    explain_issue,
    suggest_actions,
    agent_response
)

# Simulated test cases from earlier phases
test_cases = [
    {
        "line_id": 1,
        "severity": "CRITICAL",
        "rule_flag": True,
        "ml_flag": True,
        "context_flag": False,
        "abnormal_segments": [(2, 138.6)]
    },
    {
        "line_id": 13,
        "severity": "HIGH RISK",
        "rule_flag": False,
        "ml_flag": True,
        "context_flag": True,
        "abnormal_segments": []
    },
    {
        "line_id": 33,
        "severity": "MEDIUM RISK",
        "rule_flag": False,
        "ml_flag": True,
        "context_flag": False,
        "abnormal_segments": []
    },
    {
        "line_id": 48,
        "severity": "LOW RISK",
        "rule_flag": False,
        "ml_flag": False,
        "context_flag": True,
        "abnormal_segments": []
    },
    {
        "line_id": 20,
        "severity": "SAFE",
        "rule_flag": False,
        "ml_flag": False,
        "context_flag": False,
        "abnormal_segments": []
    }
]

print("=== PHASE-6 AGENT MULTI-CASE TEST ===\n")

for case in test_cases:
    explanations = explain_issue(
        case["rule_flag"],
        case["ml_flag"],
        case["context_flag"],
        features={},  # not needed yet
        abnormal_segments=case["abnormal_segments"]
    )

    actions = suggest_actions(case["severity"])

    response = agent_response(
        case["line_id"],
        case["severity"],
        explanations,
        actions
    )

    print(f"--- LINE {case['line_id']} ---")
    print("Severity:", response["severity"])
    print("Explanation:")
    for e in response["explanation"]:
        print(" -", e)
    print("Recommended Actions:")
    for a in response["recommended_actions"]:
        print(" -", a)
    print()
