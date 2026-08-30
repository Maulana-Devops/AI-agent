from app.project_inspector import ProjectInspector
from app.workspace import Workspace


def test_inspector_detects_current_project():
    inspector = ProjectInspector()

    info = inspector.inspect()

    assert info.root
    assert info.name
    assert "Python" in info.technologies
    assert "Git" in info.technologies


def test_inspector_detects_docker_project(tmp_path):
    (tmp_path / "Dockerfile").write_text("FROM python:3.12\n")

    workspace = Workspace(str(tmp_path))
    inspector = ProjectInspector(workspace)

    info = inspector.inspect()

    assert "Docker" in info.technologies
    assert info.indicators["docker"] is True


def test_inspector_detects_node_project(tmp_path):
    (tmp_path / "package.json").write_text("{}")

    workspace = Workspace(str(tmp_path))
    inspector = ProjectInspector(workspace)

    info = inspector.inspect()

    assert "Node.js" in info.technologies
    assert info.indicators["node"] is True


def test_inspector_lists_project_files(tmp_path):
    (tmp_path / "app.py").write_text("print('hello')\n")
    (tmp_path / "README.md").write_text("# Test\n")

    workspace = Workspace(str(tmp_path))
    inspector = ProjectInspector(workspace)

    info = inspector.inspect()

    assert "app.py" in info.files
    assert "README.md" in info.files


def test_inspector_ignores_git_and_cache(tmp_path):
    git_dir = tmp_path / ".git"
    cache_dir = tmp_path / "__pycache__"

    git_dir.mkdir()
    cache_dir.mkdir()

    (git_dir / "config").write_text("git")
    (cache_dir / "test.pyc").write_bytes(b"cache")

    (tmp_path / "main.py").write_text("print('hello')\n")

    workspace = Workspace(str(tmp_path))
    inspector = ProjectInspector(workspace)

    info = inspector.inspect()

    assert "main.py" in info.files
    assert ".git/config" not in info.files
    assert "__pycache__/test.pyc" not in info.files
