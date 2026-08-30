import pytest
import subprocess
import os
from pathlib import Path

from tools.registry import get_tool, list_tools
from tools.filesystem import (
    get_current_directory,
    list_directory,
    read_file,
)


@pytest.fixture
def filesystem_workspace(tmp_path):
    from app.workspace import Workspace
    from tools.filesystem import set_workspace

    ws = Workspace(tmp_path)
    set_workspace(ws)

    yield tmp_path

    set_workspace(None)

from tools.git import (
    git_status,
    git_branch,
    git_log,
    git_diff,
    git_remote,
)


def test_git_log_empty_repository(tmp_path):
    repo_dir = tmp_path / "empty_repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)

    old_cwd = os.getcwd()
    os.chdir(repo_dir)
    try:
        result = git_log(5)
        assert result == "Repository belum memiliki commit."
    finally:
        os.chdir(old_cwd)


def test_current_directory():
    result = get_current_directory()

    assert isinstance(result, str)
    assert Path(result).exists()


def test_list_directory():
    result = list_directory(".")

    assert isinstance(result, list)
    assert "app" in result
    assert "tools" in result
    assert "tests" in result


def test_read_file():
    result = read_file("README.md")

    assert isinstance(result, str)


def test_git_status():
    result = git_status()

    assert isinstance(result, str)
    assert "branch" in result.lower() or "##" in result


def test_git_branch():
    result = git_branch()

    assert isinstance(result, str)


def test_git_log():
    result = git_log(5)

    assert isinstance(result, str)


def test_git_diff():
    result = git_diff()

    assert isinstance(result, str)


def test_git_remote():
    result = git_remote()

    assert isinstance(result, str)


def test_registry_contains_read_only_tools():
    tools = list_tools()

    expected = {
        "get_current_directory",
        "list_directory",
        "read_file",
        "git_status",
        "git_branch",
        "git_log",
        "git_diff",
        "git_remote",
    }

    assert expected.issubset(tools.keys())

    for name in expected:
        assert tools[name]["risk"] == "read-only"


def test_registry_functions_are_callable():
    for name in list_tools():
        tool = get_tool(name)

        assert tool is not None
        assert callable(tool["function"])


def test_registry_create_directory_tool():
    tool = get_tool("create_directory")

    assert tool is not None
    assert tool["risk"] == "modify"


def test_registry_write_file_tool():
    tool = get_tool("write_file")

    assert tool is not None
    assert tool["risk"] == "modify"


def test_registry_delete_file_tool():
    tool = get_tool("delete_file")

    assert tool is not None
    assert tool["risk"] == "modify"


def test_registry_move_file_tool():
    tool = get_tool("move_file")

    assert tool is not None
    assert tool["risk"] == "modify"


def test_registry_copy_file_tool():
    tool = get_tool("copy_file")

    assert tool is not None
    assert tool["risk"] == "modify"


def test_registry_delete_directory_tool():
    tool = get_tool("delete_directory")

    assert tool is not None
    assert tool["risk"] == "modify"


def test_registry_delete_directory_tool():
    tool = get_tool("delete_directory")

    assert tool is not None
    assert tool["risk"] == "modify"


def test_get_file_info_file(filesystem_workspace):
    target = filesystem_workspace / "example.txt"
    target.write_text("hello")

    tool = get_tool("get_file_info")

    assert tool is not None
    assert tool["risk"] == "read-only"

    result = tool["function"](str(target))

    assert result["name"] == "example.txt"
    assert result["type"] == "file"
    assert result["size"] == 5
    assert result["extension"] == ".txt"


def test_get_file_info_directory(filesystem_workspace):
    target = filesystem_workspace / "example-dir"
    target.mkdir()

    tool = get_tool("get_file_info")
    result = tool["function"](str(target))

    assert result["name"] == "example-dir"
    assert result["type"] == "directory"
    assert result["extension"] == ""


def test_get_file_info_file(filesystem_workspace):
    target = filesystem_workspace / "example.txt"
    target.write_text("hello")

    tool = get_tool("get_file_info")

    assert tool is not None
    assert tool["risk"] == "read-only"

    result = tool["function"](str(target))

    assert result["name"] == "example.txt"
    assert result["type"] == "file"
    assert result["size"] == 5
    assert result["extension"] == ".txt"


def test_get_file_info_directory(filesystem_workspace):
    target = filesystem_workspace / "example-dir"
    target.mkdir()

    tool = get_tool("get_file_info")
    result = tool["function"](str(target))

    assert result["name"] == "example-dir"
    assert result["type"] == "directory"
    assert result["extension"] == ""


def test_list_directory_recursive(filesystem_workspace):
    (filesystem_workspace / "root.txt").write_text("root")
    sub = filesystem_workspace / "sub"
    sub.mkdir()
    (sub / "nested.txt").write_text("nested")

    tool = get_tool("list_directory")
    result = tool["function"](str(filesystem_workspace), recursive=True)

    assert "root.txt" in result
    assert "sub" in result
    assert "sub/nested.txt" in result


def test_list_directory_extension_filter(filesystem_workspace):
    (filesystem_workspace / "one.txt").write_text("1")
    (filesystem_workspace / "two.py").write_text("2")
    (filesystem_workspace / "three.txt").write_text("3")

    tool = get_tool("list_directory")
    result = tool["function"](str(filesystem_workspace), extension=".txt")

    assert result == ["one.txt", "three.txt"]


def test_search_files_by_pattern(filesystem_workspace):
    (filesystem_workspace / "main.py").write_text("print('hello')")
    (filesystem_workspace / "notes.txt").write_text("notes")

    sub = filesystem_workspace / "src"
    sub.mkdir()
    (sub / "app.py").write_text("app")

    tool = get_tool("search_files")

    assert tool is not None
    assert tool["risk"] == "read-only"

    result = tool["function"](str(filesystem_workspace), "*.py")

    assert result == ["main.py", "src/app.py"]


def test_search_file_contents(filesystem_workspace):
    (filesystem_workspace / "one.txt").write_text("hello world\npython is great")
    (filesystem_workspace / "two.txt").write_text("hello again")

    sub = filesystem_workspace / "src"
    sub.mkdir()
    (sub / "app.py").write_text("hello from python")

    tool = get_tool("search_file_contents")

    assert tool is not None
    assert tool["risk"] == "read-only"

    result = tool["function"](str(filesystem_workspace), "hello")

    assert len(result) == 3
    assert result[0]["path"] == "one.txt"
    assert result[0]["line"] == 1


def test_tool_runner_read_only_executes():
    from app.tool_runner import ToolRunner

    runner = ToolRunner()

    result = runner.run("get_current_directory")

    assert result.success is True
    assert result.executed is True
    assert result.requires_confirmation is False
    assert isinstance(result.result, str)


def test_tool_runner_modify_requires_confirmation(tmp_path):
    from app.tool_runner import ToolRunner

    runner = ToolRunner()

    target = tmp_path / "new-dir"

    result = runner.run(
        "create_directory",
        {"path": str(target)},
    )

    assert result.success is False
    assert result.executed is False
    assert result.requires_confirmation is True
    assert not target.exists()


def test_tool_runner_modify_with_confirmation(filesystem_workspace):
    from app.tool_runner import ToolRunner

    runner = ToolRunner()

    target = filesystem_workspace / "new-dir"

    result = runner.run(
        "create_directory",
        {"path": str(target)},
        confirmed=True,
    )

    assert result.success is True
    assert result.executed is True
    assert target.exists()


def test_tool_runner_unknown_tool():
    from app.tool_runner import ToolRunner

    runner = ToolRunner()

    result = runner.run("does_not_exist")

    assert result.success is False
    assert result.executed is False
