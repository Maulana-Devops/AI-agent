from pathlib import Path
import os


class Workspace:
    """
    Menentukan root workspace berdasarkan current working directory
    saat object Workspace dibuat.
    """

    def __init__(self, root: str | os.PathLike | None = None):
        if root is None:
            root = os.getcwd()

        self.root = Path(root).expanduser().resolve()

    def path(self) -> str:
        """Return absolute workspace root sebagai string."""
        return str(self.root)

    def resolve(self, path: str = ".") -> Path:
        """
        Resolve path secara absolut.
        Relative path dianggap relatif terhadap workspace root.
        """
        candidate = Path(path).expanduser()

        if not candidate.is_absolute():
            candidate = self.root / candidate

        return candidate.resolve()

    def contains(self, path: str) -> bool:
        """
        True jika path berada di dalam workspace.
        Workspace root sendiri juga dianggap valid.
        """
        target = Path(path).resolve()

        try:
            target.relative_to(self.root)
            return True
        except ValueError:
            return False

    def require_inside(self, path: str = ".") -> Path:
        """
        Resolve path dan pastikan tetap berada di dalam workspace.
        """
        target = self.resolve(path)

        if not self.contains(str(target)):
            raise PermissionError(
                f"Path berada di luar workspace: {target}"
            )

        return target
