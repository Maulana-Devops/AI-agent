from enum import Enum
import shlex


class RiskLevel(str, Enum):
    READ_ONLY = "read-only"
    MODIFY = "modify"
    DANGEROUS = "dangerous"


# Exact commands yang aman dibaca tanpa konfirmasi.
READ_ONLY_COMMANDS = {
    "pwd",
    "ls",
    "git status",
    "git diff",
    "git log",
    "git branch",
    "git remote -v",
    "whoami",
    "uname",
    "python --version",
    "python -V",
    "pip --version",
}


# Command dasar yang mengubah filesystem / repository.
MODIFY_COMMANDS = {
    "mkdir",
    "touch",
    "cp",
    "mv",
    "git add",
    "git commit",
    "git push",
    "git pull",
    "python",
}


# Command yang selalu diblokir.
DANGEROUS_COMMANDS = {
    "rm",
    "sudo",
    "su",
    "mkfs",
    "fdisk",
    "parted",
    "dd",
    "shutdown",
    "reboot",
    "poweroff",
}


def _normalize_command(command: str) -> str:
    """Normalize whitespace without changing command semantics."""
    return " ".join(command.strip().split())


def _command_name(command: str) -> str:
    """Return the first shell token."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return ""

    return tokens[0] if tokens else ""


def classify_command(command: str) -> RiskLevel:
    """
    Classify a shell command into a risk level.

    Policy:
    - known read-only commands -> READ_ONLY
    - dangerous command names -> DANGEROUS
    - known modifying command names -> MODIFY
    - unknown commands -> MODIFY
    """
    command = _normalize_command(command)

    if not command:
        return RiskLevel.DANGEROUS

    if command in READ_ONLY_COMMANDS:
        return RiskLevel.READ_ONLY

    name = _command_name(command)

    if name in DANGEROUS_COMMANDS:
        return RiskLevel.DANGEROUS

    if name in MODIFY_COMMANDS:
        return RiskLevel.MODIFY

    return RiskLevel.MODIFY


def is_allowed_without_confirmation(command: str) -> bool:
    return classify_command(command) == RiskLevel.READ_ONLY


def requires_confirmation(command: str) -> bool:
    return classify_command(command) == RiskLevel.MODIFY


def is_blocked(command: str) -> bool:
    return classify_command(command) == RiskLevel.DANGEROUS
