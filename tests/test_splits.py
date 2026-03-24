import numpy as np
import pandas as pd

from src.validation import splitters


def test_stratified_split_shapes():
    X = np.arange(100).reshape(-1, 1)
    y = np.array([0] * 50 + [1] * 50)
    X_tr, X_te, y_tr, y_te = splitters.stratified_split(X, y, test_size=0.2, random_state=0)
    assert len(X_tr) == 80
    assert len(X_te) == 20
    assert set(np.unique(y_te)) == {0, 1}
