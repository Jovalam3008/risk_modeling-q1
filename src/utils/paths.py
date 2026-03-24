"""Resolución de paths del proyecto."""

from pathlib import Path


def project_root() -> Path:
    """Raíz del repo (directorio que contiene `pyproject.toml`)."""
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    return Path.cwd()
