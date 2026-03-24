# Risk modeling — Q1

Proyecto de modelado de riesgo con pipeline reproducible: datos, features, entrenamiento, calibración y reporting.

## Dataset: Home Credit Default Risk

Home Credit Group busca ampliar la inclusión financiera para personas con historial crediticio insuficiente o inexistente, usando datos alternativos (p. ej. telecomunicaciones y transacciones) para estimar la capacidad de pago.

**Evaluación (Kaggle):** el envío se puntúa con **ROC-AUC** entre la probabilidad predicha y el `TARGET` observado.

**Archivo de envío:** cabecera `SK_ID_CURR,TARGET` y una fila por cada ID del test (ver `data/raw/sample_submission.csv`).

### Tablas y relaciones

| Tabla | Rol | Clave(s) |
|-------|-----|----------|
| `application_train.csv` / `application_test.csv` | Tabla principal; estática por solicitud. `TARGET` solo en train. | `SK_ID_CURR` |
| `bureau.csv` | Créditos previos en buró (otras entidades) | `SK_ID_CURR` → application |
| `bureau_balance.csv` | Saldos mensuales por crédito de buró | `SK_ID_BUREAU` → bureau |
| `previous_application.csv` | Solicitudes previas en Home Credit | `SK_ID_CURR` → application |
| `POS_CASH_balance.csv` | Saldos mensuales POS/cash (HC) | `SK_ID_PREV` → previous_application |
| `installments_payments.csv` | Historial de cuotas (pagos e impagos) | `SK_ID_PREV` → previous_application |
| `credit_card_balance.csv` | Saldos mensuales de tarjetas (HC) | `SK_ID_PREV` → previous_application |
| `HomeCredit_columns_description.csv` | Descripción de columnas por tabla | — |

Las tablas de comportamiento (balances, cuotas) tienen **múltiples filas por cliente**; suele agregarse (medias, conteos, tendencias) antes de unir a nivel `SK_ID_CURR`.

### Ubicación de los datos

Los CSV viven en **`data/raw/`** (no versionar ficheros pesados en git; el `.gitignore` ignora el contenido salvo `.gitkeep`).

Metadatos y nombres de archivo: **`configs/home_credit.yaml`**. En código, rutas y lectura: `src.data.home_credit` (`table_path`, `read_table`, etc.).

## Requisitos

- Python 3.10+
- Ver `pyproject.toml` para dependencias.

## Uso rápido

```bash
pip install -e ".[dev]"
python -m pytest
```

Con `make` (Linux/macOS/Git Bash): `make install-dev` y `make test`.

## Configuración

- `configs/base.yaml` — paths genéricos, seeds, splits, métricas.
- `configs/home_credit.yaml` — ficheros del dataset, claves, métrica de evaluación.
- `configs/model_*.yaml`, `configs/thresholds.yaml` — modelos y umbrales.

## Estructura del repo

- `src/` — código fuente (datos, features, modelos, validación, reporting, utils).
- `notebooks/` — EDA, feature engineering, modeling, error analysis.
- `reports/` — figuras, model cards, informe técnico.
- `artifacts/` — modelos serializados, métricas, calibración.
