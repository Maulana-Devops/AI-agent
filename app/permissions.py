from enum import Enum


class RiskLevel(str, Enum):
    READ_ONLY = "read-only"
    MODIFY = "modify"
    DANGEROUS = "dangerous"


# Command yang aman untuk dibaca tanpa konfirmasi.
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


# Command yang mengubah sesuatu dan harus meminta konfirmasi.
MODIFY_COMMAND_PREFIXES = (
    "mkdir ",
    "touch ",
    "cp ",
    "mv ",
    "git add ",
    "git commit ",
    "git push",
    "git pull",
    "python ",
)


# Command yang kita blok secara default.
DANGEROUS_PREFIXES = (
    "rm ",
    "rm -",
    "sudo ",
    "su ",
    "mkfs",
    "fdisk",
    "parted ",
    "dd ",
    "shutdown",
    "reboot",
    "poweroff",
    "chmod 777",
    "chown ",
)


def classify_command(command: str) -> RiskLevel:
    """
    Classify a shell command into a risk level.

    This is intentionally conservative.
    Unknown commands are treated as MODIFY.
    """
    command = command.strip()

    if not command:
        return RiskLevel.DANGEROUS

    if command in READ_ONLY_COMMANDS:
        return RiskLevel.READ_ONLY

    for prefix in DANGEROUS_PREFIXES:
        if command.startswith(prefix):
            return RiskLevel.DANGEROUS

    for prefix in MODIFY_COMMAND_PREFIXES:
        if command.startswith(prefix):
            return RiskLevel.MODIFY

    # Unknown commands are not automatically trusted.
    return RiskLevel.MODIFY


def is_allowed_without_confirmation(command: str) -> bool:
    return classify_command(command) == RiskLevel.READ_ONLY


def requires_confirmation(command: str) -> bool:
    return classify_command(command) == RiskLevel.MODIFY


def is_blocked(command: str) -> bool:
    return classify_command(command) == RiskLevel.DANGEROUS
