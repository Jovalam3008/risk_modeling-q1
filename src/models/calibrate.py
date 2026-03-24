"""Calibración Platt / Isotónica."""

import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression


def platt_scaler(y_true: np.ndarray, y_score: np.ndarray) -> LogisticRegression:
    """Ajusta regresión logística sobre scores (Platt scaling)."""
    lr = LogisticRegression()
    lr.fit(y_score.reshape(-1, 1), y_true)
    return lr


def isotonic_calibrator(y_true: np.ndarray, y_score: np.ndarray) -> IsotonicRegression:
    """Calibración isotónica monótona."""
    iso = IsotonicRegression(out_of_bounds="clip")
    iso.fit(y_score, y_true)
    return iso


def sklearn_calibrated_classifier(base_estimator, X, y, method: str = "sigmoid", cv: int = 3):
    """Wrapper sklearn CalibratedClassifierCV."""
    cal = CalibratedClassifierCV(base_estimator, method=method, cv=cv)
    cal.fit(X, y)
    return cal
