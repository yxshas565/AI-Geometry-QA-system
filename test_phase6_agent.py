from agent.explainer import (
    explain_issue,
    suggest_actions,
    agent_response
)

# Simulated inputs from earlier phases
line_id = 48
severity = "LOW RISK"
rule_flag = False
ml_flag = False
context_flag = True
features = {"length_ratio": 1.56}
abnormal_segments = []

explanations = explain_issue(
    rule_flag,
    ml_flag,
    context_flag,
    features,
    abnormal_segments
)

actions = suggest_actions(severity)

response = agent_response(
    line_id,
    severity,
    explanations,
    actions
)

print("=== AI AGENT RESPONSE ===")
for k, v in response.items():
    print(f"{k}: {v}")
