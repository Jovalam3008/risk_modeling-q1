"""CV y reporting."""

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.model_selection import StratifiedKFold, cross_val_score


def stratified_kfold_scores(
    estimator: BaseEstimator,
    X,
    y,
    scoring: str = "roc_auc",
    n_splits: int = 5,
    random_state: int | None = None,
) -> np.ndarray:
    """Scores por fold con StratifiedKFold."""
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    return cross_val_score(estimator, X, y, cv=cv, scoring=scoring)
