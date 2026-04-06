from api.security import validate_api_key


def test_rejects_empty_expected():
    assert validate_api_key("any", "") is False
    assert validate_api_key("", "") is False


def test_accepts_matching_key():
    assert validate_api_key("secret", "secret") is True


def test_rejects_wrong_key():
    assert validate_api_key("wrong", "secret") is False
