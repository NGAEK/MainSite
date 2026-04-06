import secrets


def validate_api_key(provided: str, expected: str) -> bool:
    """Проверка ключа API (время-устойчивое сравнение)."""
    if not expected:
        return False
    return secrets.compare_digest(provided or "", expected)
