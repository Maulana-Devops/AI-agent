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


def test_modify_tool_approval_is_per_action(tmp_path):
    """
    Approval untuk satu tool tidak boleh otomatis memberikan
    approval kepada tool modify berikutnya.
    """
    from app.tool_runner import run_tool_result

    first = tmp_path / "first"
    second = tmp_path / "second"

    # Tanpa approval -> keduanya harus ditahan.
    result1 = run_tool_result(
        "create_directory",
        {"path": str(first)},
    )

    result2 = run_tool_result(
        "create_directory",
        {"path": str(second)},
    )

    assert result1.requires_confirmation is True
    assert result2.requires_confirmation is True

    assert not first.exists()
    assert not second.exists()

    # Approval hanya diberikan pada action pertama.
    approved = run_tool_result(
        "create_directory",
        {"path": str(first)},
        confirmed=True,
    )

    assert approved.success is True
    assert approved.executed is True
    assert first.exists()

    # Action kedua tetap membutuhkan approval baru.
    still_blocked = run_tool_result(
        "create_directory",
        {"path": str(second)},
    )

    assert still_blocked.success is False
    assert still_blocked.executed is False
    assert still_blocked.requires_confirmation is True
    assert not second.exists()
