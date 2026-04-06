"""JSON API для внешней админки: приём и отдача данных о новостях."""
import logging
from datetime import date
from flask import Blueprint, request, jsonify, current_app

from api.security import validate_api_key
from db import news_repository

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

API_KEY_HEADER = "X-API-Key"


def _expected_key():
    return (current_app.config.get("ADMIN_API_KEY") or "").strip()


def _json_error(status: int, code: str, message: str):
    body = {"error": {"code": code, "message": message}}
    return jsonify(body), status


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


@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@api_bp.route("/news", methods=["GET"])
def list_news():
    err = _require_api_key()
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
    err = _require_api_key()
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
    err = _require_api_key()
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
    err = _require_api_key()
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
    err = _require_api_key()
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
    err = _require_api_key()
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
