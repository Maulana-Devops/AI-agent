from dataclasses import dataclass

from app.confirmation import Decision, evaluate_command
from app.executor import CommandExecutor


@dataclass
class ToolGatewayResult:
    decision: Decision
    executed: bool
    output: str = ""
    message: str = ""


class ToolGateway:
    """
    Security boundary between the AI and system command execution.

    The AI may request an action, but the gateway decides whether
    that action can actually be executed.
    """

    def __init__(self):
        self.executor = CommandExecutor()

    def execute(
        self,
        command: str,
        *,
        confirmed: bool = False,
    ) -> ToolGatewayResult:

        permission = evaluate_command(command)

        if permission.decision == Decision.BLOCK:
            return ToolGatewayResult(
                decision=Decision.BLOCK,
                executed=False,
                message=permission.reason,
            )

        if (
            permission.decision == Decision.CONFIRM
            and not confirmed
        ):
            return ToolGatewayResult(
                decision=Decision.CONFIRM,
                executed=False,
                message=permission.reason,
            )

        result = self.executor.execute(
            command,
            confirmed=confirmed,
        )

        return ToolGatewayResult(
            decision=permission.decision,
            executed=result.executed,
            output=result.output,
            message=result.error or permission.reason,
        )
