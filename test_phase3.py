import numpy as np

from geometry.parser import load_geometry
from features.extractor import extract_line_features
from models.anomaly_model import GeometryAnomalyDetector

# --- Load real data ---
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

# --- Extract features ---
feature_list = []
valid_geoms = []

for wkt in wkts:
    try:
        geom = load_geometry(wkt)
        features = extract_line_features(geom)
        feature_vector = [
            features["num_points"],
            features["total_length"],
            features["avg_segment_length"],
            features["max_segment_length"],
            features["length_ratio"],
            features["bbox_area"]
        ]
        feature_list.append(feature_vector)
        valid_geoms.append(wkt)
    except:
        continue

X = np.array(feature_list)

# --- Train ML model ---
detector = GeometryAnomalyDetector(contamination=0.05)
detector.fit(X)

predictions, scores = detector.predict(X)

# --- Output results ---
print("=== PHASE 3 ML OUTPUT ===")

for i, (pred, score) in enumerate(zip(predictions, scores)):
    status = "⚠️ FLAGGED (ANOMALY)" if pred == -1 else "✅ SAFE"
    print(f"Line {i+1}: {status} | Anomaly Score = {round(score, 3)}")
