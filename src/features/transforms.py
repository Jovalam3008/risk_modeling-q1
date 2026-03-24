"""Transformaciones de features (log, binning, etc.)."""

import numpy as np
import pandas as pd


def log1p_safe(s: pd.Series) -> pd.Series:
    return np.log1p(s.clip(lower=0))
