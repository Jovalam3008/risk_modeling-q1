import pandas as pd

from src.data import quality


def test_missing_summary():
    df = pd.DataFrame({"a": [1.0, None], "b": ["x", "y"]})
    s = quality.missing_summary(df)
    assert s["a"] == 0.5
    assert s["b"] == 0.0


def test_basic_range_checks():
    df = pd.DataFrame({"x": [0, 1, 2]})
    ok = quality.basic_range_checks(df, {"x": (0, 2)})
    assert ok["x"]
