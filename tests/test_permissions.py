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


def test_modify_command_mkdir():
    assert classify_command("mkdir /tmp/test-dir") == RiskLevel.MODIFY
    assert requires_confirmation("mkdir /tmp/test-dir")


def test_modify_command_write_file():
    assert classify_command("write_file") == RiskLevel.MODIFY
    assert requires_confirmation("write_file")


def test_command_classification_handles_extra_whitespace():
    assert classify_command("  mkdir /tmp/test-dir  ") == RiskLevel.MODIFY
    assert classify_command("  ls  ") == RiskLevel.READ_ONLY


def test_rm_remains_dangerous():
    assert classify_command("rm /tmp/test.txt") == RiskLevel.DANGEROUS
    assert classify_command("rm -rf /tmp/test-dir") == RiskLevel.DANGEROUS


def test_command_parser_handles_multiple_spaces():
    assert classify_command("  mkdir    /tmp/test-dir  ") == RiskLevel.MODIFY
    assert classify_command("  ls   ") == RiskLevel.READ_ONLY


def test_command_parser_detects_command_name():
    assert classify_command("mkdir /tmp/test-dir") == RiskLevel.MODIFY
    assert classify_command("cp source.txt destination.txt") == RiskLevel.MODIFY
    assert classify_command("mv source.txt destination.txt") == RiskLevel.MODIFY


def test_dangerous_command_name_is_blocked():
    assert classify_command("rm file.txt") == RiskLevel.DANGEROUS
    assert classify_command("rm -rf directory") == RiskLevel.DANGEROUS
    assert classify_command("sudo mkdir test") == RiskLevel.DANGEROUS


def test_unknown_command_remains_modify():
    assert classify_command("some-unknown-command --test") == RiskLevel.MODIFY


def test_empty_command_is_dangerous():
    assert classify_command("") == RiskLevel.DANGEROUS


def test_shell_quoted_argument_does_not_change_command_classification():
    assert classify_command('mkdir "/tmp/my folder"') == RiskLevel.MODIFY
