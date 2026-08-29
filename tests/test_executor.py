from app.executor import CommandExecutor
from app.permissions import RiskLevel


executor = CommandExecutor()


def test_read_only_command_executes():
    result = executor.execute("pwd")

    assert result.risk == RiskLevel.READ_ONLY
    assert result.executed is True
    assert result.output


def test_modify_command_requires_confirmation():
    result = executor.execute("git push")

    assert result.risk == RiskLevel.MODIFY
    assert result.executed is False
    assert "Konfirmasi" in result.error


def test_modify_command_executes_after_confirmation():
    result = executor.execute(
        "touch /tmp/laptop-ai-executor-test",
        confirmed=True,
    )

    assert result.risk == RiskLevel.MODIFY
    assert result.executed is True

    # Cleanup test artifact manually through Python, not the executor.
    import os
    os.remove("/tmp/laptop-ai-executor-test")


def test_dangerous_command_is_blocked():
    result = executor.execute("rm -rf test")

    assert result.risk == RiskLevel.DANGEROUS
    assert result.executed is False


def test_unknown_command_requires_confirmation():
    result = executor.execute("some-unknown-command")

    assert result.risk == RiskLevel.MODIFY
    assert result.executed is False


def test_modify_command_mkdir_without_confirmation_not_executed(tmp_path):
    result = executor.execute("mkdir " + str(tmp_path / "new-dir"), confirmed=False)

    assert result.risk == RiskLevel.MODIFY
    assert result.executed is False
    assert not (tmp_path / "new-dir").exists()


def test_modify_command_mkdir_with_confirmation_executed(tmp_path):
    result = executor.execute(
        "mkdir " + str(tmp_path / "new-dir"),
        confirmed=True,
    )

    assert result.risk == RiskLevel.MODIFY
    assert result.executed is True
    assert (tmp_path / "new-dir").exists()
