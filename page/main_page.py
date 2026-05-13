from urllib.parse import urlencode

from flask import redirect, render_template
import logging

from db import news_repository

logger = logging.getLogger(__name__)


def home_handler(request):
    """Обработчик главной страницы. Запрос ?q= перенаправляется на полнотекстовый поиск по сайту."""
    query = request.args.get("q", "").strip()
    if query:
        params = {"q": query}
        lang = request.args.get("lang")
        if lang in ("ru", "be", "en"):
            params["lang"] = lang
        return redirect("/search?" + urlencode(params))

    try:
        all_news = news_repository.get_all_news()
    except Exception as e:
        logger.warning(f"DB: Ошибка загрузки новостей (БД отключена?): {e}. Используется пустой список.")
        all_news = []

    data = {
        "news_list": all_news,
        "search_count": len(all_news),
    }
    
    try:
        return render_template('index.html', **data)
    except Exception as e:
        logger.error(f"Ошибка рендеринга шаблона: {e}")
        return "500 Internal Server Error", 500

