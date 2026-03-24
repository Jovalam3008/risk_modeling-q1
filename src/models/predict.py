"""Inferencia y scores."""

import numpy as np
from sklearn.base import BaseEstimator


def predict_proba(estimator: BaseEstimator, X) -> np.ndarray:
    """Probabilidad de clase positiva (binario) o matriz completa."""
    proba = estimator.predict_proba(X)
    if proba.ndim == 2 and proba.shape[1] == 2:
        return proba[:, 1]
    return proba
