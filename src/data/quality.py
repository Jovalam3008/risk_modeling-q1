"""Comprobaciones de calidad: missing, rangos, etc."""

from typing import Any

import pandas as pd


def missing_summary(df: pd.DataFrame) -> pd.Series:
    """Fracción de valores nulos por columna."""
    return df.isna().mean()


def basic_range_checks(df: pd.DataFrame, ranges: dict[str, tuple[Any, Any]]) -> dict[str, bool]:
    """Verifica que columnas numéricas estén en [low, high] cuando existen en `ranges`."""
    out: dict[str, bool] = {}
    for col, (low, high) in ranges.items():
        if col not in df.columns:
            continue
        s = df[col].dropna()
        out[col] = bool(s.empty) or bool(((s >= low) & (s <= high)).all())
    return out
