"""Сервис безопасного доступа к файлам сайта для админ API."""
from pathlib import Path


class FileServiceError(Exception):
    """Базовая ошибка файлового сервиса."""


class InvalidScopeError(FileServiceError):
    """Ошибка при неизвестной области файлов."""


class UnsafePathError(FileServiceError):
    """Ошибка при небезопасном пути."""


class FileMissingError(FileServiceError):
    """Файл не найден."""


class FileService:
    """Ограниченный доступ к файлам в заранее разрешённых корнях."""

    def __init__(self, allowed_roots: dict[str, Path]):
        self._allowed_roots = {
            scope: Path(root).resolve() for scope, root in allowed_roots.items()
        }

    def scopes(self) -> list[str]:
        return sorted(self._allowed_roots.keys())

    def list_dir(self, scope: str, rel_path: str = "") -> list[dict]:
        target = self._resolve(scope, rel_path)
        if not target.exists():
            raise FileMissingError("Путь не найден")
        if not target.is_dir():
            raise FileServiceError("Указанный путь не является директорией")
        items = []
        for child in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
            items.append(
                {
                    "name": child.name,
                    "path": self._relative(scope, child),
                    "is_dir": child.is_dir(),
                    "size": child.stat().st_size if child.is_file() else None,
                }
            )
        return items

    def read_text(self, scope: str, rel_path: str) -> str:
        target = self._resolve(scope, rel_path)
        if not target.exists() or not target.is_file():
            raise FileMissingError("Файл не найден")
        return target.read_text(encoding="utf-8")

    def write_text(self, scope: str, rel_path: str, content: str) -> None:
        target = self._resolve(scope, rel_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def delete_file(self, scope: str, rel_path: str) -> bool:
        target = self._resolve(scope, rel_path)
        if not target.exists():
            return False
        if target.is_dir():
            raise FileServiceError("Удаление директорий не поддерживается")
        target.unlink()
        return True

    def _resolve(self, scope: str, rel_path: str) -> Path:
        root = self._allowed_roots.get(scope)
        if root is None:
            raise InvalidScopeError(f"Неизвестная область: {scope}")
        normalized = (rel_path or "").strip().replace("\\", "/").lstrip("/")
        if normalized in ("", "."):
            return root
        candidate = (root / normalized).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise UnsafePathError("Недопустимый путь") from exc
        return candidate

    def _relative(self, scope: str, abs_path: Path) -> str:
        root = self._allowed_roots[scope]
        rel = abs_path.resolve().relative_to(root).as_posix()
        return "" if rel == "." else rel


def build_default_file_service(project_root: str) -> FileService:
    """Создаёт стандартный набор доступных корней для админки."""
    root = Path(project_root).resolve()
    return FileService(
        {
            "content": root / "data",
            "locales": root / "static" / "locales",
            "templates": root / "templates",
        }
    )
