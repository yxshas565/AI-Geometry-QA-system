# import json
# import numpy as np

# from geometry.parser import load_geometry
# from geometry.validators import (
#     check_geometry_validity,
#     detect_abnormal_segments
# )
# from features.extractor import extract_line_features
# from models.anomaly_model import GeometryAnomalyDetector
# from context.role_classifier import classify_line_role
# from context.neighborhood_analysis import (
#     compute_role_statistics,
#     role_based_anomaly
# )
# from decision.fusion_engine import fuse_decision
# from agent.llm_agent import generate_llm_explanation_stream


# # -------- LOAD WKT DATA --------
# wkts = []
# current = ""

# with open("data/raw/lines.wkt", "r") as f:
#     for line in f:
#         line = line.strip()
#         if not line:
#             continue
#         current += " " + line
#         if line.endswith(")"):
#             wkts.append(current.strip())
#             current = ""

# # -------- PHASE 1 + 2 --------
# lines_data = []

# for idx, wkt in enumerate(wkts):
#     try:
#         geom = load_geometry(wkt)
#         features = extract_line_features(geom)

#         lines_data.append({
#             "line_id": idx + 1,
#             "geom": geom,
#             "features": features
#         })
#     except:
#         continue

# # -------- PHASE 3 (ML) --------
# X = np.array([
#     [
#         item["features"]["num_points"],
#         item["features"]["total_length"],
#         item["features"]["avg_segment_length"],
#         item["features"]["max_segment_length"],
#         item["features"]["length_ratio"],
#         item["features"]["bbox_area"]
#     ]
#     for item in lines_data
# ])

# detector = GeometryAnomalyDetector(contamination=0.05)
# detector.fit(X)
# ml_preds, ml_scores = detector.predict(X)

# # -------- PHASE 4 (CONTEXT) --------
# for item in lines_data:
#     item["role"] = classify_line_role(item["features"])

# role_stats = compute_role_statistics([
#     {"role": item["role"], "features": item["features"]}
#     for item in lines_data
# ])

# # -------- FULL PIPELINE + LLM --------
# print("\n=== FULL AI AGENT OUTPUT (AUTO PER LINE) ===\n")

# for i, item in enumerate(lines_data):
#     geom = item["geom"]
#     features = item["features"]

#     # Phase-1
#     validity_issues = check_geometry_validity(geom)
#     abnormal_segments = detect_abnormal_segments(geom, jump_threshold=2)
#     rule_flag = bool(validity_issues or abnormal_segments)

#     # Phase-3
#     ml_flag = (ml_preds[i] == -1)
#     ml_score = float(ml_scores[i])

#     # Phase-4
#     context_flag = role_based_anomaly(
#         {"role": item["role"], "features": features},
#         role_stats
#     )

#     # Phase-5
#     severity, _ = fuse_decision(
#         rule_flag,
#         ml_flag,
#         context_flag
#     )

#     # -------- AUTO-GENERATED FACTS --------
#     facts = {
#         "line_id": item["line_id"],
#         "severity": severity,
#         "role": item["role"],
#         "ml_anomaly_score": round(ml_score, 3),
#         "context_anomaly": context_flag,
#         "length_ratio": round(features["length_ratio"], 2),
#         "abnormal_segments": abnormal_segments
#     }

#     # -------- PHASE-6b (LLM) --------
#     generate_llm_explanation_stream(facts)
#     print("-" * 60)

def verdict_to_bucket(verdict: str) -> str:
    """
    Maps verbose decision text to summary buckets.
    Does NOT change decision semantics.
    """
    v = verdict.lower()

    if "pass" in v:
        return "PASS"
    if "fail" in v or "high" in v:
        return "FAIL"
    if "warning" in v or "medium" in v or "low" in v:
        return "WARNING"

    # safe default
    return "WARNING"


# run_full_pipeline_with_llm.py

import numpy as np

from geometry.parser import load_geometry
from geometry.validators import (
    check_geometry_validity,
    detect_abnormal_segments
)

from features.extractor import extract_line_features
from models.anomaly_model import GeometryAnomalyDetector

from context.role_classifier import classify_line_role
from context.neighborhood_analysis import (
    compute_role_statistics,
    role_based_anomaly
)

from decision.fusion_engine import fuse_decision
from agent.llm_agent import generate_llm_explanation_stream


# ============================================================
# LOAD WKT DATA
# ============================================================

wkts = []
current = ""

with open("data/raw/lines.wkt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        current += " " + line
        if line.endswith(")"):
            wkts.append(current.strip())
            current = ""


# ============================================================
# PHASE 1 + 2 : GEOMETRY + FEATURE EXTRACTION
# ============================================================

lines_data = []

for idx, wkt in enumerate(wkts):
    try:
        geom = load_geometry(wkt)
        features = extract_line_features(geom)

        lines_data.append({
            "line_id": idx + 1,
            "geom": geom,
            "features": features
        })

    except Exception:
        continue


# ============================================================
# PHASE 3 : ML ANOMALY DETECTION
# ============================================================

X = np.array([
    [
        item["features"]["num_points"],
        item["features"]["total_length"],
        item["features"]["avg_segment_length"],
        item["features"]["max_segment_length"],
        item["features"]["length_ratio"],
        item["features"]["bbox_area"]
    ]
    for item in lines_data
])

detector = GeometryAnomalyDetector(contamination=0.05)
detector.fit(X)

ml_preds, ml_scores = detector.predict(X)


# ============================================================
# PHASE 4 : CONTEXTUAL ROLE ANALYSIS
# ============================================================

for item in lines_data:
    item["role"] = classify_line_role(item["features"])

role_stats = compute_role_statistics([
    {"role": item["role"], "features": item["features"]}
    for item in lines_data
])


# ============================================================
# GLOBAL SUMMARY INIT (STRICT VERDICT BUCKETS)
# ============================================================

summary = {
    "TOTAL": 0,
    "PASS": 0,
    "WARNING": 0,
    "FAIL": 0
}


# ============================================================
# FULL PIPELINE
# ============================================================

print("\n=== FULL AI AGENT OUTPUT (AUTO PER LINE) ===\n")

for i, item in enumerate(lines_data):
    geom = item["geom"]
    features = item["features"]

    # ---------------- Rule-based ----------------
    validity_issues = check_geometry_validity(geom)
    abnormal_segments = detect_abnormal_segments(
        geom,
        jump_threshold=2
    )
    rule_flag = bool(validity_issues or abnormal_segments)

    # ---------------- ML ----------------
    ml_flag = (ml_preds[i] == -1)
    ml_score = float(ml_scores[i])   # may be negative (important)

    # ---------------- Context ----------------
    context_flag = role_based_anomaly(
        {"role": item["role"], "features": features},
        role_stats
    )

    # ---------------- Decision Fusion ----------------
    # CONTRACT:
    # verdict ∈ {"PASS", "WARNING", "FAIL"}
    severity, verdict = fuse_decision(
        rule_flag=rule_flag,
        ml_flag=ml_flag,
        context_flag=context_flag
    )

    # ---------------- GLOBAL SUMMARY UPDATE ----------------
    summary["TOTAL"] += 1
    summary[verdict] += 1

    # ---------------- FACTS (SIGNED CONFIDENCE) ----------------
    facts = {
        "line_id": item["line_id"],
        "severity": severity,          # e.g. HIGH RISK
        "verdict": verdict,            # PASS / WARNING / FAIL
        "confidence": ml_score,        # SIGNED value (negative allowed)
        "role": item["role"],
        "rule_violation": rule_flag,
        "context_anomaly": context_flag,
        "abnormal_segments": abnormal_segments
    }

    # ---------------- EXPLANATION ----------------
    generate_llm_explanation_stream(facts)


    print("-" * 60)


# ============================================================
# FINAL DATASET SUMMARY
# ============================================================

print("\n=== FINAL DATASET QA SUMMARY ===\n")
print(f"Total lines checked : {summary['TOTAL']}")
print(f"PASS               : {summary['PASS']}")
print(f"WARNING            : {summary['WARNING']}")
print(f"FAIL               : {summary['FAIL']}")
