import re
from flask import render_template, redirect
import logging
from db import news_repository, pages_repository, tabs_repository
from util.locale_search import href_with_lang, search_localized_site


def _unified_search_matches(query: str, lang: str, news_results, page_results, locale_results) -> list[dict]:
    """Один список: БД (страницы, вкладки, новости) + совпадения в messages.json."""
    matches: list[dict] = []
    for p in page_results:
        matches.append(
            {
                "kind": "page",
                "title": p["title"],
                "excerpt": (p.get("excerpt") or "").strip(),
                "href": href_with_lang(p["url"], "", lang),
            }
        )
    for n in news_results:
        desc = n.localized_description(lang)
        matches.append(
            {
                "kind": "news",
                "title": n.localized_name(lang),
                "excerpt": _make_excerpt(desc, query),
                "href": href_with_lang(f"/news/{n.id}", "", lang),
            }
        )
    for h in locale_results:
        matches.append(
            {
                "kind": "locale",
                "title": h["title"],
                "excerpt": (h.get("excerpt") or "").strip(),
                "href": h["href"],
            }
        )
    return matches

logger = logging.getLogger(__name__)

_SUPPORTED = frozenset({'ru', 'be', 'en'})
# Максимальная длина отрывка текста из страницы (в символах)
_EXCERPT_LEN = 200
# Тег-мусор: удаляем HTML из content_html перед показом отрывка
_TAG_RE = re.compile(r'<[^>]+>')


def _strip_html(html: str) -> str:
    """Убирает HTML-теги для отображения чистого текста-превью."""
    return _TAG_RE.sub(' ', html or '').strip()


def _make_excerpt(text: str, query: str, length: int = _EXCERPT_LEN) -> str:
    """Возвращает отрывок текста вокруг первого вхождения запроса."""
    clean = _strip_html(text)
    idx = clean.lower().find(query.lower())
    if idx == -1:
        return clean[:length] + ('…' if len(clean) > length else '')
    start = max(0, idx - length // 3)
    end = min(len(clean), start + length)
    excerpt = clean[start:end]
    if start > 0:
        excerpt = '…' + excerpt
    if end < len(clean):
        excerpt = excerpt + '…'
    return excerpt


def search_handler(request):
    """Обработчик страницы поиска: новости, страницы site_pages и динамические вкладки site_tabs."""
    query = request.args.get('q', '').strip()
    lang = request.args.get('lang') or request.cookies.get('locale', 'ru')
    if lang not in _SUPPORTED:
        lang = 'ru'

    if not query:
        if lang == 'ru':
            return redirect('/')
        return redirect(f'/?lang={lang}')

    news_results = []
    page_results = []
    seen_page_slugs: set[str] = set()

    try:
        news_results = news_repository.search_news(query)
    except Exception as e:
        logger.error(f"DB: Ошибка поиска по новостям (БД отключена?): {e}")

    try:
        raw_pages = pages_repository.search_pages(query)
        for p in raw_pages:
            slug = p["slug"]
            seen_page_slugs.add(slug)
            page_results.append({
                "id": p["id"],
                "slug": slug,
                "title": p["title"],
                "excerpt": _make_excerpt(p.get("content_html") or "", query),
                "url": f"/pages/{slug}",
            })
    except Exception as e:
        logger.error(f"DB: Ошибка поиска по страницам (БД отключена?): {e}")

    try:
        raw_tabs = tabs_repository.search_tabs(query)
        for t in raw_tabs:
            slug = t["slug"]
            if slug in seen_page_slugs:
                continue
            seen_page_slugs.add(slug)
            page_results.append({
                "id": t["id"],
                "slug": slug,
                "title": t["title"],
                "excerpt": _make_excerpt(t.get("content_html") or "", query),
                "url": f"/pages/{slug}",
            })
    except Exception as e:
        logger.error(f"DB: Ошибка поиска по вкладкам (БД отключена?): {e}")

    locale_results = search_localized_site(query, lang)
    all_matches = _unified_search_matches(query, lang, news_results, page_results, locale_results)

    return render_template(
        'search/results.html',
        query=query,
        all_matches=all_matches,
    )
