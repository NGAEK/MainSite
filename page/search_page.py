from flask import render_template, redirect
import logging
from db import news_repository

logger = logging.getLogger(__name__)


def search_handler(request):
    """Обработчик страницы поиска"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return redirect('/')
    
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

