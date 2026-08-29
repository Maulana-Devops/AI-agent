import subprocess
from dataclasses import dataclass

from app.permissions import (
    RiskLevel,
    classify_command,
)


@dataclass
class ExecutionResult:
    command: str
    risk: RiskLevel
    executed: bool
    output: str = ""
    error: str = ""


class CommandExecutor:
    """Execute shell commands according to the permission policy."""

    def execute(
        self,
        command: str,
        *,
        confirmed: bool = False,
    ) -> ExecutionResult:
        command = command.strip()

        if not command:
            return ExecutionResult(
                command=command,
                risk=RiskLevel.DANGEROUS,
                executed=False,
                error="Command kosong.",
            )

        risk = classify_command(command)

        if risk == RiskLevel.DANGEROUS:
            return ExecutionResult(
                command=command,
                risk=risk,
                executed=False,
                error="Command diblokir oleh permission policy.",
            )

        if risk == RiskLevel.MODIFY and not confirmed:
            return ExecutionResult(
                command=command,
                risk=risk,
                executed=False,
                error="Konfirmasi diperlukan sebelum menjalankan command.",
            )

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False,
        )

        return ExecutionResult(
            command=command,
            risk=risk,
            executed=True,
            output=result.stdout.strip(),
            error=result.stderr.strip(),
        )
