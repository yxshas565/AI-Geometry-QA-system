from geometry.parser import load_geometry
from geometry.validators import check_geometry_validity, detect_abnormal_segments
from features.extractor import extract_line_features

wkts = []
current_wkt = ""

with open("data/raw/lines.wkt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        current_wkt += " " + line

        if line.endswith(")"):
            wkts.append(current_wkt.strip())
            current_wkt = ""

print(f"Total geometries loaded: {len(wkts)}\n")

for idx, wkt in enumerate(wkts):
    try:
        geom = load_geometry(wkt)
    except ValueError:
        print(f"LINE {idx+1}: ❌ INVALID WKT – skipped")
        continue

    validity_issues = check_geometry_validity(geom)
    abnormal_segments = detect_abnormal_segments(geom, jump_threshold=2)
    features = extract_line_features(geom)

    # --- DECISION LOGIC ---
    is_flagged = len(abnormal_segments) > 0

    print(f"--- LINE {idx+1} ---")

    if validity_issues:
        print("STATUS: ❌ INVALID GEOMETRY")
        print("Issues:", validity_issues)

    elif is_flagged:
        print("STATUS: ⚠️ FLAGGED – INVESTIGATE")
        for seg_idx, seg_len in abnormal_segments:
            print(
                f"  → Abnormal segment at index {seg_idx} "
                f"(length = {round(seg_len, 2)})"
            )

    else:
        print("STATUS: ✅ SAFE – geometry passed QA")

    print("Feature Summary:", {
        "num_points": features["num_points"],
        "length_ratio": round(features["length_ratio"], 2)
    })
    print()

