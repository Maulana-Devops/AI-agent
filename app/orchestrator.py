from dataclasses import dataclass

from app.confirmation import Decision, evaluate_command
from app.executor import CommandExecutor


@dataclass
class AgentResult:
    command: str
    decision: Decision
    executed: bool
    output: str = ""
    message: str = ""


class AgentOrchestrator:
    """Coordinate permission checks and command execution."""

    def __init__(self):
        self.executor = CommandExecutor()

    def run(self, command: str, *, confirmed: bool = False) -> AgentResult:
        permission = evaluate_command(command)

        if permission.decision == Decision.BLOCK:
            return AgentResult(
                command=command,
                decision=permission.decision,
                executed=False,
                message=permission.reason,
            )

        if permission.decision == Decision.CONFIRM and not confirmed:
            return AgentResult(
                command=command,
                decision=permission.decision,
                executed=False,
                message=permission.reason,
            )

        result = self.executor.execute(
            command,
            confirmed=confirmed,
        )

        return AgentResult(
            command=command,
            decision=permission.decision,
            executed=result.executed,
            output=result.output,
            message=result.error or permission.reason,
        )
