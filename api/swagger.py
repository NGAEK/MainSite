"""Swagger UI на /swagger."""
from __future__ import annotations

from flask import Flask, Response, redirect

OPENAPI_JSON_PATH = "/api/v1/openapi.json"

SWAGGER_UI_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NGAEK Admin API — Swagger</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui.css">
  <style>
    html { box-sizing: border-box; overflow-y: scroll; }
    *, *:before, *:after { box-sizing: inherit; }
    body { margin: 0; background: #fafafa; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui-bundle.js" crossorigin></script>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui-standalone-preset.js" crossorigin></script>
  <script>
    window.onload = function () {
      SwaggerUIBundle({
        url: __OPENAPI_URL__,
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        layout: "StandaloneLayout",
        persistAuthorization: true,
        tryItOutEnabled: true,
        displayRequestDuration: true,
        filter: true,
        syntaxHighlight: { theme: "agate" }
      });
    };
  </script>
</body>
</html>
"""


def _swagger_html() -> str:
    return SWAGGER_UI_HTML.replace("__OPENAPI_URL__", repr(OPENAPI_JSON_PATH))


def register_swagger(app: Flask) -> None:
    """Регистрирует GET /swagger и редирект с /swagger/."""

    @app.route("/swagger")
    def swagger_ui():
        return Response(_swagger_html(), mimetype="text/html; charset=utf-8")

    @app.route("/swagger/")
    def swagger_ui_slash():
        return redirect("/swagger", code=302)
