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
