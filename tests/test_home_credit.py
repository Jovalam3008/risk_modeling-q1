from pathlib import Path

from src.data import home_credit
from src.utils.paths import project_root


def test_config_loads():
    cfg = home_credit.load_home_credit_config()
    assert cfg["dataset"]["name"] == "home_credit_default_risk"
    assert "SK_ID_CURR" in cfg["keys"].values()


def test_raw_csv_paths_exist():
    root = project_root()
    for key in (
        "application_train",
        "application_test",
        "bureau",
        "bureau_balance",
        "previous_application",
        "pos_cash_balance",
        "installments_payments",
        "credit_card_balance",
        "column_descriptions",
        "sample_submission",
    ):
        p = home_credit.table_path(key)
        assert p.is_file(), f"Falta {key}: {p} (raíz del proyecto: {root})"


def test_target_column():
    assert home_credit.target_column() == "TARGET"
