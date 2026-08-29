from pathlib import Path


def get_current_directory() -> str:
    """Return the current working directory."""
    return str(Path.cwd())


def list_directory(path: str = ".") -> list[str]:
    """List files and directories in a directory without modifying anything."""
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


def create_directory(path: str) -> str:
    """Create a new directory."""
    target = Path(path).resolve()
    target.mkdir(parents=True, exist_ok=True)
    return str(target)


def write_file(path: str, content: str) -> str:
    """Write text content to a file."""
    target = Path(path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return str(target)


def delete_file(path: str) -> str:
    """Delete a file."""
    target = Path(path).resolve()

    if not target.exists():
        raise FileNotFoundError(f"Tidak ditemukan: {target}")

    if not target.is_file():
        raise IsADirectoryError(f"Bukan file: {target}")

    target.unlink()
    return str(target)


def move_file(source: str, destination: str) -> str:
    """Move or rename a file."""
    source_path = Path(source).resolve()
    destination_path = Path(destination).resolve()

    if not source_path.exists():
        raise FileNotFoundError(f"Tidak ditemukan: {source_path}")

    if not source_path.is_file():
        raise IsADirectoryError(f"Bukan file: {source_path}")

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.rename(destination_path)

    return str(destination_path)
