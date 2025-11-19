from flask import render_template, abort
import logging
from db import news_repository

logger = logging.getLogger(__name__)


def news_detail_handler(request, news_id):
    """Обработчик страницы детального просмотра новости"""
    try:
        # Проверяем существование новости
        exists = news_repository.news_exists(news_id)
        if not exists:
            abort(404)
        
        # Получаем новость из БД
        news = news_repository.get_news_by_id(news_id)
        if not news:
            abort(404)
        
        query = request.args.get('q', '')
        
        data = {
            'news': news,
            'query': query
        }
        
        return render_template('news_detail.html', **data)
    
    except Exception as e:
        logger.error(f"Ошибка получения новости: {e}")
        abort(500)

