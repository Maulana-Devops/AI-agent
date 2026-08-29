from app.confirmation import Decision
from app.tool_gateway import ToolGateway


def test_read_only_command_is_executed():
    gateway = ToolGateway()

    result = gateway.execute("pwd")

    assert result.decision == Decision.ALLOW
    assert result.executed is True
    assert result.output


def test_modify_command_requires_confirmation():
    gateway = ToolGateway()

    result = gateway.execute("git push")

    assert result.decision == Decision.CONFIRM
    assert result.executed is False


def test_dangerous_command_is_blocked():
    gateway = ToolGateway()

    result = gateway.execute("rm -rf test")

    assert result.decision == Decision.BLOCK
    assert result.executed is False
