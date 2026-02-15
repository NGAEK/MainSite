from flask import Flask, render_template, request, abort, send_from_directory
import logging
import json
import os
from config.config import load_config
from db.connection import init_db
from page import main_page, news_detail_page, search_page, spec_page, notfound_page

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

LOCALES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'locales')
MESSAGES_FILE = os.path.join(LOCALES_DIR, 'messages.json')
SUPPORTED_LANGS = ('ru', 'be')
DEFAULT_LANG = 'ru'
LANG_KEY_MAP = {'ru': 'RU', 'be': 'BY'}  # код языка -> ключ в JSON


def get_locale():
    """Язык из query ?lang= или cookie locale, по умолчанию русский."""
    lang = request.args.get('lang') or request.cookies.get('locale', DEFAULT_LANG)
    return lang if lang in SUPPORTED_LANGS else DEFAULT_LANG


def _resolve_messages(obj, lang_key):
    """Рекурсивно подставить строку языка: каждый { RU, BY } -> значение для lang_key."""
    if isinstance(obj, dict):
        if 'RU' in obj and 'BY' in obj:
            return obj.get(lang_key) or obj.get('RU')
        return {k: _resolve_messages(v, lang_key) for k, v in obj.items()}
    return obj


def get_translations():
    """Загрузка строк из одного файла messages.json и выбор языка RU/BY."""
    lang_key = LANG_KEY_MAP.get(get_locale(), 'RU')
    try:
        with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return _resolve_messages(data, lang_key)
    except Exception as e:
        logger.warning(f"Не удалось загрузить локализацию {MESSAGES_FILE}: {e}")
        return {}


@app.context_processor
def inject_locale_and_query():
    """Передача переводов (t), текущего языка и query во все шаблоны."""
    return dict(
        t=get_translations(),
        current_lang=get_locale(),
        query=request.args.get('q', '')
    )

@app.after_request
def set_locale_cookie(response):
    """Сохраняем выбранный язык в cookie при ?lang=."""
    if request.args.get('lang') in SUPPORTED_LANGS:
        response.set_cookie('locale', request.args.get('lang'), max_age=365 * 24 * 3600)
    return response


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

