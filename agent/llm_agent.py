# # agent/llm_agent.py

# from openai import OpenAI
# import json

# client = OpenAI()

# # ---------------- SYSTEM PROMPT ----------------
# SYSTEM_PROMPT = """
# You are a GIS Quality Assurance Assistant.

# You will receive structured facts about a map geometry.

# Your task is to generate a QA report in the EXACT format below.
# Do NOT add extra sections.
# Do NOT change severity.
# Do NOT invent issues.

# FORMAT:

# LINE ID: <line_id>
# SEVERITY: <severity>

# WHY THIS WAS FLAGGED:
# - <reason 1>
# - <reason 2>

# WHERE THE ISSUE IS:
# - <location or explanation>

# RECOMMENDED ACTIONS:
# - <action 1>
# - <action 2>

# Rules:
# - Use ONLY the provided facts.
# - Be concise and technical.
# """

# # ---------------- JSON SAFETY ----------------
# def make_json_safe(obj):
#     if isinstance(obj, dict):
#         return {k: make_json_safe(v) for k, v in obj.items()}
#     elif isinstance(obj, list):
#         return [make_json_safe(v) for v in obj]
#     elif hasattr(obj, "item"):  # numpy scalar
#         return obj.item()
#     else:
#         return obj


# # ---------------- STREAMING LLM (CORRECT) ----------------
# def generate_llm_explanation_stream(facts: dict):
#     """
#     Fully working streaming implementation.
#     No buffering.
#     No retries.
#     No token waste.
#     """

#     if not facts:
#         print("[LLM SKIPPED] Empty facts")
#         return

#     safe_facts = make_json_safe(facts)

#     response_stream = client.responses.create(
#         model="gpt-4.1-mini",  # cheaper + stable
#         stream=True,
#         input=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {
#                 "role": "user",
#                 "content": f"Facts:\n{json.dumps(safe_facts, indent=2)}"
#             }
#         ],
#         temperature=0.2,
#         max_output_tokens=250  # HARD COST CAP
#     )

#     print("\n=== LLM QA REPORT (STREAMING) ===\n")

#     # ✅ THIS IS THE ONLY VALID WAY
#     for event in response_stream:
#         if event.type == "response.output_text.delta":
#             print(event.delta, end="", flush=True)

#         elif event.type == "response.completed":
#             break

#     print("\n")  # clean newline after report



# def generate_llm_explanation_stream(facts: dict):
#     if not facts:
#         print("[LLM SKIPPED] Empty facts")
#         return

#     safe_facts = make_json_safe(facts)

#     response_stream = client.responses.create(
#         model="gpt-4.1-mini",
#         stream=True,
#         input=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {
#                 "role": "user",
#                 "content": f"Facts:\n{json.dumps(safe_facts, indent=2)}"
#             }
#         ],
#         temperature=0.2,
#         max_output_tokens=250  # still keep this
#     )

#     print("\n=== LLM QA REPORT (FIRST 5 LINES ONLY) ===\n")

#     line_count = 0
#     buffer = ""

#     for event in response_stream:
#         if event.type == "response.output_text.delta":
#             buffer += event.delta

#             while "\n" in buffer:
#                 line, buffer = buffer.split("\n", 1)
#                 print(line)
#                 line_count += 1

#                 # 🔒 HARD STOP AFTER 5 LINES
#                 if line_count >= 5:
#                     print("\n[LLM STOPPED AFTER 5 LINES]")
#                     return

#         elif event.type == "response.completed":
#             break

#     print()







def severity_bar(severity, width=12):
    mapping = {
        "LOW": 0.3,
        "MEDIUM": 0.6,
        "HIGH": 0.85
    }

    score = mapping.get(severity, 0.5)
    filled = int(score * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {score:.2f}"



# agent/llm_agent.py

import json
import requests








# ---------------- SYSTEM PROMPT ----------------
# SYSTEM_PROMPT = """
# You are a GIS Quality Assurance Assistant.

# You will receive structured facts about a map geometry.

# Your task is to generate a QA report in the EXACT format below.
# Do NOT add extra sections.
# Do NOT change severity.
# Do NOT invent issues.

# FORMAT:

# LINE ID: <line_id>
# SEVERITY: <severity>

# WHY THIS WAS FLAGGED:
# - <reason 1>
# - <reason 2>

# WHERE THE ISSUE IS:
# - <location or explanation>

# RECOMMENDED ACTIONS:
# - <action 1>
# - <action 2>

# Rules:
# - Use ONLY the provided facts.
# - Be concise and technical.
# """







SYSTEM_PROMPT = """
You are a senior GIS Quality Assurance engineer.

You will receive structured facts about a single map geometry.
These facts are FINAL and already validated.

Your task:
- Generate a clear, developer-friendly QA explanation
- Do NOT change severity or verdict
- Do NOT invent issues
- Do NOT mention uncertainty
- Explain exactly:
  1. Why the geometry was flagged (based on facts)
  2. Where the issue occurs (use segment indices if present)
  3. How a developer should fix it (specific and actionable)

Use professional technical language.
Vary phrasing naturally across different cases.
Be concise but informative.

Output FORMAT (exactly):

LINE ID: <line_id>
SEVERITY: <severity>

WHY THIS WAS FLAGGED:
<paragraph>

WHERE THE ISSUE IS:
<paragraph>

RECOMMENDED ACTIONS:
<paragraph>
"""



# ---------------- JSON SAFETY ----------------
def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif hasattr(obj, "item"):  # numpy scalar
        return obj.item()
    else:
        return obj








# ---------------- OLLAMA HTTP API (THE REAL FIX) ----------------
# def generate_llm_explanation_stream(facts: dict):
#     """
#     Uses Ollama HTTP API.
#     This is the ONLY reliable method on Windows.
#     """

#     if not facts:
#         return

#     safe_facts = make_json_safe(facts)

#     prompt = f"""{SYSTEM_PROMPT}

# Facts:
# {json.dumps(safe_facts, indent=2)}
# """

#     print("\n=== LLM QA REPORT (LOCAL MODEL) ===\n")

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "phi3:mini",
#             "prompt": prompt,
#             "stream": False  # IMPORTANT: deterministic, no CLI bugs
#         },
#         timeout=120
#     )

#     if response.status_code != 200:
#         print("[LLM ERROR] Ollama API failed")
#         return

#     data = response.json()
#     text = data.get("response", "").strip()

#     if not text:
#         print("[LLM ERROR] Empty response from model")
#         return

#     print(text)
#     print()

# agent/llm_agent.py





# From here i had commented out

import time


# ---------------- CONFIDENCE BAR (FIXED) ----------------
def signed_confidence_bar(value, width=24):
    """
    Bi-directional confidence bar.
    Negative values grow LEFT (anomaly / critical).
    Positive values grow RIGHT (normal / safe).
    """

    try:
        value = float(value)
    except (TypeError, ValueError):
        value = 0.0

    # Clamp to [-1, 1]
    value = max(-1.0, min(1.0, value))

    half = width // 2
    left = ""
    right = ""

    if value < 0:
        filled = int(abs(value) * half)
        left = "█" * filled + "░" * (half - filled)
        right = "░" * half
    elif value > 0:
        filled = int(value * half)
        left = "░" * half
        right = "█" * filled + "░" * (half - filled)
    else:
        left = "░" * half
        right = "░" * half

    return f"[{left}|{right}] {value:+.2f}"



# ---------------- STREAM PRINT ----------------
def stream_print(text, delay=0.02):
    """Print text character-by-character (streaming effect)."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def build_reasoning_explanation(facts: dict):
    verdict = facts.get("verdict", "UNKNOWN")
    conf = facts.get("confidence", 0.0)

    if verdict == "PASS":
        return (
            "This geometry meets all structural validation rules and conforms to expected "
            "patterns for its contextual role. Statistical analysis did not identify any "
            "anomalous characteristics, indicating the geometry is suitable for downstream processing."
        )

    reasons = []

    if facts.get("rule_violation"):
        reasons.append(
            "The geometry violates one or more structural validation rules, "
            "indicating invalid shape or topology."
        )

    if facts.get("context_anomaly"):
        reasons.append(
            "The geometry deviates from typical characteristics expected for its contextual role."
        )

    if conf < 0:
        reasons.append(
            f"Machine learning analysis classified this geometry as anomalous "
            f"(anomaly score: {conf:.2f})."
        )

    return " ".join(reasons)

def build_location_explanation(facts: dict):
    verdict = facts.get("verdict", "UNKNOWN")
    segments = facts.get("abnormal_segments")

    if verdict == "PASS":
        return (
            "No localized geometric issues were detected. The line geometry is "
            "consistent across its entire length."
        )

    if segments:
        return (
            f"The issue is localized to specific segments of the line geometry, "
            f"notably at indices {segments}, where abnormal geometric behavior was detected."
        )

    return (
        "The issue affects the overall structure of the geometry rather than a single segment."
    )

def build_recommendation(facts: dict):
    verdict = facts.get("verdict", "UNKNOWN")
    actions = []

    if verdict == "PASS":
        return (
            "No corrective action is required. The geometry can safely proceed through "
            "subsequent processing stages."
        )

    if facts.get("rule_violation"):
        actions.append(
            "Inspect the geometry for structural issues such as self-intersections, overlaps, "
            "or invalid coordinate ordering."
        )

    if facts.get("abnormal_segments"):
        actions.append(
            "Focus corrections on the identified segments to smooth abrupt changes or inconsistencies."
        )

    actions.append(
        "After applying corrections, re-run quality validation to ensure compliance."
    )

    return " ".join(actions)



# # ---------------- EXPLANATION BUILDERS ----------------
# def build_reasoning_explanation(facts: dict):
#     """
#     Converts validated facts into human-friendly reasoning.
#     Deterministic. No AI.
#     """

#     reasons = []

#     if facts.get("rule_violation"):
#         reasons.append(
#             "The geometry violates one or more structural validation rules, "
#             "indicating that its shape or topology does not meet expected standards."
#         )

#     if facts.get("context_anomaly"):
#         reasons.append(
#             "Based on its assigned contextual role, this line deviates significantly "
#             "from typical geometric characteristics observed in similar features."
#         )

#     conf = facts.get("confidence", 0.0)
#     if conf < 0:
#         reasons.append(
#             f"Machine learning analysis identified this geometry as an anomaly "
#             f"(anomaly score: {conf:.2f}), suggesting unusual structural patterns."
#         )

#     if not reasons:
#         reasons.append(
#             "No structural, contextual, or statistical anomalies were detected."
#         )

#     return " ".join(reasons)


# def build_location_explanation(facts: dict):
#     segments = facts.get("abnormal_segments")

#     if segments:
#         return (
#             f"The issue is localized to specific segments of the line geometry, "
#             f"notably at segment indices {segments}, where abnormal geometric behavior was detected."
#         )
#     else:
#         return (
#             "The issue affects the geometry as a whole and is not confined to a single segment."
#         )


# def build_recommendation(facts: dict):
#     actions = []

#     if facts.get("rule_violation"):
#         actions.append(
#             "Inspect the line geometry for structural issues such as self-intersections, "
#             "overlaps, or invalid coordinate sequences."
#         )

#     if facts.get("abnormal_segments"):
#         actions.append(
#             "Focus editing efforts on the highlighted segments to correct abrupt changes "
#             "in direction or length."
#         )

#     actions.append(
#         "After corrections are applied, re-run validation to confirm that the geometry "
#         "meets quality requirements."
#     )

#     return " ".join(actions)



# # ---------------- STREAMING EXPLANATION ----------------
# def generate_llm_explanation_stream(facts: dict):
#     """
#     Deterministic + streaming-safe explanation.
#     No LLM dependency.
#     """

#     if not facts:
#         return

#     sev = facts.get("severity", "UNKNOWN")
#     conf = facts.get("confidence", 0.5)
#     score = facts.get("confidence", 0.0)
#     output = []

#     output.append("=== QA REPORT (STREAMING MODE) ===\n")
#     output.append(f"LINE ID: {facts.get('line_id')}\n")
#     output.append(
#         f"SEVERITY: {sev} {signed_confidence_bar(score)}\n\n"
#     )

#     output.append("WHY THIS WAS FLAGGED:\n")
#     if facts.get("rule_violation"):
#         output.append("- Geometry violated validation rules\n")
#     if facts.get("context_anomaly"):
#         output.append("- Contextual role-based deviation detected\n")
#     if conf > 0:
#         output.append(f"- ML anomaly confidence: {conf:.2f}\n")

#     output.append("\nWHERE THE ISSUE IS:\n")
#     if facts.get("abnormal_segments"):
#         output.append(
#             f"- Abnormal segments detected: {facts['abnormal_segments']}\n"
#         )
#     else:
#         output.append("- Geometry-level inconsistency\n")

#     output.append("\nRECOMMENDED ACTIONS:\n")
#     output.append("- Inspect geometry manually\n")
#     output.append("- Re-validate after correction\n")

#     # 🔴 STREAM OUTPUT (SAFE)
#     for block in output:
#         stream_print(block)



def generate_llm_explanation_stream(facts: dict):
    """
    Deterministic + streaming-safe explanation.
    No LLM dependency.
    """

    if not facts:
        return

    sev = facts.get("severity", "UNKNOWN")
    score = facts.get("confidence", 0.0)

    output = []

    output.append("=== QA REPORT (STREAMING MODE) ===\n")
    output.append(f"LINE ID: {facts.get('line_id')}\n")
    output.append(
        f"SEVERITY: {sev} {signed_confidence_bar(score)}\n\n"
    )

    output.append("WHY THIS WAS FLAGGED:\n")
    output.append(build_reasoning_explanation(facts) + "\n\n")

    output.append("WHERE THE ISSUE IS:\n")
    output.append(build_location_explanation(facts) + "\n\n")

    output.append("RECOMMENDED ACTIONS:\n")
    output.append(build_recommendation(facts) + "\n")

    for block in output:
        stream_print(block)
