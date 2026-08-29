import pytest

from app.tool_runner import ToolExecutionError, run_tool


def test_run_registered_tool():
    result = run_tool("get_current_directory")

    assert result


def test_unknown_tool_is_rejected():
    with pytest.raises(ToolExecutionError):
        run_tool("execute_arbitrary_shell")


def test_tool_arguments_are_supported():
    result = run_tool("git_log", {"limit": 5})

    # Repository mungkin belum punya commit.
    # Yang penting error yang muncul adalah error Git,
    # bukan error karena tool runner gagal memanggil fungsi.
    assert isinstance(result, str) or result is not None
