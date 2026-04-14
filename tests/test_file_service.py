from pathlib import Path

import pytest

from api.file_service import FileService, InvalidScopeError, UnsafePathError, FileMissingError


def _service(tmp_path: Path) -> FileService:
    return FileService({"content": tmp_path / "content"})


def test_write_and_read_file(tmp_path):
    service = _service(tmp_path)
    service.write_text("content", "news/test.txt", "hello")
    assert service.read_text("content", "news/test.txt") == "hello"


def test_list_directory_contains_created_file(tmp_path):
    service = _service(tmp_path)
    service.write_text("content", "news/test.txt", "hello")
    items = service.list_dir("content", "news")
    assert len(items) == 1
    assert items[0]["name"] == "test.txt"
    assert items[0]["is_dir"] is False


def test_rejects_unknown_scope(tmp_path):
    service = _service(tmp_path)
    with pytest.raises(InvalidScopeError):
        service.read_text("unknown", "test.txt")


def test_rejects_path_traversal(tmp_path):
    service = _service(tmp_path)
    with pytest.raises(UnsafePathError):
        service.read_text("content", "../secret.txt")


def test_delete_missing_file_returns_false(tmp_path):
    service = _service(tmp_path)
    assert service.delete_file("content", "missing.txt") is False


def test_read_missing_file_raises(tmp_path):
    service = _service(tmp_path)
    with pytest.raises(FileMissingError):
        service.read_text("content", "missing.txt")
