"""Splits estratificados y time-aware."""

import pandas as pd
from sklearn.model_selection import train_test_split


def stratified_split(
    X,
    y,
    test_size: float = 0.2,
    random_state: int | None = None,
    stratify=None,
):
    """Train/test estratificado."""
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify if stratify is not None else y,
    )


def time_based_split(df: pd.DataFrame, time_col: str, test_frac: float = 0.2):
    """Parte por tiempo: primeros (1-test_frac) train, últimos test."""
    df = df.sort_values(time_col)
    n = len(df)
    cut = int(n * (1 - test_frac))
    train_df, test_df = df.iloc[:cut], df.iloc[cut:]
    return train_df, test_df
