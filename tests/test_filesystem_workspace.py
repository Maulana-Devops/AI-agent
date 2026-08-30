import shutil

import pytest

from app.workspace import Workspace
from tools import filesystem


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    ws = Workspace(tmp_path)
    filesystem.set_workspace(ws)

    yield ws

    filesystem.set_workspace(None)


def test_read_file_cannot_escape_workspace(tmp_path, workspace):
    outside = tmp_path.parent / f"{tmp_path.name}-outside.txt"
    outside.write_text("secret", encoding="utf-8")

    try:
        with pytest.raises(PermissionError):
            filesystem.read_file(str(outside))
    finally:
        outside.unlink(missing_ok=True)


def test_write_file_cannot_escape_workspace(tmp_path, workspace):
    outside = tmp_path.parent / f"{tmp_path.name}-outside.txt"

    try:
        with pytest.raises(PermissionError):
            filesystem.write_file(
                str(outside),
                "must not be written",
            )

        assert not outside.exists()
    finally:
        outside.unlink(missing_ok=True)


def test_create_directory_cannot_escape_workspace(tmp_path, workspace):
    outside = tmp_path.parent / f"{tmp_path.name}-outside-dir"

    try:
        with pytest.raises(PermissionError):
            filesystem.create_directory(str(outside))

        assert not outside.exists()
    finally:
        shutil.rmtree(outside, ignore_errors=True)


def test_delete_file_cannot_escape_workspace(tmp_path, workspace):
    outside = tmp_path.parent / f"{tmp_path.name}-outside.txt"
    outside.write_text("must survive", encoding="utf-8")

    try:
        with pytest.raises(PermissionError):
            filesystem.delete_file(str(outside))

        assert outside.exists()
    finally:
        outside.unlink(missing_ok=True)


def test_delete_directory_cannot_escape_workspace(tmp_path, workspace):
    outside = tmp_path.parent / f"{tmp_path.name}-outside-dir"
    outside.mkdir()

    (outside / "data.txt").write_text(
        "must survive",
        encoding="utf-8",
    )

    try:
        with pytest.raises(PermissionError):
            filesystem.delete_directory(str(outside))

        assert outside.exists()
    finally:
        shutil.rmtree(outside, ignore_errors=True)


def test_workspace_file_operations_still_work(workspace):
    target = workspace.root / "inside.txt"

    filesystem.write_file(
        str(target),
        "hello",
    )

    assert target.exists()
    assert filesystem.read_file(str(target)) == "hello"


def test_workspace_directory_operations_still_work(workspace):
    target = workspace.root / "inside-dir"

    filesystem.create_directory(str(target))

    assert target.exists()
    assert target.is_dir()
