"""Проверка, что ключевые Jinja-шаблоны компилируются без синтаксических ошибок."""
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError

TEMPLATES_ROOT = Path(__file__).resolve().parent.parent / "templates"


@pytest.fixture
def jinja_env():
    return Environment(loader=FileSystemLoader(str(TEMPLATES_ROOT)))


@pytest.mark.parametrize(
    "name",
    [
        "index.html",
        "base.html",
        "header.html",
        "footer.html",
        "macros/url.html",
    ],
)
def test_core_templates_compile(jinja_env, name):
    try:
        jinja_env.get_template(name)
    except TemplateSyntaxError as exc:
        pytest.fail(f"{name}: {exc}")
