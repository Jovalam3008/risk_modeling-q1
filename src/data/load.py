"""Lectura de datos, tipado y esquemas."""

from pathlib import Path

import pandas as pd


def read_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """Lee CSV con opciones por defecto sensatas."""
    return pd.read_csv(path, **kwargs)
