from pathlib import Path


class Workspace:
    """
    Menentukan workspace aktif tempat Laptop AI bekerja.
    """

    def __init__(self, root: str | None = None):
        if root:
            self.root = Path(root).expanduser().resolve()
        else:
            self.root = Path.cwd().resolve()

        if not self.root.exists():
            raise FileNotFoundError(
                f"Workspace tidak ditemukan: {self.root}"
            )

        if not self.root.is_dir():
            raise NotADirectoryError(
                f"Workspace bukan directory: {self.root}"
            )

    def path(self) -> str:
        return str(self.root)

    def contains(self, path: str) -> bool:
        """
        Memastikan path berada di dalam workspace.
        """
        target = Path(path).expanduser().resolve()

        try:
            target.relative_to(self.root)
            return True
        except ValueError:
            return False

    def resolve(self, path: str = ".") -> Path:
        """
        Resolve path relatif terhadap workspace.
        """
        target = Path(path).expanduser()

        if not target.is_absolute():
            target = self.root / target

        return target.resolve()

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
