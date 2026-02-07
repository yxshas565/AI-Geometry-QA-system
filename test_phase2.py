from geometry.parser import load_geometry
from features.extractor import extract_line_features

wkt_line = "LINESTRING (0 0, 1 1, 2 2, 100 100)"

geom = load_geometry(wkt_line)
features = extract_line_features(geom)

print("=== PHASE 2 FEATURE OUTPUT ===")
for k, v in features.items():
    print(f"{k}: {v}")
