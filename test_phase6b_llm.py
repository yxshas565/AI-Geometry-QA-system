from agent.llm_agent import generate_llm_explanation

facts = {
    "line_id": 13,
    "severity": "HIGH RISK",
    "role": "STANDARD",
    "ml_anomaly_score": -0.27,
    "context_anomaly": True,
    "length_ratio": 2.9,
    "abnormal_segments": []
}


print("=== LLM AGENT OUTPUT ===")
print(generate_llm_explanation(facts))
