import subprocess
import os
from pathlib import Path

from tools.registry import get_tool, list_tools
from tools.filesystem import (
    get_current_directory,
    list_directory,
    read_file,
)
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


def test_get_file_info_file(tmp_path):
    target = tmp_path / "example.txt"
    target.write_text("hello")

    tool = get_tool("get_file_info")

    assert tool is not None
    assert tool["risk"] == "read-only"

    result = tool["function"](str(target))

    assert result["name"] == "example.txt"
    assert result["type"] == "file"
    assert result["size"] == 5
    assert result["extension"] == ".txt"


def test_get_file_info_directory(tmp_path):
    target = tmp_path / "example-dir"
    target.mkdir()

    tool = get_tool("get_file_info")
    result = tool["function"](str(target))

    assert result["name"] == "example-dir"
    assert result["type"] == "directory"
    assert result["extension"] == ""


def test_get_file_info_file(tmp_path):
    target = tmp_path / "example.txt"
    target.write_text("hello")

    tool = get_tool("get_file_info")

    assert tool is not None
    assert tool["risk"] == "read-only"

    result = tool["function"](str(target))

    assert result["name"] == "example.txt"
    assert result["type"] == "file"
    assert result["size"] == 5
    assert result["extension"] == ".txt"


def test_get_file_info_directory(tmp_path):
    target = tmp_path / "example-dir"
    target.mkdir()

    tool = get_tool("get_file_info")
    result = tool["function"](str(target))

    assert result["name"] == "example-dir"
    assert result["type"] == "directory"
    assert result["extension"] == ""


def test_list_directory_recursive(tmp_path):
    (tmp_path / "root.txt").write_text("root")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "nested.txt").write_text("nested")

    tool = get_tool("list_directory")
    result = tool["function"](str(tmp_path), recursive=True)

    assert "root.txt" in result
    assert "sub" in result
    assert "sub/nested.txt" in result


def test_list_directory_extension_filter(tmp_path):
    (tmp_path / "one.txt").write_text("1")
    (tmp_path / "two.py").write_text("2")
    (tmp_path / "three.txt").write_text("3")

    tool = get_tool("list_directory")
    result = tool["function"](str(tmp_path), extension=".txt")

    assert result == ["one.txt", "three.txt"]
