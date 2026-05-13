from flask import render_template
import logging

from db import news_repository

logger = logging.getLogger(__name__)


def news_list_handler(request):
    """Страница со списком всех новостей."""
    try:
        news_list = news_repository.get_all_news()
    except Exception as e:
        logger.warning(f"DB: не удалось загрузить список новостей: {e}")
        news_list = []
    return render_template("news/news_list.html", news_list=news_list)
