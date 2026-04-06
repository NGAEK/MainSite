from flask import render_template, redirect
import logging
from db import news_repository

logger = logging.getLogger(__name__)

_SUPPORTED = frozenset({'ru', 'be', 'en'})


def search_handler(request):
    """Обработчик страницы поиска"""
    query = request.args.get('q', '').strip()
    lang = request.args.get('lang') or request.cookies.get('locale', 'ru')
    if lang not in _SUPPORTED:
        lang = 'ru'

    if not query:
        if lang == 'ru':
            return redirect('/')
        return redirect(f'/?lang={lang}')
    
    try:
        results = news_repository.search_news(query)
    except Exception as e:
        logger.error(f"Ошибка поиска: {e}")
        return "Internal Server Error", 500
    
    data = {
        'title': 'Результаты поиска',
        'query': query,
        'results': results
    }
    
    return render_template('search/results.html', **data)

