from werkzeug.security import generate_password_hash

from api.security import (
    validate_admin_credentials,
    issue_access_token,
    validate_access_token,
)


def test_validate_admin_credentials_ok():
    password_hash = generate_password_hash("secret123")
    assert validate_admin_credentials("admin", "secret123", "admin", password_hash) is True


def test_validate_admin_credentials_invalid_password():
    password_hash = generate_password_hash("secret123")
    assert validate_admin_credentials("admin", "wrong", "admin", password_hash) is False


def test_validate_access_token_ok():
    token = issue_access_token("my-secret", "admin")
    data = validate_access_token("my-secret", token, 60)
    assert data is not None
    assert data["sub"] == "admin"


def test_validate_access_token_invalid_secret():
    token = issue_access_token("my-secret", "admin")
    assert validate_access_token("other-secret", token, 60) is None


def test_validate_admin_credentials_rejects_empty_hash():
    assert validate_admin_credentials("admin", "secret123", "admin", "") is False


def test_validate_admin_credentials_with_bcrypt_hash():
    bcrypt_hash = "$2b$12$k7dOeMUC/9L4i8Vx9Z9zku.I9M9ygis1WF0QAP8z668UYZLTKzvRa"
    assert validate_admin_credentials("admin", "admin", "admin", bcrypt_hash) is True
