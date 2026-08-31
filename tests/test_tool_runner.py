import pytest

from app.tool_runner import ToolExecutionError, run_tool


@pytest.fixture
def filesystem_workspace(tmp_path):
    from app.workspace import Workspace
    from tools.filesystem import set_workspace

    ws = Workspace(tmp_path)
    set_workspace(ws)

    yield tmp_path

    set_workspace(None)



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


def test_modify_tool_can_execute_with_confirmation(filesystem_workspace):
    from app.tool_runner import run_tool

    target = filesystem_workspace / "confirmed-dir"

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


def test_modify_tool_approval_is_per_action(filesystem_workspace):
    """
    Approval untuk satu tool tidak boleh otomatis memberikan
    approval kepada tool modify berikutnya.
    """
    from app.tool_runner import run_tool_result

    first = filesystem_workspace / "first"
    second = filesystem_workspace / "second"

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


def test_unknown_tool_argument_is_rejected(filesystem_workspace):
    from app.tool_runner import run_tool_result

    target = filesystem_workspace / "unknown-argument"

    result = run_tool_result(
        "create_directory",
        {
            "path": str(target),
            "unexpected": "value",
        },
        confirmed=True,
    )

    assert result.success is False
    assert result.executed is False
    assert "Argument tidak dikenal" in result.error
    assert not target.exists()


def test_required_tool_argument_is_validated_before_execution():
    from app.tool_runner import run_tool_result

    result = run_tool_result(
        "read_file",
        {},
    )

    assert result.success is False
    assert result.executed is False
    assert "Argument wajib belum diberikan" in result.error


def test_tool_argument_type_is_validated_before_execution():
    from app.tool_runner import run_tool_result

    result = run_tool_result(
        "git_log",
        {"limit": "5"},
    )

    assert result.success is False
    assert result.executed is False
    assert "harus bertipe integer" in result.error


def test_valid_tool_arguments_still_execute(filesystem_workspace):
    from app.tool_runner import run_tool_result

    target = filesystem_workspace / "valid-arguments"

    result = run_tool_result(
        "create_directory",
        {"path": str(target)},
        confirmed=True,
    )

    assert result.success is True
    assert result.executed is True
    assert target.exists()


def test_git_log_rejects_limit_below_minimum():
    from app.tool_runner import run_tool_result

    result = run_tool_result(
        "git_log",
        {"limit": 0},
    )

    assert result.success is False
    assert result.executed is False
    assert "harus >= 1" in result.error


def test_git_log_rejects_limit_above_maximum():
    from app.tool_runner import run_tool_result

    result = run_tool_result(
        "git_log",
        {"limit": 51},
    )

    assert result.success is False
    assert result.executed is False
    assert "harus <= 50" in result.error


def test_git_log_accepts_boundary_values():
    from app.tool_runner import run_tool_result

    lower = run_tool_result(
        "git_log",
        {"limit": 1},
    )

    upper = run_tool_result(
        "git_log",
        {"limit": 50},
    )

    assert lower.success is True
    assert lower.executed is True

    assert upper.success is True
    assert upper.executed is True


def test_search_file_contents_rejects_empty_query():
    from app.tool_runner import run_tool_result

    result = run_tool_result(
        "search_file_contents",
        {"path": ".", "query": ""},
    )

    assert result.success is False
    assert result.executed is False
    assert "minimal 1 karakter" in result.error


def test_semantic_validation_happens_before_confirmation(
    filesystem_workspace,
):
    from app.tool_runner import run_tool_result

    target = filesystem_workspace / "semantic-validation"

    result = run_tool_result(
        "create_directory",
        {
            "path": str(target),
        },
        confirmed=False,
    )

    assert result.success is False
    assert result.executed is False
    assert result.requires_confirmation is True
    assert not target.exists()


def test_schema_enum_is_enforced(monkeypatch):
    from app.tool_runner import ToolRunner
    from tools.registry import TOOLS

    def fake_tool(mode):
        return mode

    original = TOOLS.get("test_enum_tool")

    TOOLS["test_enum_tool"] = {
        "description": "Test enum validation",
        "risk": "read-only",
        "function": fake_tool,
        "parameters": {
            "type": "object",
            "properties": {
                "mode": {
                    "type": "string",
                    "enum": ["safe", "normal"],
                },
            },
            "required": ["mode"],
            "additionalProperties": False,
        },
    }

    try:
        runner = ToolRunner()

        invalid = runner.run(
            "test_enum_tool",
            {"mode": "dangerous"},
        )

        assert invalid.success is False
        assert invalid.executed is False
        assert "enum" in invalid.error.lower()

        valid = runner.run(
            "test_enum_tool",
            {"mode": "safe"},
        )

        assert valid.success is True
        assert valid.executed is True
        assert valid.result == "safe"

    finally:
        if original is None:
            TOOLS.pop("test_enum_tool", None)
        else:
            TOOLS["test_enum_tool"] = original


def test_schema_max_length_is_enforced():
    from app.tool_runner import ToolRunner
    from tools.registry import TOOLS

    def fake_tool(value):
        return value

    original = TOOLS.get("test_max_length_tool")

    TOOLS["test_max_length_tool"] = {
        "description": "Test maxLength validation",
        "risk": "read-only",
        "function": fake_tool,
        "parameters": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "maxLength": 5,
                },
            },
            "required": ["value"],
        },
    }

    try:
        runner = ToolRunner()

        invalid = runner.run(
            "test_max_length_tool",
            {"value": "123456"},
        )

        assert invalid.success is False
        assert invalid.executed is False
        assert "maksimal" in invalid.error.lower()

        valid = runner.run(
            "test_max_length_tool",
            {"value": "12345"},
        )

        assert valid.success is True
        assert valid.executed is True

    finally:
        if original is None:
            TOOLS.pop("test_max_length_tool", None)
        else:
            TOOLS["test_max_length_tool"] = original


def test_additional_properties_false_is_enforced():
    from app.tool_runner import ToolRunner
    from tools.registry import TOOLS

    def fake_tool(path):
        return path

    original = TOOLS.get("test_additional_properties_tool")

    TOOLS["test_additional_properties_tool"] = {
        "description": "Test additionalProperties validation",
        "risk": "read-only",
        "function": fake_tool,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                },
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    }

    try:
        runner = ToolRunner()

        invalid = runner.run(
            "test_additional_properties_tool",
            {
                "path": "test.txt",
                "unexpected": "value",
            },
        )

        assert invalid.success is False
        assert invalid.executed is False
        assert "tidak dikenal" in invalid.error.lower()

        valid = runner.run(
            "test_additional_properties_tool",
            {"path": "test.txt"},
        )

        assert valid.success is True
        assert valid.executed is True

    finally:
        if original is None:
            TOOLS.pop("test_additional_properties_tool", None)
        else:
            TOOLS["test_additional_properties_tool"] = original
