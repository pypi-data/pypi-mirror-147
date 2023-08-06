"""Python venv module library for skelly."""

import os.path
import subprocess
from types import SimpleNamespace
from typing import Optional
import venv


class RequirementsEnvBuilder(venv.EnvBuilder):
    """
    Custom EnvBuilder that pip installs the packages in a requirements file after
    the venv is created.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        req_file: str,
        install_dot: bool = True,
        system_site_packages: bool = False,
        clear: bool = False,
        symlinks: bool = False,
        upgrade: bool = False,
        prompt: Optional[str] = None,
        upgrade_deps: bool = False,
    ) -> None:
        self.req_file = req_file
        self.install_dot = install_dot
        super().__init__(
            system_site_packages,
            clear,
            symlinks,
            upgrade,
            True,  # with_pip is True because we need pip
            prompt,
            upgrade_deps,
        )

    def post_setup(self, context: SimpleNamespace) -> None:
        """
        Run pip to install the packages in the requirments file after the venv
        is created.
        """
        subprocess.run(
            [context.env_exe, "-m", "pip", "install", "-r", self.req_file], check=True
        )
        if self.install_dot:
            subprocess.run(
                [
                    context.env_exe,
                    "-m",
                    "pip",
                    "install",
                    "-e",
                    os.path.dirname(context.env_dir),
                ],
                check=True,
            )


def create_venv(
    target: str,
    env_dir: Optional[str] = None,
    req_file: Optional[str] = None,
    install_dot: bool = True,
) -> None:
    """Create a venv in the target, then pip install the requirements."""
    if not env_dir:
        env_dir = os.path.join(target, ".venv")
    if not req_file:
        req_file = os.path.join(target, "requirements.txt")
    envbuilder = RequirementsEnvBuilder(req_file, install_dot)
    envbuilder.create(env_dir)
