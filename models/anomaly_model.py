# models/anomaly_model.py

import numpy as np
from sklearn.ensemble import IsolationForest

class GeometryAnomalyDetector:
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42
        )

    def fit(self, feature_matrix):
        self.model.fit(feature_matrix)

    def predict(self, feature_matrix):
        """
        Returns:
        - predictions: -1 (anomaly), 1 (normal)
        - scores: anomaly scores (lower = more anomalous)
        """
        predictions = self.model.predict(feature_matrix)
        scores = self.model.decision_function(feature_matrix)
        return predictions, scores
