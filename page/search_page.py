import re
from flask import render_template, redirect
import logging
from db import news_repository, pages_repository

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
    """Обработчик страницы поиска. Ищет по новостям и страницам сайта."""
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

    try:
        news_results = news_repository.search_news(query)
    except Exception as e:
        logger.error(f"DB: Ошибка поиска по новостям (БД отключена?): {e}")

    try:
        raw_pages = pages_repository.search_pages(query)
        for p in raw_pages:
            page_results.append({
                'id':      p['id'],
                'slug':    p['slug'],
                'title':   p['title'],
                'excerpt': _make_excerpt(p.get('content_html') or '', query),
                'url':     f"/pages/{p['slug']}",
            })
    except Exception as e:
        logger.error(f"DB: Ошибка поиска по страницам (БД отключена?): {e}")

    return render_template(
        'search/results.html',
        query=query,
        results=news_results,
        page_results=page_results,
    )
