# -*- coding: utf-8 -*-
"""Inserta una celda markdown antes de cada celda de código en notebooks/01_eda.ipynb."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB_PATH = ROOT / "notebooks" / "01_eda.ipynb"

DOCS = [
    """### Documentación — Configuración e imports

- **`sys.path` / `ROOT`**: permite importar el paquete `src` aunque el kernel se ejecute desde `notebooks/` o la raíz del repo.
- **Librerías**: `numpy`, `pandas`, `matplotlib`, `yaml`; **`scipy.stats`**: `chi2_contingency` (tablas de contingencia) y `ks_2samp` (comparar distribuciones train vs test).
- **`IPython.display.display`**: muestra tablas en el notebook.
- **`src.data.home_credit`**: lectura de CSV y rutas según `configs/home_credit.yaml`.
- **`src.data.quality`**: funciones de calidad (`missing_summary`, `basic_range_checks`).
- **`set_seed(42)`**: alinea con `configs/base.yaml` para muestreos reproducibles en celdas posteriores.
- **Salida**: imprime la raíz del proyecto resuelta por `project_root()`.""",
    """### Documentación — Carga de `application_train` / `application_test`

- **`read_table`**: lee los CSV completos desde `data/raw/` (rutas definidas en config).
- **`y_col`**: nombre de la columna objetivo (`TARGET`), solo presente en train.
- **`k_curr`**: nombre de la clave primaria (`SK_ID_CURR`) para joins y comprobaciones.
- **Salida**: dimensiones de ambos DataFrames y comprobación de que `TARGET` no está en test.""",
    """### Documentación — Distribución del `TARGET` y baselines

- **`value_counts`**: recuentos de clases 0 y 1.
- **Métricas**: proporción de positivos; ratio aproximado entre mayoritaria y minoritaria.
- **Baselines**: accuracy que obtendrías prediciendo siempre 0 o siempre 1 (sin modelo), para contextualizar ROC-AUC posterior.
- **Figuras**: barras de conteos y gráfico circular de proporciones.""",
    """### Documentación — Tipos de datos y cardinalidad

- **`dtypes`**: conteo de tipos por columna en train.
- **`feat_cols`**: todas las columnas excepto `TARGET`.
- **`num_feats` / `obj_cols`**: separación numéricas vs texto (categóricas crudas).
- **Binarias**: columnas numéricas que solo toman 0 y 1 (flags).
- **`card`**: cardinalidad de columnas `object` (orden descendente).
- **Constantes**: columnas con un único valor (poca información marginal).""",
    """### Documentación — Valores faltantes

- **`missing_summary`**: fracción de `NA` por columna (todo el train).
- **Visualización**: barras horizontales de las 25 columnas con más nulos.
- **Bloque siguiente**: para las 30 columnas con más nulos, compara la **tasa de NA** entre filas con `TARGET=0` y `TARGET=1`; si difiere, el patrón de missing puede ser informativo (MNAR / necesidad de indicadores).""",
    """### Documentación — Duplicados e IDs

- **`duplicated()`** sobre `SK_ID_CURR`: debe ser 0 en train y test (un registro por solicitud).
- **Intersección de sets** train vs test: no debe haber IDs compartidos entre archivos (simula el holdout de la competición).""",
    """### Documentación — Alineación de columnas train / test

- **Conjuntos de nombres**: columnas solo en train (p. ej. `TARGET`), solo en test, y comunes.
- **Dtypes**: lista columnas comunes donde `train` y `test` declaran tipos distintos (riesgo al concatenar o al aplicar el mismo pipeline).""",
    """### Documentación — Coherencia de distribuciones (train vs test)

- **`num_common`**: columnas numéricas presentes en ambos conjuntos.
- **Medias**: comparación rápida de `mean_train` vs `mean_test` y diferencia relativa.
- **Kolmogorov–Smirnov (`ks_2samp`)**: contrasta si dos muestras vienen de la misma distribución; aquí se submuestrea hasta 50k filas por lado si hace falta por coste.
- **Interpretación**: p-valores muy bajos o estadísticos KS altos sugieren **deriva** entre train y test en esa variable.""",
    """### Documentación — Volumetría de tablas auxiliares

- **`count_csv_rows`**: cuenta líneas sin cargar el CSV completo en memoria (solo lectura byte a byte).
- **Uso**: dimensionar el trabajo de joins y agregaciones en `bureau`, balances, cuotas, etc.""",
    """### Documentación — Sanity checks de rangos

- **`range_hints`**: intervalos plausibles para scores externos (`EXT_SOURCE_*`), días (`DAYS_BIRTH`, `DAYS_EMPLOYED` con placeholder 365243).
- **`basic_range_checks`**: comprueba que valores no nulos caen en el rango (o marca REVISAR).
- **Percentiles de `DAYS_BIRTH`**: contexto si el check rígido falla por valores límite.""",
    """### Documentación — Asociación con `TARGET` (numéricas y categóricas)

- **Pearson**: correlación lineal de cada numérica con `TARGET`; ordena por valor absoluto.
- **Heatmap**: matriz de correlación entre las **top 25** variables por |corr| con `TARGET` más la propia `TARGET` (dependencias lineales entre candidatos a feature).
- **Cramér V**: a partir de `chi2_contingency` sobre tablas cruzadas categoría × `TARGET`; mide asociación 0–1 en categóricas.
- **Tablas por grupo**: tasa de default (`mean` de `TARGET`) y volumen `n` para variables de negocio (`CODE_GENDER`, etc.).""",
    """### Documentación — Histogramas `EXT_SOURCE_*`

- Para cada `EXT_SOURCE` disponible, superpone histogramas por clase (`TARGET` 0 vs 1) en [0, 1].
- **Densidad** (`density=True`): comparar formas aunque los tamaños de clase difieran.""",
    """### Documentación — Agregación mínima de `bureau`

- Lee solo **`SK_ID_CURR`** de `bureau.csv` para contar cuántos registros de buró tiene cada cliente.
- **Merge** con train: añade `n_bureau_records` (0 si no hay filas en buró).
- **Deciles** (`qcut`) con `duplicates="drop"` si hay empates: tasa de default por franja de volumen de historial en buró.""",
    """### Documentación — Heurística de nombres (leakage)

- Busca subcadenas en mayúsculas (`TARGET`, `DEFAULT`, etc.) en nombres de columnas para revisión manual.
- **`FLAG_DOCUMENT_*`**: cuenta documentos aportados; no implica leakage por sí solo, pero conviene documentar en el informe técnico.""",
    """### Documentación — Reproducibilidad del pipeline

- Lee **`configs/base.yaml`** y muestra semilla, fracciones de split y métricas previstas.
- **Uso**: trazabilidad entre este EDA y la validación/modelado en otros notebooks.""",
]


def to_source_lines(text: str) -> list[str]:
    return [line + "\n" for line in text.strip().split("\n")]


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding="utf-8"))
    if any(
        "### Documentación — Configuración e imports" in "".join(c.get("source", []))
        for c in nb["cells"]
    ):
        print("El notebook ya incluye celdas de documentación; no se modifica.")
        return
    new_cells: list[dict] = []
    doc_idx = 0
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            if doc_idx >= len(DOCS):
                raise RuntimeError(f"More code cells than docs: {doc_idx}")
            new_cells.append(
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": to_source_lines(DOCS[doc_idx]),
                }
            )
            doc_idx += 1
        new_cells.append(c)
    if doc_idx != len(DOCS):
        raise RuntimeError(f"Doc count mismatch: used {doc_idx}, expected {len(DOCS)}")
    nb["cells"] = new_cells
    NB_PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    try:
        import nbformat
        from nbformat.validator import normalize

        nbr = nbformat.read(NB_PATH, as_version=4)
        normalize(nbr)
        nbformat.write(nbr, NB_PATH)
    except Exception as e:
        print("nbformat normalize:", e)
    print("Done:", NB_PATH, "cells:", len(new_cells))


if __name__ == "__main__":
    main()
