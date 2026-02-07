from geometry.parser import load_geometry
from features.extractor import extract_line_features
from context.role_classifier import classify_line_role
from context.neighborhood_analysis import (
    compute_role_statistics,
    role_based_anomaly
)

# --- Load WKT data ---
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

# --- Extract features + roles ---
lines_data = []

for idx, wkt in enumerate(wkts):
    try:
        geom = load_geometry(wkt)
        features = extract_line_features(geom)
        role = classify_line_role(features)

        lines_data.append({
            "id": idx + 1,
            "features": features,
            "role": role
        })
    except:
        continue

# --- Compute role-level statistics ---
role_stats = compute_role_statistics(lines_data)

print("=== ROLE STATISTICS ===")
for role, stats in role_stats.items():
    print(f"{role}: mean={round(stats['mean'], 2)}, std={round(stats['std'], 2)}")

print("\n=== CONTEXTUAL ANOMALY CHECK ===")

for item in lines_data:
    is_context_anomaly = role_based_anomaly(item, role_stats)

    status = "⚠️ CONTEXT ANOMALY" if is_context_anomaly else "✅ CONTEXT OK"

    print(
        f"Line {item['id']} | Role={item['role']} | "
        f"length_ratio={round(item['features']['length_ratio'], 2)} | {status}"
    )
