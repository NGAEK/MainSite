"""Вспомогательные функции для URL с языком (hreflang, тестируемо без Flask)."""
from urllib.parse import urlencode


def build_hreflang_url(url_root: str, path: str, query_args: dict, lang: str) -> str:
    """Собирает абсолютный URL той же страницы с подстановкой lang=."""
    args = dict(query_args)
    args["lang"] = lang
    qs = urlencode(sorted((k, v) for k, v in args.items() if v is not None and v != ""))
    base = (url_root or "").rstrip("/")
    p = path if path.startswith("/") else "/" + path
    return f"{base}{p}?{qs}" if qs else f"{base}{p}"
