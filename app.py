from flask import Flask, render_template, request, abort, send_from_directory, current_app
import logging
import json
import os
from config.config import load_config
from db.connection import init_db
from db import admin_users_repository
from db import visitor_metrics_repository
from db import tabs_repository
from db import pages_repository
from page import (
    main_page,
    news_detail_page,
    search_page,
    spec_page,
    notfound_page,
    site_pages,
    student_pages,
    applicant_pages,
)
from api import api_bp
from util.i18n_url import build_hreflang_url

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

LOCALES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'locales')
MESSAGES_FILE = os.path.join(LOCALES_DIR, 'messages.json')
SUPPORTED_LANGS = ('ru', 'be', 'en')
DEFAULT_LANG = 'ru'
LANG_KEY_MAP = {'ru': 'RU', 'be': 'BY', 'en': 'EN'}  # код языка -> ключ в JSON


def get_locale():
    """Язык из query ?lang= или cookie locale, по умолчанию русский."""
    lang = request.args.get('lang') or request.cookies.get('locale', DEFAULT_LANG)
    return lang if lang in SUPPORTED_LANGS else DEFAULT_LANG


def _resolve_messages(obj, lang_key):
    """Рекурсивно подставить строку языка: каждый { RU, BY [, EN] } -> значение для lang_key."""
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


@app.context_processor
def inject_hreflang():
    def hreflang_url(lang_code: str) -> str:
        return build_hreflang_url(
            request.url_root,
            request.path,
            request.args.to_dict(flat=True),
            lang_code,
        )

    return dict(hreflang_url=hreflang_url)


@app.context_processor
def inject_site_public():
    """Реквизиты из config.yml (site) для футера и страниц."""
    s = current_app.config.get("SITE") or {}
    gris = s.get("gris") if isinstance(s.get("gris"), dict) else {}
    num = str(gris.get("number") or "").strip()
    reg_date = str(gris.get("registration_date") or "").strip()
    show_ph = gris.get("show_placeholder_if_empty", True)
    if isinstance(show_ph, str):
        show_ph = show_ph.lower() in ("1", "true", "yes", "on")
    phone_display = str(s.get("phone") or "").strip() or "+375 (17) 123-45-67"
    phone_tel = str(s.get("phone_tel") or "").strip()
    if not phone_tel:
        digits = "".join(c for c in phone_display if c.isdigit())
        phone_tel = ("+" + digits) if digits else ""
    return dict(
        site_gris_number=num,
        site_gris_date=reg_date,
        site_gris_show_placeholder=bool(show_ph),
        site_admin_email=str(s.get("admin_email") or "info@ngaek.by").strip(),
        site_one_window_url=str(s.get("one_window_external_url") or "").strip(),
        site_phone=phone_display,
        site_phone_tel=phone_tel,
    )


@app.context_processor
def inject_dynamic_tabs():
    try:
        tabs = tabs_repository.get_active_tabs()
    except Exception as exc:
        logger.warning(f"Не удалось загрузить динамические вкладки: {exc}")
        tabs = []
    return dict(dynamic_tabs=tabs)


@app.after_request
def set_locale_cookie(response):
    """Сохраняем выбранный язык в cookie при ?lang=."""
    if request.args.get('lang') in SUPPORTED_LANGS:
        response.set_cookie('locale', request.args.get('lang'), max_age=365 * 24 * 3600)
    return response


@app.after_request
def add_api_cors_headers(response):
    """CORS для запросов админки к API."""
    if request.path.startswith("/api/v1"):
        site_cfg = current_app.config.get("SITE") or {}
        allowed_origin = str(site_cfg.get("admin_panel_origin") or "").strip()
        request_origin = request.headers.get("Origin", "")
        if allowed_origin and request_origin == allowed_origin:
            response.headers["Access-Control-Allow-Origin"] = allowed_origin
            response.headers["Vary"] = "Origin"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-API-Key, Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Credentials"] = "false"
    return response


@app.after_request
def collect_site_user_metrics(response):
    """Собирает метрики уникальных пользователей по посещениям."""
    path = request.path or ""
    if path.startswith("/api/") or path.startswith("/static/") or path == "/favicon.ico":
        return response
    try:
        forwarded = (request.headers.get("X-Forwarded-For") or "").split(",")[0].strip()
        ip = forwarded or request.remote_addr or ""
        ua = request.user_agent.string or ""
        visitor_key = visitor_metrics_repository.build_visitor_key(ip, ua)
        visitor_metrics_repository.record_visit(visitor_key)
    except Exception as exc:
        logger.warning(f"Не удалось сохранить метрику посещения: {exc}")
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
app.config["ADMIN_API_KEY"] = config.admin_api_key
app.config["ADMIN_AUTH"] = config.admin_auth
app.config["SITE"] = config.site or {}

# Инициализация базы данных
init_db(
    config.database.user,
    config.database.password,
    config.database.host,
    config.database.port,
    config.database.name
)

admin_users_repository.ensure_admin_users_table()
visitor_metrics_repository.ensure_site_visits_table()
tabs_repository.ensure_tabs_table()
pages_repository.ensure_pages_table()
seed_auth = config.admin_auth or {}
seed_username = str(seed_auth.get("username") or "").strip()
seed_password_hash = str(seed_auth.get("password_hash") or "").strip()
if seed_username and seed_password_hash:
    existing_admin = admin_users_repository.get_admin_user_by_username(seed_username)
    if not existing_admin:
        admin_users_repository.create_admin_user(seed_username, seed_password_hash)
        logger.info("Bootstrap admin user created in MySQL")

app.register_blueprint(api_bp)


# Регистрация обработчиков ошибок
@app.errorhandler(404)
def not_found_handler(e):
    return notfound_page.not_found_handler(request)


# Статические файлы (включая static/js/*.js)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


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


@app.route("/privacy")
def privacy():
    return site_pages.privacy_handler(request)


@app.route("/one-window")
def one_window():
    return site_pages.one_window_handler(request)


@app.route("/sitemap")
def sitemap():
    return site_pages.sitemap_handler(request)


@app.route("/contacts")
def contacts():
    return site_pages.contacts_handler(request)


@app.route("/cookies")
def cookies_page():
    return site_pages.cookies_handler(request)


@app.route("/specialties")
def specialties_list():
    return site_pages.specialties_handler(request)


@app.route("/students")
def students_hub():
    return student_pages.students_hub_handler(request)


@app.route("/students/<slug>")
def students_article(slug):
    return student_pages.students_article_handler(request, slug)


@app.route("/applicants")
def applicants_hub():
    return applicant_pages.applicants_hub_handler(request)


@app.route("/applicants/<slug>")
def applicants_article(slug):
    return applicant_pages.applicants_article_handler(request, slug)


@app.route("/pages/<slug>")
def custom_page(slug):
    return site_pages.custom_page_handler(request, slug)


if __name__ == '__main__':
    port = config.server.port.lstrip(':') if config.server.port.startswith(':') else config.server.port
    logger.info(f"Сервер запущен на http://localhost:{port}")
    app.run(host='0.0.0.0', port=int(port), debug=True)

