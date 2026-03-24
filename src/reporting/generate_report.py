"""Export de informes a HTML/PDF."""

from pathlib import Path


def write_html_stub(path: str | Path, title: str, body: str) -> None:
    """Escribe un HTML mínimo (extender con plantillas)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title></head>
<body><h1>{title}</h1>{body}</body></html>
"""
    path.write_text(html, encoding="utf-8")
