from dataclasses import dataclass
from enum import Enum

from app.permissions import RiskLevel, classify_command


class Decision(str, Enum):
    ALLOW = "allow"
    CONFIRM = "confirm"
    BLOCK = "block"


@dataclass(frozen=True)
class PermissionDecision:
    command: str
    risk: RiskLevel
    decision: Decision
    reason: str


def evaluate_command(command: str) -> PermissionDecision:
    command = command.strip()
    risk = classify_command(command)

    if risk == RiskLevel.READ_ONLY:
        return PermissionDecision(
            command=command,
            risk=risk,
            decision=Decision.ALLOW,
            reason="Command read-only dan aman dijalankan.",
        )

    if risk == RiskLevel.MODIFY:
        return PermissionDecision(
            command=command,
            risk=risk,
            decision=Decision.CONFIRM,
            reason="Command dapat mengubah sistem atau data.",
        )

    return PermissionDecision(
        command=command,
        risk=risk,
        decision=Decision.BLOCK,
        reason="Command termasuk operasi berbahaya.",
    )
