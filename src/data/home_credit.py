"""Home Credit Default Risk: rutas, claves y lectura de tablas."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.utils.paths import project_root

_CONFIG_REL = Path("configs") / "home_credit.yaml"


@lru_cache(maxsize=1)
def load_home_credit_config() -> dict[str, Any]:
    """Carga `configs/home_credit.yaml`."""
    path = project_root() / _CONFIG_REL
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def raw_dir() -> Path:
    cfg = load_home_credit_config()
    return project_root() / cfg["paths"]["raw"]


def table_path(table_key: str) -> Path:
    """Path absoluto a un CSV en `data/raw` según la clave en `files`."""
    cfg = load_home_credit_config()
    name = cfg["files"][table_key]
    return raw_dir() / name


def keys() -> dict[str, str]:
    return dict(load_home_credit_config()["keys"])


def target_column() -> str:
    return str(load_home_credit_config()["target"])


def read_table(table_key: str, **read_csv_kwargs) -> pd.DataFrame:
    """Lee un CSV del dataset (p. ej. `application_train`, `bureau`)."""
    return pd.read_csv(table_path(table_key), **read_csv_kwargs)


def read_column_descriptions(**read_csv_kwargs) -> pd.DataFrame:
    """Diccionario de columnas (`HomeCredit_columns_description.csv`)."""
    return read_table("column_descriptions", **read_csv_kwargs)


def read_sample_submission(**read_csv_kwargs) -> pd.DataFrame:
    """Plantilla de envío Kaggle."""
    return read_table("sample_submission", **read_csv_kwargs)
