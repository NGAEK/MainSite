from __future__ import annotations

API_KEY_HEADER = "X-API-Key"


def build_openapi_spec(base_url: str | None = None) -> dict:
    servers = [{"url": "/api/v1", "description": "RestAPI"}]
    if base_url:
        root = base_url.rstrip("/")
        servers.insert(0, {"url": f"{root}/api/v1", "description": "Текущий сервер"})

    return {
        "openapi": "3.0.3",
        "info": {
            "title": "NGAEK — API",
            "version": "1.0.0",
            "description": (
                "REST API для внешней админ-панели: новости, вкладки меню, "
                "динамические страницы, файлы шаблонов и метрики.\n\n"
                "**Авторизация:** заголовок `X-API-Key` и/или `Authorization: Bearer <token>` "
                "(токен выдаётся через `POST /auth/login`).\n\n"
                "Интерактивная документация: `/swagger`"
            ),
        },
        "servers": servers,
        "tags": [
            {"name": "Auth", "description": "Вход и токен"},
            {"name": "Health", "description": "Проверка доступности"},
            {"name": "Metrics", "description": "Сводные метрики"},
            {"name": "News", "description": "Новости колледжа"},
            {"name": "Tabs", "description": "Динамические вкладки меню"},
            {"name": "Pages", "description": "Динамические страницы (site_pages)"},
            {"name": "PageTemplates", "description": "Редактируемые HTML-шаблоны"},
            {"name": "Media", "description": "Загрузка изображений"},
            {"name": "Files", "description": "Файловый менеджер (ограниченные scope)"},
            {"name": "System", "description": "Состояние системы"},
        ],
        "components": _components(),
        "paths": _paths(),
    }


def _components() -> dict:
    err = {
        "description": "Ошибка",
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
            }
        },
    }
    return {
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": API_KEY_HEADER,
                "description": "Ключ из config.yml (`admin_api.key`) или `NGAEK_ADMIN_API_KEY`",
            },
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT-like",
                "description": "Токен из `POST /auth/login` (срок жизни 8 ч)",
            },
        },
        "schemas": {
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string", "example": "validation_error"},
                            "message": {"type": "string"},
                        },
                        "required": ["code", "message"],
                    }
                },
            },
            "LoginRequest": {
                "type": "object",
                "required": ["username", "password"],
                "properties": {
                    "username": {"type": "string", "example": "admin"},
                    "password": {"type": "string", "format": "password"},
                },
            },
            "TokenResponse": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "properties": {
                            "access_token": {"type": "string"},
                            "token_type": {"type": "string", "example": "Bearer"},
                            "expires_in": {"type": "integer", "example": 28800},
                        },
                    }
                },
            },
            "News": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string", "description": "Заголовок (RU)"},
                    "date": {"type": "string", "format": "date", "example": "2026-05-15"},
                    "description": {"type": "string", "description": "Текст (RU)"},
                    "name_be": {"type": "string", "nullable": True},
                    "name_en": {"type": "string", "nullable": True},
                    "description_be": {"type": "string", "nullable": True},
                    "description_en": {"type": "string", "nullable": True},
                    "image_path": {
                        "type": "string",
                        "nullable": True,
                        "example": "/static/images/news_images/abc.jpg",
                    },
                },
            },
            "NewsInput": {
                "type": "object",
                "required": ["name", "description", "date"],
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "date": {"type": "string", "format": "date"},
                    "name_be": {"type": "string"},
                    "name_en": {"type": "string"},
                    "description_be": {"type": "string"},
                    "description_en": {"type": "string"},
                    "image_path": {"type": "string"},
                },
            },
            "NewsPatch": {
                "type": "object",
                "description": "Любое подмножество полей NewsInput",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "date": {"type": "string", "format": "date"},
                    "name_be": {"type": "string"},
                    "name_en": {"type": "string"},
                    "description_be": {"type": "string"},
                    "description_en": {"type": "string"},
                    "image_path": {"type": "string"},
                },
            },
            "Tab": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "slug": {"type": "string"},
                    "title": {"type": "string"},
                    "menu_title": {"type": "string"},
                    "content_html": {"type": "string"},
                    "sort_order": {"type": "integer", "default": 100},
                    "is_active": {"type": "boolean", "default": True},
                    "open_in_new_tab": {"type": "boolean", "default": False},
                },
            },
            "TabInput": {
                "type": "object",
                "required": ["title", "menu_title"],
                "properties": {
                    "title": {"type": "string"},
                    "menu_title": {"type": "string"},
                    "slug": {"type": "string", "description": "Если не указан — из menu_title"},
                    "content_html": {"type": "string"},
                    "sort_order": {"type": "integer", "default": 100},
                    "is_active": {"type": "boolean", "default": True},
                    "open_in_new_tab": {"type": "boolean", "default": False},
                },
            },
            "SitePage": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "slug": {"type": "string", "example": "testirovanie1"},
                    "title": {"type": "string"},
                    "content_html": {"type": "string"},
                    "sort_order": {"type": "integer"},
                    "is_active": {"type": "boolean"},
                    "branch_id": {
                        "type": "string",
                        "description": "Раздел каталога в админке (history, education, …)",
                    },
                    "route": {
                        "type": "string",
                        "readOnly": True,
                        "example": "/pages/example",
                    },
                },
            },
            "SitePageInput": {
                "type": "object",
                "required": ["title"],
                "properties": {
                    "title": {"type": "string"},
                    "slug": {"type": "string", "description": "Уникальный URL-идентификатор"},
                    "content_html": {"type": "string"},
                    "sort_order": {"type": "integer", "default": 100},
                    "is_active": {"type": "boolean", "default": True},
                    "branch_id": {"type": "string"},
                },
            },
            "IdResponse": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    }
                },
            },
            "UpdatedResponse": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "updated": {"type": "boolean"},
                        },
                    }
                },
            },
            "FileWriteRequest": {
                "type": "object",
                "required": ["scope", "path", "content"],
                "properties": {
                    "scope": {"type": "string", "example": "templates"},
                    "path": {"type": "string", "example": "pages/contacts.html"},
                    "content": {"type": "string"},
                },
            },
            "TemplateContentUpdate": {
                "type": "object",
                "required": ["content"],
                "properties": {"content": {"type": "string"}},
            },
        },
        "responses": {
            "Unauthorized": err,
            "ValidationError": err,
            "NotFound": err,
            "Conflict": err,
            "DatabaseUnavailable": err,
        },
        "parameters": {
            "TabId": {
                "name": "tab_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
            },
            "PageId": {
                "name": "page_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
            },
            "NewsId": {
                "name": "news_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
            },
            "TemplateSlug": {
                "name": "slug",
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
                "description": "privacy | one_window | contacts | cookies | specialties",
            },
        },
    }


def _op(
    *,
    tag: str,
    summary: str,
    description: str = "",
    secured: bool = True,
    request_body=None,
    parameters=None,
    responses=None,
):
    op = {
        "tags": [tag],
        "summary": summary,
        "description": description,
        "responses": responses or {"200": {"description": "OK"}},
    }
    if secured:
        op["security"] = [{"ApiKeyAuth": []}, {"BearerAuth": []}]
    if request_body:
        op["requestBody"] = request_body
    if parameters:
        op["parameters"] = parameters
    return op


def _json_body(schema_ref: str, required: bool = True):
    return {
        "required": required,
        "content": {
            "application/json": {"schema": {"$ref": f"#/components/schemas/{schema_ref}"}}
        },
    }


def _paths() -> dict:
    json_list_news = {
        "200": {
            "description": "Список новостей",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/News"},
                            }
                        },
                    }
                }
            },
        },
        "401": {"$ref": "#/components/responses/Unauthorized"},
        "503": {"$ref": "#/components/responses/DatabaseUnavailable"},
    }
    auth_err = {
        "401": {"$ref": "#/components/responses/Unauthorized"},
        "503": {"$ref": "#/components/responses/DatabaseUnavailable"},
    }

    return {
        "/health": {
            "get": _op(
                tag="Health",
                summary="Проверка API",
                secured=False,
                description="Не требует авторизации.",
                responses={
                    "200": {
                        "description": "Сервис отвечает",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "ok"},
                                        "db_alive": {"type": "boolean"},
                                    },
                                }
                            }
                        },
                    }
                },
            )
        },
        "/auth/login": {
            "post": _op(
                tag="Auth",
                summary="Вход (Bearer-токен)",
                secured=False,
                description="Проверяет логин/пароль администратора в PostgreSQL.",
                request_body=_json_body("LoginRequest"),
                responses={
                    "200": {
                        "description": "Токен выдан",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TokenResponse"}
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/ValidationError"},
                    "401": {"$ref": "#/components/responses/Unauthorized"},
                    "503": {"$ref": "#/components/responses/DatabaseUnavailable"},
                },
            )
        },
        "/metrics/main": {
            "get": _op(
                tag="Metrics",
                summary="Операционные метрики",
                description="Новости, посетители, вкладки, страницы, uptime API.",
                responses={
                    "200": {"description": "Метрики"},
                    **auth_err,
                },
            )
        },
        "/media/news-image": {
            "post": _op(
                tag="Media",
                summary="Загрузить изображение новости",
                description="multipart/form-data, поле `image` (jpg, png, webp, gif).",
                request_body={
                    "required": True,
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "type": "object",
                                "required": ["image"],
                                "properties": {
                                    "image": {
                                        "type": "string",
                                        "format": "binary",
                                    }
                                },
                            }
                        }
                    },
                },
                responses={
                    "201": {
                        "description": "Файл сохранён",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "image_path": {"type": "string"},
                                                "image_url": {"type": "string"},
                                            },
                                        }
                                    },
                                }
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/ValidationError"},
                    **auth_err,
                },
            )
        },
        "/page-templates": {
            "get": _op(
                tag="PageTemplates",
                summary="Список редактируемых шаблонов",
                parameters=[
                    {
                        "name": "include_content",
                        "in": "query",
                        "schema": {"type": "boolean", "default": False},
                    }
                ],
                responses={"200": {"description": "Шаблоны"}, **auth_err},
            )
        },
        "/page-templates/{slug}": {
            "get": _op(
                tag="PageTemplates",
                summary="Содержимое шаблона",
                parameters=[{"$ref": "#/components/parameters/TemplateSlug"}],
                responses={
                    "200": {"description": "Шаблон и content"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
            "put": _op(
                tag="PageTemplates",
                summary="Обновить HTML шаблона",
                parameters=[{"$ref": "#/components/parameters/TemplateSlug"}],
                request_body=_json_body("TemplateContentUpdate"),
                responses={
                    "200": {"description": "Обновлено"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
        },
        "/tabs": {
            "get": _op(
                tag="Tabs",
                summary="Список вкладок",
                parameters=[
                    {
                        "name": "include_inactive",
                        "in": "query",
                        "schema": {"type": "boolean", "default": True},
                    }
                ],
                responses={
                    "200": {
                        "description": "Вкладки",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/Tab"},
                                        }
                                    },
                                }
                            }
                        },
                    },
                    **auth_err,
                },
            ),
            "post": _op(
                tag="Tabs",
                summary="Создать вкладку",
                request_body=_json_body("TabInput"),
                responses={
                    "201": {
                        "description": "Создано",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/IdResponse"}
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/ValidationError"},
                    "409": {"$ref": "#/components/responses/Conflict"},
                    **auth_err,
                },
            ),
        },
        "/tabs/{tab_id}": {
            "put": _op(
                tag="Tabs",
                summary="Обновить вкладку",
                parameters=[{"$ref": "#/components/parameters/TabId"}],
                request_body=_json_body("TabInput"),
                responses={
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UpdatedResponse"}
                            }
                        }
                    },
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
            "delete": _op(
                tag="Tabs",
                summary="Удалить вкладку",
                parameters=[{"$ref": "#/components/parameters/TabId"}],
                responses={
                    "204": {"description": "Удалено"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
        },
        "/pages": {
            "get": _op(
                tag="Pages",
                summary="Список динамических страниц",
                responses={
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/SitePage"},
                                        }
                                    },
                                }
                            }
                        }
                    },
                    **auth_err,
                },
            ),
            "post": _op(
                tag="Pages",
                summary="Создать страницу",
                description="`slug` должен быть уникальным. При дубликате — **409** `slug_conflict`.",
                request_body=_json_body("SitePageInput"),
                responses={
                    "201": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {"$ref": "#/components/schemas/SitePage"},
                                    },
                                }
                            }
                        }
                    },
                    "409": {"$ref": "#/components/responses/Conflict"},
                    "400": {"$ref": "#/components/responses/ValidationError"},
                    **auth_err,
                },
            ),
        },
        "/search": {
            "get": _op(
                tag="Pages",
                summary="Поиск по сайту (JSON)",
                parameters=[
                    {
                        "name": "q",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"},
                    },
                    {
                        "name": "lang",
                        "in": "query",
                        "schema": {"type": "string", "enum": ["ru", "be", "en"]},
                    },
                ],
                responses={
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "query": {"type": "string"},
                                                "lang": {"type": "string"},
                                                "matches": {"type": "array"},
                                            },
                                        }
                                    },
                                }
                            }
                        }
                    },
                    **auth_err,
                },
            ),
        },
        "/pages/{page_id}": {
            "get": _op(
                tag="Pages",
                summary="Получить страницу по id",
                parameters=[{"$ref": "#/components/parameters/PageId"}],
                responses={
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {"$ref": "#/components/schemas/SitePage"},
                                    },
                                }
                            }
                        }
                    },
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
            "put": _op(
                tag="Pages",
                summary="Обновить страницу",
                parameters=[{"$ref": "#/components/parameters/PageId"}],
                request_body=_json_body("SitePageInput"),
                responses={
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UpdatedResponse"}
                            }
                        }
                    },
                    "409": {"$ref": "#/components/responses/Conflict"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
            "delete": _op(
                tag="Pages",
                summary="Удалить страницу",
                parameters=[{"$ref": "#/components/parameters/PageId"}],
                responses={
                    "204": {"description": "Удалено"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
        },
        "/system/status": {
            "get": _op(
                tag="System",
                summary="Статус БД и файловых scope",
                responses={"200": {"description": "Статус"}, **auth_err},
            )
        },
        "/files": {
            "get": _op(
                tag="Files",
                summary="Список файлов или чтение файла",
                parameters=[
                    {
                        "name": "scope",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"},
                    },
                    {"name": "path", "in": "query", "schema": {"type": "string", "default": ""}},
                    {
                        "name": "include_content",
                        "in": "query",
                        "schema": {"type": "boolean", "default": False},
                    },
                ],
                responses={
                    "200": {"description": "items или content"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
            "put": _op(
                tag="Files",
                summary="Записать текстовый файл",
                request_body=_json_body("FileWriteRequest"),
                responses={"200": {"description": "Сохранено"}, **auth_err},
            ),
            "delete": _op(
                tag="Files",
                summary="Удалить файл",
                parameters=[
                    {
                        "name": "scope",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"},
                    },
                    {"name": "path", "in": "query", "required": True, "schema": {"type": "string"}},
                ],
                responses={
                    "204": {"description": "Удалено"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
        },
        "/news": {
            "get": _op(
                tag="News",
                summary="Список новостей",
                responses=json_list_news,
            ),
            "post": _op(
                tag="News",
                summary="Создать новость",
                request_body=_json_body("NewsInput"),
                responses={
                    "201": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/IdResponse"}
                            }
                        }
                    },
                    "400": {"$ref": "#/components/responses/ValidationError"},
                    **auth_err,
                },
            ),
        },
        "/news/{news_id}": {
            "get": _op(
                tag="News",
                summary="Новость по ID",
                parameters=[{"$ref": "#/components/parameters/NewsId"}],
                responses={
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {"$ref": "#/components/schemas/News"}
                                    },
                                }
                            }
                        }
                    },
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
            "put": _op(
                tag="News",
                summary="Полная замена новости",
                parameters=[{"$ref": "#/components/parameters/NewsId"}],
                request_body=_json_body("NewsInput"),
                responses={
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UpdatedResponse"}
                            }
                        }
                    },
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
            "patch": _op(
                tag="News",
                summary="Частичное обновление новости",
                parameters=[{"$ref": "#/components/parameters/NewsId"}],
                request_body=_json_body("NewsPatch"),
                responses={
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UpdatedResponse"}
                            }
                        }
                    },
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
            "delete": _op(
                tag="News",
                summary="Удалить новость",
                parameters=[{"$ref": "#/components/parameters/NewsId"}],
                responses={
                    "204": {"description": "Удалено"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                    **auth_err,
                },
            ),
        },
    }
