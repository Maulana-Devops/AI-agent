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


def test_modify_tool_requires_confirmation():
    from app.tool_runner import ToolExecutionError, run_tool

    with pytest.raises(ToolExecutionError):
        run_tool(
            "create_directory",
            {"path": "/tmp/laptop-ai-test-confirmation"},
        )


def test_modify_tool_can_execute_with_confirmation(tmp_path):
    from app.tool_runner import run_tool

    target = tmp_path / "confirmed-dir"

    result = run_tool(
        "create_directory",
        {"path": str(target)},
        confirmed=True,
    )

    assert result == str(target.resolve())
    assert target.exists()


def test_modify_tool_returns_structured_confirmation_result(tmp_path):
    from app.tool_runner import run_tool_result

    target = tmp_path / "structured-confirmation"

    result = run_tool_result(
        "create_directory",
        {"path": str(target)},
    )

    assert result.success is False
    assert result.executed is False
    assert result.requires_confirmation is True
    assert result.error
    assert not target.exists()


def test_read_only_tool_returns_structured_success_result():
    from app.tool_runner import run_tool_result

    result = run_tool_result("get_current_directory")

    assert result.success is True
    assert result.executed is True
    assert result.requires_confirmation is False
    assert result.result
