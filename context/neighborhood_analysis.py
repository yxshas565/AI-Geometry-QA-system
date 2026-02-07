# context/neighborhood_analysis.py

import numpy as np

def compute_role_statistics(lines_with_features):
    role_stats = {}

    for item in lines_with_features:
        role = item["role"]
        ratio = item["features"]["length_ratio"]

        role_stats.setdefault(role, []).append(ratio)

    return {
        role: {
            "mean": np.mean(vals),
            "std": np.std(vals)
        }
        for role, vals in role_stats.items()
    }


def role_based_anomaly(item, role_stats, z_thresh=2.5):
    role = item["role"]
    ratio = item["features"]["length_ratio"]

    stats = role_stats.get(role)
    if not stats or stats["std"] == 0:
        return False

    z_score = abs(ratio - stats["mean"]) / stats["std"]
    return z_score > z_thresh
