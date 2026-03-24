"""Orquestación de construcción de matriz de features."""

import pandas as pd


def build_feature_matrix(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """Selecciona columnas de features (extender con pipelines)."""
    return df[feature_cols].copy()
