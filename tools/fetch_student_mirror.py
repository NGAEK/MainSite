"""
Скачивает страницы раздела «Учащимся» с ngaek.by и сохраняет
тело статьи (article) в data/students_mirror/<slug>.html для офлайн-отображения.
Запуск из корня проекта: python tools/fetch_student_mirror.py
"""
from __future__ import annotations

import os
import re
import ssl
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from page.student_mirror_config import STUDENT_SOURCE_PATHS as SOURCES  # noqa: E402

OUT_DIR = os.path.join(ROOT, "data", "students_mirror")
BASE = "https://ngaek.by"


def _fetch(url: str) -> str:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "NgaekMirrorFetcher/1.0 (+internal college site migration)"},
    )
    with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _extract_article(html: str) -> str | None:
    m = re.search(
        r'<article\s+class="item-page[^"]*"[^>]*>(.*?)</article>',
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return None
    body = m.group(1)
    body = re.sub(
        r'<div\s+id="js_csc"\s*[^>]*>.*?</div>',
        "",
        body,
        flags=re.DOTALL | re.IGNORECASE,
    )
    body = re.sub(r'<header\s+class="entry-header"[^>]*>.*?</header>', "", body, flags=re.DOTALL | re.IGNORECASE)
    body = body.replace('href="/', f'href="{BASE}/')
    body = body.replace("href='/", f"href='{BASE}/")
    body = body.replace('src="/', f'src="{BASE}/')
    body = body.replace("src='/", f"src='{BASE}/")
    body = body.replace("https://ngaek.by/..\\docs\\", "https://ngaek.by/docs/")
    body = body.replace("https://ngaek.by/../docs/", "https://ngaek.by/docs/")
    body = _sanitize_fragment(body)
    return body.strip()


def _sanitize_fragment(html: str) -> str:
    """Убираем соцкнопки, скрипты и битые хвосты из разметки Joomla."""
    html = re.sub(
        r'<div\s+class="socbuttons"[^>]*>.*?</div>\s*</div>\s*<div\s+style="clear:both;"></div>',
        "",
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"</footer\s*>", "", html, flags=re.IGNORECASE)
    return html


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    for slug, path in SOURCES.items():
        url = f"{BASE}/index.php/ru/{path}"
        print("fetch", slug, "...", flush=True)
        raw = _fetch(url)
        art = _extract_article(raw)
        if not art:
            print("  SKIP: no article", slug)
            continue
        out = os.path.join(OUT_DIR, f"{slug}.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(art)
        print("  ->", out, len(art), "chars")
    print("done.")


if __name__ == "__main__":
    main()
