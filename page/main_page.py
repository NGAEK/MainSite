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
        logger.error(f"Ошибка загрузки новостей: {e}")
        return "500 Internal Server Error", 500
    
    query = request.args.get('q', '').strip()
    logger.info(f"Search query: '{query}'")
    
    filtered_news = []
    is_search_results = False
    
    if query:
        is_search_results = True
        try:
            db_results = news_repository.search_news(query)
            filtered_news = db_results
        except Exception as e:
            logger.error(f"Ошибка поиска в БД: {e}")
            # Если ошибка в БД, фильтруем локально
            query_lower = query.lower()
            for news in all_news:
                if (query_lower in news.name.lower() if news.name else False) or \
                   (query_lower in news.description.lower() if news.description else False):
                    filtered_news.append(news)
        
        logger.info(f"Found {len(filtered_news)} results for query '{query}'")
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

