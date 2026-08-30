from dataclasses import dataclass, field
from pathlib import Path

from app.workspace import Workspace


@dataclass
class ProjectInfo:
    root: str
    name: str
    technologies: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    indicators: dict[str, bool] = field(default_factory=dict)


class ProjectInspector:
    """
    Read-only project discovery.

    Inspector hanya membaca struktur workspace.
    Tidak membuat, mengubah, atau menghapus file.
    """

    INDICATORS = {
        "git": [".git"],
        "python": [
            "pyproject.toml",
            "requirements.txt",
            "setup.py",
            "setup.cfg",
        ],
        "docker": [
            "Dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
            "compose.yml",
            "compose.yaml",
        ],
        "node": [
            "package.json",
        ],
        "terraform": [
            "main.tf",
            "terraform.tf",
        ],
        "ansible": [
            "ansible.cfg",
            "playbook.yml",
            "playbook.yaml",
        ],
    }

    TECHNOLOGY_NAMES = {
        "git": "Git",
        "python": "Python",
        "docker": "Docker",
        "node": "Node.js",
        "terraform": "Terraform",
        "ansible": "Ansible",
    }

    def __init__(self, workspace: Workspace | None = None):
        self.workspace = workspace or Workspace()

    def inspect(self) -> ProjectInfo:
        root = Path(self.workspace.path())

        indicators = {}

        for technology, markers in self.INDICATORS.items():
            indicators[technology] = any(
                (root / marker).exists()
                for marker in markers
            )

        # Python juga dapat dikenali dari source file.
        # Ini berguna untuk project sederhana yang belum memiliki
        # pyproject.toml atau requirements.txt.
        if not indicators["python"]:
            indicators["python"] = any(
                item.suffix == ".py"
                for item in root.rglob("*.py")
                if not any(
                    part in {
                        ".git",
                        "__pycache__",
                        ".pytest_cache",
                        ".venv",
                        "venv",
                    }
                    for part in item.relative_to(root).parts
                )
            )

        technologies = [
            self.TECHNOLOGY_NAMES[name]
            for name, detected in indicators.items()
            if detected
        ]

        files = self._list_files(root)

        return ProjectInfo(
            root=str(root),
            name=root.name,
            technologies=technologies,
            files=files,
            indicators=indicators,
        )

    def _list_files(self, root: Path) -> list[str]:
        """
        List file paths relatif terhadap workspace.

        Directory .git dan cache Python tidak dimasukkan agar
        hasil discovery tetap relevan.
        """
        ignored_directories = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".venv",
            "venv",
            "node_modules",
        }

        result = []

        for item in root.rglob("*"):
            if not item.is_file():
                continue

            relative = item.relative_to(root)

            if any(
                part in ignored_directories
                for part in relative.parts
            ):
                continue

            result.append(str(relative))

        return sorted(result)
