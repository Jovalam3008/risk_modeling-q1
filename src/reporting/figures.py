"""Utilidades para figuras reutilizables."""

import matplotlib.pyplot as plt


def save_fig(path: str, dpi: int = 150) -> None:
    """Guarda la figura actual."""
    plt.savefig(path, dpi=dpi, bbox_inches="tight")
