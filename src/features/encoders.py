"""Encoders categóricos (target, one-hot, etc.)."""

from sklearn.preprocessing import OneHotEncoder


def make_one_hot_encoder(**kwargs) -> OneHotEncoder:
    return OneHotEncoder(handle_unknown="ignore", sparse_output=False, **kwargs)
