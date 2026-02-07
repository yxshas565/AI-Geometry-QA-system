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
import numpy as np

# --- Load WKTs ---
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

# --- Feature extraction ---
lines_data = []

for idx, wkt in enumerate(wkts):
    try:
        geom = load_geometry(wkt)
        features = extract_line_features(geom)

        lines_data.append({
            "id": idx + 1,
            "geom": geom,
            "features": features
        })
    except:
        continue

# --- ML model ---
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
preds, scores = detector.predict(X)

# --- Context stats ---
for item in lines_data:
    item["role"] = classify_line_role(item["features"])

role_stats = compute_role_statistics([
    {"role": item["role"], "features": item["features"]}
    for item in lines_data
])

# --- Final decision ---
print("=== FINAL QA DECISION ===")

for i, item in enumerate(lines_data):
    geom = item["geom"]

    rule_flag = (
        len(check_geometry_validity(geom)) > 0 or
        len(detect_abnormal_segments(geom, jump_threshold=2)) > 0
    )

    ml_flag = (preds[i] == -1)

    context_flag = role_based_anomaly(
        {"role": item["role"], "features": item["features"]},
        role_stats
    )

    severity, reason = fuse_decision(
        rule_flag, ml_flag, context_flag
    )

    print(
        f"Line {item['id']} | "
        f"Severity: {severity} | "
        f"Reason: {reason}"
    )
