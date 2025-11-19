from flask import Flask, render_template, request, abort, send_from_directory
import logging
from config.config import load_config
from db.connection import init_db
from page import main_page, news_detail_page, search_page, spec_page, notfound_page

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Контекстный процессор для передачи query во все шаблоны
@app.context_processor
def inject_query():
    return dict(query=request.args.get('q', ''))

# Регистрация фильтров для шаблонов
@app.template_filter('date_format')
def date_format_filter(date, format_str='%Y-%m-%d'):
    """Фильтр для форматирования даты"""
    if date is None:
        return ''
    if isinstance(date, str):
        from datetime import datetime
        try:
            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d.%m.%Y"]:
                try:
                    date = datetime.strptime(date, fmt)
                    break
                except:
                    continue
        except:
            return date
    if hasattr(date, 'strftime'):
        return date.strftime(format_str)
    return str(date)

# Загрузка конфигурации
config = load_config("config.yml")

# Инициализация базы данных
init_db(
    config.database.user,
    config.database.password,
    config.database.host,
    config.database.port,
    config.database.name
)


# Регистрация обработчиков ошибок
@app.errorhandler(404)
def not_found_handler(e):
    return notfound_page.not_found_handler(request)


# Статические файлы
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


# JavaScript файлы
@app.route('/js/<path:filename>')
def js_files(filename):
    return send_from_directory('js', filename)


# Маршруты
@app.route('/')
def home():
    return main_page.home_handler(request)


@app.route('/search')
def search():
    return search_page.search_handler(request)


@app.route('/news/<int:news_id>')
def news_detail(news_id):
    return news_detail_page.news_detail_handler(request, news_id)


@app.route('/spec/byx')
def spec_byx():
    return spec_page.spec_byx()


@app.route('/spec/do')
def spec_do():
    return spec_page.spec_do()


@app.route('/spec/ogu')
def spec_ogu():
    return spec_page.spec_ogu()


@app.route('/spec/po')
def spec_po():
    return spec_page.spec_po()


@app.route('/spec/soc_rab')
def spec_soc_rab():
    return spec_page.spec_soc_rab()


if __name__ == '__main__':
    port = config.server.port.lstrip(':') if config.server.port.startswith(':') else config.server.port
    logger.info(f"Сервер запущен на http://localhost:{port}")
    app.run(host='0.0.0.0', port=int(port), debug=True)

