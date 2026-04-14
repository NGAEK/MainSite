"""JSON API для внешней админки: приём и отдача данных о новостях."""
import logging
from datetime import date, datetime, timezone
from flask import Blueprint, request, jsonify, current_app

from api.file_service import (
    build_default_file_service,
    FileServiceError,
    InvalidScopeError,
    UnsafePathError,
    FileMissingError,
)
from api.security import validate_api_key
from db.connection import is_db_alive, get_table_names
from db import news_repository
from db import admin_users_repository
from api.security import (
    validate_admin_credentials,
    issue_access_token,
    validate_access_token,
)

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

API_KEY_HEADER = "X-API-Key"
AUTHORIZATION_HEADER = "Authorization"
ACCESS_TOKEN_TTL_SECONDS = 8 * 60 * 60
API_STARTED_AT = datetime.now(timezone.utc)


@api_bp.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        return "", 204
    return None


def _expected_key():
    return (current_app.config.get("ADMIN_API_KEY") or "").strip()


def _json_error(status: int, code: str, message: str):
    body = {"error": {"code": code, "message": message}}
    return jsonify(body), status


def _parse_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _file_service():
    project_root = current_app.root_path
    return build_default_file_service(project_root)


def _require_api_key():
    expected = _expected_key()
    if not expected:
        return _json_error(
            503,
            "api_not_configured",
            "Задайте ключ в config.yml (admin_api.key) или переменную NGAEK_ADMIN_API_KEY",
        )
    provided = request.headers.get(API_KEY_HEADER, "")
    if not validate_api_key(provided, expected):
        return _json_error(401, "unauthorized", "Неверный или отсутствует ключ API")
    return None


def _require_auth():
    api_key_err = _require_api_key()
    if api_key_err is None:
        return None
    expected_secret = _expected_key()
    auth_header = request.headers.get(AUTHORIZATION_HEADER, "")
    if not auth_header.lower().startswith("bearer "):
        return api_key_err
    token = auth_header[7:].strip()
    if not token or not expected_secret:
        return api_key_err
    token_data = validate_access_token(expected_secret, token, ACCESS_TOKEN_TTL_SECONDS)
    if not token_data:
        return api_key_err
    return None


def _parse_json_body():
    if not request.is_json:
        return None, _json_error(400, "invalid_body", "Ожидается Content-Type: application/json")
    try:
        return request.get_json(force=False), None
    except Exception:
        return None, _json_error(400, "invalid_json", "Тело запроса не является JSON")


def _validate_date(raw) -> tuple:
    if raw is None or raw == "":
        return None, "Поле date обязательно (YYYY-MM-DD)"
    if isinstance(raw, str):
        try:
            return date.fromisoformat(raw), None
        except ValueError:
            return None, "Неверный формат date, ожидается YYYY-MM-DD"
    return None, "Поле date должно быть строкой YYYY-MM-DD"


def _collect_main_metrics() -> dict:
    now = datetime.now(timezone.utc)
    uptime_seconds = int((now - API_STARTED_AT).total_seconds())
    db_tables = get_table_names()
    return {
        "generated_at": now.isoformat(),
        "api_uptime_seconds": uptime_seconds,
        "db_alive": is_db_alive(),
        "db_table_count": len(db_tables),
        "db_tables": db_tables,
        "news_total": news_repository.count_news(),
        "admin_users_total": admin_users_repository.count_admin_users(active_only=False),
        "admin_users_active": admin_users_repository.count_admin_users(active_only=True),
    }


@api_bp.route("/auth/login", methods=["POST", "OPTIONS"])
def auth_login():
    if request.method == "OPTIONS":
        return "", 204
    payload, err = _parse_json_body()
    if err:
        return err
    username = str(payload.get("username") or "").strip()
    password = str(payload.get("password") or "")
    if not username or not password:
        return _json_error(400, "validation_error", "Поля username и password обязательны")
    try:
        user = admin_users_repository.get_admin_user_by_username(username)
    except Exception as e:
        logger.exception("API auth_login get_admin_user_by_username")
        return _json_error(500, "database_error", str(e))
    if not user or not bool(user.get("is_active")):
        return _json_error(401, "unauthorized", "Неверный логин или пароль")
    expected_username = str(user.get("username") or "").strip()
    expected_password_hash = str(user.get("password_hash") or "").strip()
    if not validate_admin_credentials(username, password, expected_username, expected_password_hash):
        return _json_error(401, "unauthorized", "Неверный логин или пароль")
    token_secret = _expected_key()
    if not token_secret:
        return _json_error(
            503,
            "api_not_configured",
            "Для выпуска токенов задайте admin_api.key или NGAEK_ADMIN_API_KEY",
        )
    token = issue_access_token(token_secret, username)
    return (
        jsonify(
            {
                "data": {
                    "access_token": token,
                    "token_type": "Bearer",
                    "expires_in": ACCESS_TOKEN_TTL_SECONDS,
                }
            }
        ),
        200,
    )


@api_bp.route("/openapi.json", methods=["GET"])
def openapi_schema():
    schema = {
        "openapi": "3.0.3",
        "info": {"title": "MainSite Admin API", "version": "1.0.0"},
        "servers": [{"url": "/api/v1"}],
        "components": {
            "securitySchemes": {
                "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": API_KEY_HEADER},
                "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "token"},
            }
        },
        "security": [{"ApiKeyAuth": []}, {"BearerAuth": []}],
        "paths": {
            "/health": {"get": {"summary": "API health"}},
            "/auth/login": {"post": {"summary": "Login and receive bearer token"}},
            "/metrics/main": {"get": {"summary": "Main operational metrics"}},
            "/system/status": {"get": {"summary": "System status"}},
            "/files": {"get": {"summary": "List files or read file"}, "put": {"summary": "Write file"}, "delete": {"summary": "Delete file"}},
            "/news": {"get": {"summary": "List news"}, "post": {"summary": "Create news"}},
            "/news/{news_id}": {"get": {"summary": "Get news"}, "put": {"summary": "Replace news"}, "patch": {"summary": "Patch news"}, "delete": {"summary": "Delete news"}},
        },
    }
    return jsonify(schema), 200


@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "db_alive": is_db_alive()}), 200


@api_bp.route("/metrics/main", methods=["GET"])
def main_metrics():
    err = _require_auth()
    if err:
        return err
    try:
        data = _collect_main_metrics()
    except Exception as e:
        logger.exception("API main_metrics")
        return _json_error(500, "database_error", str(e))
    return jsonify({"data": data}), 200


@api_bp.route("/system/status", methods=["GET"])
def system_status():
    err = _require_auth()
    if err:
        return err
    service = _file_service()
    return (
        jsonify(
            {
                "data": {
                    "db_alive": is_db_alive(),
                    "db_tables": get_table_names(),
                    "file_scopes": service.scopes(),
                }
            }
        ),
        200,
    )


@api_bp.route("/files", methods=["GET"])
def list_files():
    err = _require_auth()
    if err:
        return err
    scope = (request.args.get("scope") or "").strip()
    rel_path = request.args.get("path", "")
    include_content = _parse_bool(request.args.get("include_content"), default=False)
    service = _file_service()
    try:
        if include_content:
            content = service.read_text(scope, rel_path)
            return jsonify({"data": {"scope": scope, "path": rel_path, "content": content}}), 200
        items = service.list_dir(scope, rel_path)
        return jsonify({"data": {"scope": scope, "path": rel_path, "items": items}}), 200
    except InvalidScopeError as e:
        return _json_error(400, "invalid_scope", str(e))
    except UnsafePathError as e:
        return _json_error(400, "unsafe_path", str(e))
    except FileMissingError as e:
        return _json_error(404, "not_found", str(e))
    except FileServiceError as e:
        return _json_error(400, "file_error", str(e))


@api_bp.route("/files", methods=["PUT"])
def put_file():
    err = _require_auth()
    if err:
        return err
    payload, err = _parse_json_body()
    if err:
        return err
    scope = str(payload.get("scope") or "").strip()
    rel_path = str(payload.get("path") or "").strip()
    content = payload.get("content")
    if not scope or not rel_path:
        return _json_error(400, "validation_error", "Поля scope и path обязательны")
    if not isinstance(content, str):
        return _json_error(400, "validation_error", "Поле content должно быть строкой")
    service = _file_service()
    try:
        service.write_text(scope, rel_path, content)
    except InvalidScopeError as e:
        return _json_error(400, "invalid_scope", str(e))
    except UnsafePathError as e:
        return _json_error(400, "unsafe_path", str(e))
    except FileServiceError as e:
        return _json_error(400, "file_error", str(e))
    return jsonify({"data": {"scope": scope, "path": rel_path, "updated": True}}), 200


@api_bp.route("/files", methods=["DELETE"])
def delete_file():
    err = _require_auth()
    if err:
        return err
    scope = (request.args.get("scope") or "").strip()
    rel_path = request.args.get("path", "")
    service = _file_service()
    try:
        deleted = service.delete_file(scope, rel_path)
    except InvalidScopeError as e:
        return _json_error(400, "invalid_scope", str(e))
    except UnsafePathError as e:
        return _json_error(400, "unsafe_path", str(e))
    except FileServiceError as e:
        return _json_error(400, "file_error", str(e))
    if not deleted:
        return _json_error(404, "not_found", "Файл не найден")
    return "", 204


@api_bp.route("/news", methods=["GET"])
def list_news():
    err = _require_auth()
    if err:
        return err
    try:
        items = news_repository.get_all_news()
    except Exception as e:
        logger.exception("API list_news")
        return _json_error(500, "database_error", str(e))
    return jsonify({"data": [news_repository.news_to_dict(n) for n in items]}), 200


@api_bp.route("/news/<int:news_id>", methods=["GET"])
def get_news(news_id):
    err = _require_auth()
    if err:
        return err
    try:
        n = news_repository.get_news_by_id(news_id)
    except Exception as e:
        logger.exception("API get_news")
        return _json_error(500, "database_error", str(e))
    if not n:
        return _json_error(404, "not_found", "Новость не найдена")
    return jsonify({"data": news_repository.news_to_dict(n)}), 200


@api_bp.route("/news", methods=["POST"])
def create_news():
    err = _require_auth()
    if err:
        return err
    payload, err = _parse_json_body()
    if err:
        return err
    name = (payload.get("name") or "").strip()
    description = (payload.get("description") or "").strip()
    if not name or not description:
        return _json_error(400, "validation_error", "Обязательны поля name и description (RU)")
    d, derr = _validate_date(payload.get("date"))
    if derr:
        return _json_error(400, "validation_error", derr)
    row = {
        "name": name,
        "date": d,
        "description": description,
        "name_be": payload.get("name_be"),
        "name_en": payload.get("name_en"),
        "description_be": payload.get("description_be"),
        "description_en": payload.get("description_en"),
        "image_path": payload.get("image_path"),
    }
    try:
        new_id = news_repository.insert_news(row)
    except Exception as e:
        logger.exception("API create_news")
        return _json_error(500, "database_error", str(e))
    return jsonify({"data": {"id": new_id}}), 201


@api_bp.route("/news/<int:news_id>", methods=["PUT"])
def put_news(news_id):
    err = _require_auth()
    if err:
        return err
    if not news_repository.news_exists(news_id):
        return _json_error(404, "not_found", "Новость не найдена")
    payload, err = _parse_json_body()
    if err:
        return err
    name = (payload.get("name") or "").strip()
    description = (payload.get("description") or "").strip()
    if not name or not description:
        return _json_error(400, "validation_error", "Обязательны поля name и description (RU)")
    d, derr = _validate_date(payload.get("date"))
    if derr:
        return _json_error(400, "validation_error", derr)
    row = {
        "name": name,
        "date": d,
        "description": description,
        "name_be": payload.get("name_be"),
        "name_en": payload.get("name_en"),
        "description_be": payload.get("description_be"),
        "description_en": payload.get("description_en"),
        "image_path": payload.get("image_path"),
    }
    try:
        news_repository.update_news_full(news_id, row)
    except Exception as e:
        logger.exception("API put_news")
        return _json_error(500, "database_error", str(e))
    return jsonify({"data": {"id": news_id, "updated": True}}), 200


@api_bp.route("/news/<int:news_id>", methods=["PATCH"])
def patch_news(news_id):
    err = _require_auth()
    if err:
        return err
    if not news_repository.news_exists(news_id):
        return _json_error(404, "not_found", "Новость не найдена")
    payload, err = _parse_json_body()
    if err:
        return err
    if not isinstance(payload, dict) or not payload:
        return _json_error(400, "validation_error", "Пустой объект изменений")
    patch = {}
    for key in (
        "name",
        "description",
        "name_be",
        "name_en",
        "description_be",
        "description_en",
        "image_path",
    ):
        if key in payload:
            patch[key] = payload[key]
    if "date" in payload:
        d, derr = _validate_date(payload.get("date"))
        if derr:
            return _json_error(400, "validation_error", derr)
        patch["date"] = d
    if not patch:
        return _json_error(400, "validation_error", "Нет допустимых полей для обновления")
    try:
        news_repository.update_news_partial(news_id, patch)
    except Exception as e:
        logger.exception("API patch_news")
        return _json_error(500, "database_error", str(e))
    return jsonify({"data": {"id": news_id, "updated": True}}), 200


@api_bp.route("/news/<int:news_id>", methods=["DELETE"])
def delete_news(news_id):
    err = _require_auth()
    if err:
        return err
    try:
        deleted = news_repository.delete_news(news_id)
    except Exception as e:
        logger.exception("API delete_news")
        return _json_error(500, "database_error", str(e))
    if not deleted:
        return _json_error(404, "not_found", "Новость не найдена")
    return "", 204
