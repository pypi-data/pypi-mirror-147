"""Git module library for skelly."""

import subprocess


def init_git(target: str, main_branch: str = "main") -> None:
    """Init a git repo inside the target."""
    subprocess.run(["git", "init", "-b", main_branch], cwd=target, check=True)
