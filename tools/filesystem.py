from pathlib import Path


def get_current_directory() -> str:
    """Return the current working directory."""
    return str(Path.cwd())


def list_directory(path: str = ".") -> list[str]:
    """List entries in a directory without modifying anything."""
    target = Path(path).resolve()

    if not target.exists():
        raise FileNotFoundError(f"Path tidak ditemukan: {target}")

    if not target.is_dir():
        raise NotADirectoryError(f"Bukan directory: {target}")

    return sorted(item.name for item in target.iterdir())


def read_file(path: str) -> str:
    """Read a text file without modifying it."""
    target = Path(path).resolve()

    if not target.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {target}")

    if not target.is_file():
        raise IsADirectoryError(f"Bukan file: {target}")

    return target.read_text(encoding="utf-8")
