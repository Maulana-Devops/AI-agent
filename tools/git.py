import subprocess


def _run_git(args: list[str]) -> str:
    """Run a read-only Git command."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        error = result.stderr.strip() or "Git command gagal."
        raise RuntimeError(error)

    return result.stdout.strip()


def git_status() -> str:
    """Return Git working tree status."""
    return _run_git(["status", "--short", "--branch"])


def git_branch() -> str:
    """Return Git branches."""
    return _run_git(["branch", "--all"])


def git_log(limit: int = 10) -> str:
    """Return recent Git commits.

    An empty repository is treated as a valid state and returns
    a human-readable message instead of raising an error.
    """
    if limit < 1 or limit > 50:
        raise ValueError("limit harus antara 1 dan 50.")

    result = subprocess.run(
        ["git", "log", f"-{limit}", "--oneline", "--decorate"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        error = result.stderr.strip()

        if "does not have any commits yet" in error:
            return "Repository belum memiliki commit."

        raise RuntimeError(error or "Git command gagal.")

    return result.stdout.strip()


def git_diff() -> str:
    """Return unstaged Git diff."""
    return _run_git(["diff"])


def git_remote() -> str:
    """Return configured Git remotes."""
    return _run_git(["remote", "-v"])
