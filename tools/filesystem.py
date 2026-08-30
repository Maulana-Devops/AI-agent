from pathlib import Path

from app.workspace import Workspace


_workspace = None


def set_workspace(workspace):
    """
    Set workspace aktif untuk membatasi operasi filesystem.

    Jika workspace None, filesystem berjalan tanpa boundary eksplisit
    untuk menjaga kompatibilitas dengan pemanggil lama dan test.
    """
    global _workspace
    _workspace = workspace


def get_workspace():
    """Return workspace aktif."""
    return _workspace


def _workspace_path(path: str = ".") -> Path:
    """
    Resolve path dan pastikan berada di dalam workspace.

    Jika workspace eksplisit belum dipasang, current working directory
    digunakan sebagai workspace default.
    """
    if _workspace is None:
        return Workspace().require_inside(path)

    return _workspace.require_inside(path)

def get_current_directory() -> str:
    """Return the current working directory."""
    return str(Path.cwd())


def list_directory(
    path: str = ".",
    recursive: bool = False,
    extension: str | None = None,
) -> list[str]:
    """List files and directories with optional recursion and extension filtering."""
    target = _workspace_path(path)

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

        result.append(str(item.relative_to(target)))

    return sorted(result)


def read_file(path: str) -> str:
    """Read a text file without modifying it."""
    target = _workspace_path(path)

    if not target.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {target}")

    if not target.is_file():
        raise IsADirectoryError(f"Bukan file: {target}")

    return target.read_text(encoding="utf-8")


def create_directory(path: str) -> str:
    """Create a new directory."""
    target = _workspace_path(path)
    target.mkdir(parents=True, exist_ok=True)
    return str(target)


def write_file(path: str, content: str) -> str:
    """Write text content to a file."""
    target = _workspace_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return str(target)


def delete_file(path: str) -> str:
    """Delete a file."""
    target = _workspace_path(path)

    if not target.exists():
        raise FileNotFoundError(f"Tidak ditemukan: {target}")

    if not target.is_file():
        raise IsADirectoryError(f"Bukan file: {target}")

    target.unlink()
    return str(target)


def move_file(source: str, destination: str) -> str:
    """Move or rename a file."""
    source_path = _workspace_path(source)
    destination_path = _workspace_path(destination)

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

    source_path = _workspace_path(source)
    destination_path = _workspace_path(destination)

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

    target = _workspace_path(path)

    if not target.exists():
        raise FileNotFoundError(f"Tidak ditemukan: {target}")

    if not target.is_dir():
        raise NotADirectoryError(f"Bukan direktori: {target}")

    shutil.rmtree(target)
    return str(target)


def get_file_info(path: str) -> dict:
    """Get basic metadata about a file or directory."""
    target = _workspace_path(path)

    if not target.exists():
        raise FileNotFoundError(f"Tidak ditemukan: {target}")

    return {
        "path": str(target),
        "name": target.name,
        "type": "directory" if target.is_dir() else "file",
        "size": target.stat().st_size,
        "extension": target.suffix if target.is_file() else "",
    }


def search_files(path: str = ".", pattern: str = "*") -> list[str]:
    """Search files recursively by filename pattern."""
    target = _workspace_path(path)

    if not target.exists():
        raise FileNotFoundError(f"Path tidak ditemukan: {target}")

    if not target.is_dir():
        raise NotADirectoryError(f"Bukan directory: {target}")

    return sorted(
        str(item.relative_to(target))
        for item in target.rglob(pattern)
        if item.is_file()
    )


def search_file_contents(path: str = ".", query: str = "") -> list[dict]:
    """Search text inside files recursively."""
    target = _workspace_path(path)

    if not target.exists():
        raise FileNotFoundError(f"Path tidak ditemukan: {target}")

    if not target.is_dir():
        raise NotADirectoryError(f"Bukan directory: {target}")

    if not query:
        raise ValueError("Query tidak boleh kosong")

    results = []

    for item in target.rglob("*"):
        if not item.is_file():
            continue

        try:
            lines = item.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, PermissionError):
            continue

        for number, line in enumerate(lines, 1):
            if query in line:
                results.append({
                    "path": str(item.relative_to(target)),
                    "line": number,
                    "content": line,
                })

    return results
