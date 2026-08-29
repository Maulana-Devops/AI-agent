from app.confirmation import Decision
from app.orchestrator import AgentOrchestrator


agent = AgentOrchestrator()


def test_read_only_command_runs():
    result = agent.run("pwd")

    assert result.decision == Decision.ALLOW
    assert result.executed is True
    assert result.output


def test_modify_command_stops_for_confirmation():
    result = agent.run("git push")

    assert result.decision == Decision.CONFIRM
    assert result.executed is False


def test_modify_command_runs_after_confirmation():
    result = agent.run(
        "touch /tmp/laptop-ai-orchestrator-test",
        confirmed=True,
    )

    assert result.decision == Decision.CONFIRM
    assert result.executed is True

    import os
    os.remove("/tmp/laptop-ai-orchestrator-test")


def test_dangerous_command_never_runs():
    result = agent.run("rm -rf test")

    assert result.decision == Decision.BLOCK
    assert result.executed is False
