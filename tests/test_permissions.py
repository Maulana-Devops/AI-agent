from app.permissions import (
    RiskLevel,
    classify_command,
    is_allowed_without_confirmation,
    requires_confirmation,
    is_blocked,
)


def test_read_only_command():
    assert classify_command("pwd") == RiskLevel.READ_ONLY
    assert is_allowed_without_confirmation("pwd")


def test_modify_command():
    assert classify_command("git push") == RiskLevel.MODIFY
    assert requires_confirmation("git push")


def test_dangerous_command():
    assert classify_command("rm -rf test") == RiskLevel.DANGEROUS
    assert is_blocked("rm -rf test")


def test_unknown_command_is_not_trusted():
    assert classify_command("some-unknown-command") == RiskLevel.MODIFY
    assert requires_confirmation("some-unknown-command")
