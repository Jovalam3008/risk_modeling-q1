"""
One-off script: insert TOC + numbered ## sections with stable HTML anchors in 01_eda.ipynb.
"""
from __future__ import annotations

import json
from pathlib import Path

NB = Path(__file__).resolve().parents[1] / "notebooks" / "01_eda.ipynb"

# (old_first_line_prefix_or_exact, new_source_lines) for markdown cells that start with ##
SECTION_UPDATES: list[tuple[str, list[str]]] = [
    (
        "## Fuentes de datos\n",
        [
            '<a id="sec-1"></a>\n',
            "## 1. Fuentes de datos\n",
            "\n",
        ],
    ),
    (
        "## Tabla principal `application_train` / `application_test`\n",
        [
            '<a id="sec-2"></a>\n',
            "## 2. Tabla principal `application_train` / `application_test`\n",
            "\n",
        ],
    ),
    (
        "## Valores faltantes\n",
        [
            '<a id="sec-3"></a>\n',
            "## 3. Valores faltantes\n",
            "\n",
        ],
    ),
    (
        "## Calidad: duplicados e IDs\n",
        [
            '<a id="sec-4"></a>\n',
            "## 4. Calidad: duplicados e IDs\n",
            "\n",
        ],
    ),
    (
        "## Otras tablas (volumen)\n",
        [
            '<a id="sec-5"></a>\n',
            "## 5. Otras tablas (volumen)\n",
            "\n",
        ],
    ),
    (
        "## Rangos plausibles (sanity checks)\n",
        [
            '<a id="sec-6"></a>\n',
            "## 6. Rangos plausibles (sanity checks)\n",
            "\n",
        ],
    ),
    (
        "## Asociación con `TARGET`\n",
        [
            '<a id="sec-7"></a>\n',
            "## 7. Asociación con `TARGET`\n",
            "\n",
        ],
    ),
    (
        "## Auditoría preliminar de leakage (`application_*`)\n",
        [
            '<a id="sec-8"></a>\n',
            "## 8. Auditoría preliminar de leakage (`application_*`)\n",
            "\n",
        ],
    ),
    (
        "## Reproducibilidad\n",
        [
            '<a id="sec-9"></a>\n',
            "## 9. Reproducibilidad\n",
            "\n",
        ],
    ),
    (
        "## EDA univariado, bivariado y multivariado\n",
        [
            '<a id="sec-10"></a>\n',
            "## 10. EDA univariado, bivariado y multivariado\n",
            "\n",
        ],
    ),
    (
        "## EDA premium (estadística avanzada)\n",
        [
            '<a id="sec-11"></a>\n',
            "## 11. EDA premium (estadística avanzada)\n",
            "\n",
        ],
    ),
    (
        "## Resumen y siguientes pasos\n",
        [
            '<a id="sec-12"></a>\n',
            "## 12. Resumen y siguientes pasos\n",
            "\n",
        ],
    ),
]

TOC_CELL = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Índice\n",
        "\n",
        "Flujo del notebook: contexto y datos → calidad y coherencia train/test → volumetría y rangos → "
        "asociación con `TARGET` y tablas auxiliares → auditoría de leakage → reproducibilidad → "
        "EDA uni/bi/multi → análisis avanzado → cierre.\n",
        "\n",
        "| # | Sección |\n",
        "|---|--------|\n",
        "| 1 | [Fuentes de datos](#sec-1) |\n",
        "| 2 | [Tabla principal `application_*`](#sec-2) |\n",
        "| 3 | [Valores faltantes](#sec-3) |\n",
        "| 4 | [Calidad: duplicados e IDs](#sec-4) |\n",
        "| 5 | [Otras tablas (volumen)](#sec-5) |\n",
        "| 6 | [Rangos plausibles (sanity checks)](#sec-6) |\n",
        "| 7 | [Asociación con `TARGET`](#sec-7) |\n",
        "| 8 | [Auditoría preliminar de leakage](#sec-8) |\n",
        "| 9 | [Reproducibilidad](#sec-9) |\n",
        "| 10 | [EDA univariado, bivariado y multivariado](#sec-10) |\n",
        "| 11 | [EDA premium (estadística avanzada)](#sec-11) |\n",
        "| 12 | [Resumen y siguientes pasos](#sec-12) |\n",
        "\n",
        "Las celdas **Documentación — …** preceden cada bloque de código y explican qué hace ese bloque.\n",
    ],
}


def apply_section_updates(source: list[str]) -> list[str] | None:
    if not source:
        return None
    first = source[0]
    for old_prefix, new_head in SECTION_UPDATES:
        if first == old_prefix or first.rstrip("\n") == old_prefix.rstrip("\n"):
            return new_head + source[1:]
    return None


def main() -> None:
    text = NB.read_text(encoding="utf-8")
    nb = json.loads(text)

    # Insert TOC after first cell if not already present
    cells = nb["cells"]
    if len(cells) > 1 and cells[1].get("cell_type") == "markdown":
        src1 = "".join(cells[1].get("source", []))
        if src1.strip().startswith("## Índice"):
            print("TOC already present, skipping insert")
        else:
            cells.insert(1, {**TOC_CELL, "id": None})
            # nbformat will assign id on save if needed
            print("Inserted TOC at index 1")
    else:
        cells.insert(1, {**TOC_CELL, "id": None})
        print("Inserted TOC at index 1")

    updated = 0
    for cell in nb["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        src = cell.get("source", [])
        if isinstance(src, str):
            src = [src]
        new_src = apply_section_updates(src)
        if new_src is not None:
            cell["source"] = new_src
            updated += 1

    NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Updated {updated} section headers")


if __name__ == "__main__":
    main()
