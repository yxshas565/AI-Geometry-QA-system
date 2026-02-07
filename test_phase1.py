from geometry.parser import load_geometry
from geometry.validators import (
    check_geometry_validity,
    detect_abnormal_segments
)

# -----------------------------
# Test Case: Broken Line Geometry
# -----------------------------
wkt_line = "LINESTRING (0 0, 1 1, 2 2, 100 100)"

geom = load_geometry(wkt_line)

print("=== PHASE 1 TEST OUTPUT ===")
print("Validity Issues:")
print(check_geometry_validity(geom))

print("\nAbnormal Segments:")
print(detect_abnormal_segments(geom))
print(detect_abnormal_segments(geom, jump_threshold=2))