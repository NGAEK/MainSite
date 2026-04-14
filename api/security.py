import secrets

import bcrypt
from itsdangerous import URLSafeTimedSerializer, BadSignature, BadTimeSignature
from werkzeug.security import check_password_hash


def validate_api_key(provided: str, expected: str) -> bool:
    """Проверка ключа API (время-устойчивое сравнение)."""
    if not expected:
        return False
    return secrets.compare_digest(provided or "", expected)


def validate_admin_credentials(
    provided_username: str,
    provided_password: str,
    expected_username: str,
    expected_password_hash: str,
) -> bool:
    """Проверяет пару логин/пароль с hash-верификацией."""
    if not expected_username or not expected_password_hash:
        return False
    if not secrets.compare_digest(provided_username or "", expected_username):
        return False
    # Поддержка bcrypt-хешей из БД (формат $2a$/$2b$/$2y$).
    if expected_password_hash.startswith(("$2a$", "$2b$", "$2y$")):
        try:
            return bcrypt.checkpw(
                (provided_password or "").encode("utf-8"),
                expected_password_hash.encode("utf-8"),
            )
        except ValueError:
            return False
    try:
        return check_password_hash(expected_password_hash, provided_password or "")
    except ValueError:
        return False


def issue_access_token(secret: str, username: str) -> str:
    serializer = URLSafeTimedSerializer(secret_key=secret, salt="ngaek-admin-api")
    return serializer.dumps({"sub": username})


def validate_access_token(secret: str, token: str, max_age_seconds: int) -> dict | None:
    serializer = URLSafeTimedSerializer(secret_key=secret, salt="ngaek-admin-api")
    try:
        data = serializer.loads(token, max_age=max_age_seconds)
        if not isinstance(data, dict):
            return None
        return data
    except (BadSignature, BadTimeSignature):
        return None
