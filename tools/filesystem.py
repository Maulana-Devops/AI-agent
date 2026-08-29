from pathlib import Path


def get_current_directory() -> str:
    """Return the current working directory."""
    return str(Path.cwd())


def list_directory(
    path: str = ".",
    recursive: bool = False,
    extension: str | None = None,
) -> list[str]:
    """List files and directories with optional recursion and extension filtering."""
    target = Path(path).resolve()

    if not target.exists():
        raise FileNotFoundError(f"Path tidak ditemukan: {target}")

    if not target.is_dir():
        raise NotADirectoryError(f"Bukan directory: {target}")

    entries = target.rglob("*") if recursive else target.iterdir()

    result = []

    for item in entries:
        if extension and item.is_file():
            normalized = extension if extension.startswith(".") else f".{extension}"
            if item.suffix != normalized:
                continue

        result.append(
            str(item.relative_to(target))
        )

    return sorted(result)


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


def copy_file(source: str, destination: str) -> str:
    """Copy a file to a new destination."""
    import shutil

    source_path = Path(source).resolve()
    destination_path = Path(destination).resolve()

    if not source_path.exists():
        raise FileNotFoundError(f"Tidak ditemukan: {source_path}")

    if not source_path.is_file():
        raise IsADirectoryError(f"Bukan file: {source_path}")

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination_path)

    return str(destination_path)


def delete_directory(path: str) -> str:
    """Delete a directory and its contents."""
    import shutil

    target = Path(path).resolve()

    if not target.exists():
        raise FileNotFoundError(f"Tidak ditemukan: {target}")

    if not target.is_dir():
        raise NotADirectoryError(f"Bukan direktori: {target}")

    shutil.rmtree(target)
    return str(target)


def get_file_info(path: str) -> dict:
    """Get basic metadata about a file or directory."""
    target = Path(path).resolve()

    if not target.exists():
        raise FileNotFoundError(f"Tidak ditemukan: {target}")

    return {
        "path": str(target),
        "name": target.name,
        "type": "directory" if target.is_dir() else "file",
        "size": target.stat().st_size,
        "extension": target.suffix if target.is_file() else "",
    }
