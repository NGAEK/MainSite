from flask import render_template
import logging

logger = logging.getLogger(__name__)


def not_found_handler(request):
    """Обработчик страницы 404"""
    try:
        data = {
            'title': 'Страница не найдена',
            'path': request.path
        }
        return render_template('errors/404.html', **data), 404
    except Exception as e:
        logger.error(f"Ошибка загрузки шаблона 404: {e}")
        return "500 Internal Server Error", 500

