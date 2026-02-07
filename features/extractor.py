# features/extractor.py

import numpy as np
from shapely.geometry import LineString

def extract_line_features(line: LineString):
    coords = list(line.coords)
    num_points = len(coords)

    segment_lengths = []
    for i in range(num_points - 1):
        x1, y1 = coords[i]
        x2, y2 = coords[i + 1]
        length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        segment_lengths.append(length)

    total_length = sum(segment_lengths)
    avg_segment_length = np.mean(segment_lengths)
    max_segment_length = np.max(segment_lengths)

    minx, miny, maxx, maxy = line.bounds
    bbox_area = (maxx - minx) * (maxy - miny)

    length_ratio = max_segment_length / avg_segment_length if avg_segment_length > 0 else 0

    return {
        "num_points": num_points,
        "total_length": total_length,
        "avg_segment_length": avg_segment_length,
        "max_segment_length": max_segment_length,
        "length_ratio": length_ratio,
        "bbox_area": bbox_area
    }
