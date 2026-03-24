"""Entrenamiento de modelos."""

from sklearn.base import BaseEstimator


def train_estimator(estimator: BaseEstimator, X, y, **fit_kwargs) -> BaseEstimator:
    """Ajusta el estimador y lo devuelve."""
    estimator.fit(X, y, **fit_kwargs)
    return estimator
