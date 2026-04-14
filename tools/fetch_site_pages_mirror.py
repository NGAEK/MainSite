"""
Скачивает страницы подпунктов меню с ngaek.by в data/site_pages_mirror.
Запуск из корня проекта: python tools/fetch_site_pages_mirror.py
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

from page.site_mirror_config import SITE_PAGE_MIRROR  # noqa: E402

OUT_DIR = os.path.join(ROOT, "data", "site_pages_mirror")
BASE = "https://ngaek.by"


def _fetch(url: str) -> str:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "NgaekMirrorFetcher/1.0 (+site pages migration)"},
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
        m = re.search(
            r'<div\s+class="item-page[^"]*"[^>]*>(.*?)</div>\s*</main>',
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
    body = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.DOTALL | re.IGNORECASE)
    body = body.replace('href="/', f'href="{BASE}/')
    body = body.replace("href='/", f"href='{BASE}/")
    body = body.replace('src="/', f'src="{BASE}/')
    body = body.replace("src='/", f"src='{BASE}/")
    body = body.replace("https://ngaek.by/..\\docs\\", "https://ngaek.by/docs/")
    body = body.replace("https://ngaek.by/../docs/", "https://ngaek.by/docs/")
    return body.strip()


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    ok_count = 0
    fail_count = 0
    for slug, meta in SITE_PAGE_MIRROR.items():
        legacy_path = (meta.get("legacy_path") or "").strip()
        if not legacy_path:
            print("SKIP", slug, "- empty legacy_path")
            fail_count += 1
            continue
        candidates = [
            f"{BASE}/index.php/ru/{legacy_path}",
            f"{BASE}/index.php/{legacy_path}",
            f"{BASE}/{legacy_path}",
        ]
        print("fetch", slug, "...", flush=True)
        try:
            raw = None
            last_error = None
            for url in candidates:
                try:
                    raw = _fetch(url)
                    break
                except Exception as exc:
                    last_error = exc
            if raw is None:
                raise last_error or RuntimeError("no working source URL")
            art = _extract_article(raw)
            if not art:
                print("  FAIL: no article", slug)
                fail_count += 1
                continue
            out = os.path.join(OUT_DIR, f"{slug}.html")
            with open(out, "w", encoding="utf-8") as f:
                f.write(art)
            print("  ->", out, len(art), "chars")
            ok_count += 1
        except Exception as exc:
            safe_err = str(exc).encode("ascii", "backslashreplace").decode("ascii")
            print("  FAIL:", slug, "-", safe_err)
            fail_count += 1
    print(f"done. ok={ok_count} fail={fail_count}")


if __name__ == "__main__":
    main()

