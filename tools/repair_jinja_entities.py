#!/usr/bin/env python3
"""Исправляет HTML-сущности (&gt; и т.д.) внутри тегов Jinja в templates/*.html."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from api.template_guard import sanitize_jinja_html_entities  # noqa: E402


def main() -> None:
    templates = ROOT / "templates"
    changed = 0
    for path in sorted(templates.rglob("*.html")):
        raw = path.read_text(encoding="utf-8")
        fixed = sanitize_jinja_html_entities(raw)
        if fixed != raw:
            path.write_text(fixed, encoding="utf-8")
            print(f"fixed: {path.relative_to(ROOT)}")
            changed += 1
    print(f"Готово. Изменено файлов: {changed}")


if __name__ == "__main__":
    main()
