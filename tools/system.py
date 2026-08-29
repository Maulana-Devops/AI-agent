from pathlib import Path


def get_current_directory() -> str:
    """Return the current working directory."""
    return str(Path.cwd())
