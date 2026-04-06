from datetime import datetime

from models.news import News


def test_localized_name_fallback_to_ru():
    n = News(name="RU title", name_en=None, name_be=None)
    assert n.localized_name("en") == "RU title"
    assert n.localized_name("be") == "RU title"


def test_localized_name_uses_translation():
    n = News(name="RU", name_en="EN", name_be="BY")
    assert n.localized_name("en") == "EN"
    assert n.localized_name("be") == "BY"


def test_formatted_date_english():
    n = News(date=datetime(2025, 5, 15))
    assert "May" in n.formatted_date("en")
    assert "2025" in n.formatted_date("en")
