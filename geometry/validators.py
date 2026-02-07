# geometry/validators.py

from shapely.geometry import LineString

def check_geometry_validity(geom):
    """
    Check basic geometry validity
    """
    issues = []

    if geom.is_empty:
        issues.append("Geometry is empty")

    if not geom.is_valid:
        issues.append("Geometry is invalid (self-intersection or corruption)")

    if isinstance(geom, LineString):
        if geom.length == 0:
            issues.append("Zero-length line detected")

    return issues


def detect_abnormal_segments(line, jump_threshold=5):
    """
    Detect segments that are abnormally long compared to average
    """
    coords = list(line.coords)
    segment_lengths = []

    for i in range(len(coords) - 1):
        x1, y1 = coords[i]
        x2, y2 = coords[i + 1]
        length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        segment_lengths.append(length)

    avg_length = sum(segment_lengths) / len(segment_lengths)

    abnormal_segments = []
    for idx, length in enumerate(segment_lengths):
        if length > jump_threshold * avg_length:
            abnormal_segments.append((idx, length))

    return abnormal_segments


