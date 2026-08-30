import pytest

from app.workspace import Workspace


def test_workspace_defaults_to_current_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    workspace = Workspace()

    assert workspace.path() == str(tmp_path.resolve())


def test_workspace_resolves_relative_path(tmp_path):
    workspace = Workspace(str(tmp_path))

    result = workspace.resolve("project/file.txt")

    assert result == (
        tmp_path / "project" / "file.txt"
    ).resolve()


def test_workspace_accepts_path_inside_workspace(tmp_path):
    workspace = Workspace(str(tmp_path))

    target = tmp_path / "project" / "file.txt"

    assert workspace.contains(str(target))


def test_workspace_rejects_path_outside_workspace(tmp_path):
    workspace = Workspace(str(tmp_path))

    outside = tmp_path.parent / "outside.txt"

    assert not workspace.contains(str(outside))


def test_require_inside_rejects_escape(tmp_path):
    workspace = Workspace(str(tmp_path))

    with pytest.raises(PermissionError):
        workspace.require_inside("../outside")
