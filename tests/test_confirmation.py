from app.confirmation import Decision, evaluate_command
from app.permissions import RiskLevel


def test_read_only_is_allowed():
    result = evaluate_command("pwd")

    assert result.risk == RiskLevel.READ_ONLY
    assert result.decision == Decision.ALLOW


def test_modify_requires_confirmation():
    result = evaluate_command("git push")

    assert result.risk == RiskLevel.MODIFY
    assert result.decision == Decision.CONFIRM


def test_dangerous_is_blocked():
    result = evaluate_command("rm -rf test")

    assert result.risk == RiskLevel.DANGEROUS
    assert result.decision == Decision.BLOCK


def test_unknown_command_requires_confirmation():
    result = evaluate_command("some-unknown-command")

    assert result.risk == RiskLevel.MODIFY
    assert result.decision == Decision.CONFIRM
