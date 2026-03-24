"""Joins y agregaciones para construir el dataset de modelado.

Home Credit — relaciones entre tablas (una fila final por `SK_ID_CURR` en train/test):

- ``application_{train|test}``: clave ``SK_ID_CURR``; ``TARGET`` solo en train.
- ``bureau`` → ``application`` por ``SK_ID_CURR``; ``bureau_balance`` → ``bureau`` por ``SK_ID_BUREAU``.
- ``previous_application`` → ``application`` por ``SK_ID_CURR``.
- ``POS_CASH_balance``, ``installments_payments``, ``credit_card_balance`` → ``previous_application`` por ``SK_ID_PREV``.

Las tablas de balance/comportamiento requieren agregaciones (por cliente o por préstamo previo) antes de unir al nivel aplicación.
"""

import pandas as pd


def build_dataset(*frames: pd.DataFrame, on: str | list[str], how: str = "inner") -> pd.DataFrame:
    """Une tablas intermedias en un único DataFrame (stub)."""
    if not frames:
        raise ValueError("Se requiere al menos un DataFrame")
    out = frames[0]
    for other in frames[1:]:
        out = out.merge(other, on=on, how=how)
    return out
