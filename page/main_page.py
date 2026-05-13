from flask import render_template
import logging
from db import news_repository
import re

logger = logging.getLogger(__name__)


def home_handler(request):
    """Обработчик главной страницы"""
    try:
        all_news = news_repository.get_all_news()
    except Exception as e:
        logger.warning(f"DB: Ошибка загрузки новостей (БД отключена?): {e}. Используется пустой список.")
        all_news = []
    
    query = request.args.get('q', '').strip()

    filtered_news = []
    is_search_results = False
    
    if query:
        is_search_results = True
        try:
            db_results = news_repository.search_news(query)
            filtered_news = db_results
        except Exception as e:
            logger.warning(f"DB: Ошибка поиска в БД (БД отключена?): {e}")
            # Если ошибка в БД, фильтруем локально (из пустого списка ничего не найдётся)
            query_lower = query.lower()

            def _texts(n):
                for attr in (
                    "name", "description", "name_be", "name_en",
                    "description_be", "description_en",
                ):
                    val = getattr(n, attr, None)
                    if val:
                        yield val.lower()

            for news in all_news:
                if any(query_lower in t for t in _texts(news)):
                    filtered_news.append(news)
        
    else:
        filtered_news = all_news
        is_search_results = False
    
    data = {
        'news_list': filtered_news,
        'query': query,
        'is_search_results': is_search_results,
        'search_count': len(filtered_news)
    }
    
    try:
        return render_template('index.html', **data)
    except Exception as e:
        logger.error(f"Ошибка рендеринга шаблона: {e}")
        return "500 Internal Server Error", 500

