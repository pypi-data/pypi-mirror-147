"""Create a Python package."""

import os.path
from typing import Optional, Mapping

from skelly.args import Args
from skelly.builder.builder import Builder, create_literal_mapping, create_re_any
from skelly.builder.python.venv import create_venv


class PythonBuilder(Builder):  # pylint: disable=too-few-public-methods
    """Builds a project to create a Python package."""

    def __init__(self, args: Args) -> None:
        super().__init__(args)

        # User provided template
        if self.template_path:
            return

        # Default template, so prompt for/assert missing required template vars
        if not self._args["silent"]:
            self._prompt_template_vars(
                [
                    ("Author", "author"),
                    ("Author email", "email"),
                    ("Description", "description"),
                    ("Repository", "repo"),
                ]
            )
        self._assert_template_vars(["author", "email", "description", "repo"], True)
        self.template_path = os.path.join(os.path.dirname(__file__), "template")

    def _get_builder_opt_env_dir(self) -> Optional[str]:
        """Get env_dir, if not an absolute path, relative to target."""
        env_dir = self._args["builder_opts"].get("env_dir", None)
        return (
            env_dir
            if not env_dir or os.path.isabs(env_dir)
            else os.path.join(self._args["target"], env_dir)
        )

    def _create_full_template_vars(self) -> Mapping[str, str]:
        """Return the full template vars for this builder."""
        name = self._get_template_var_name()
        return {
            **self._template_vars,
            **{
                "name": name,
                "name_h1": "=" * len(name),
                "issue_url": self._get_template_var_issue_url(),
            },
        }

    def build(self) -> None:
        self._copy_template_to_target()
        full_template_vars = self._create_full_template_vars()
        literal_template_vars = create_literal_mapping(full_template_vars)
        terms = create_re_any(literal_template_vars.keys())
        self._rename_in_target(literal_template_vars, terms)
        self._fill_in_target(literal_template_vars, terms)
        create_venv(
            self._args["target"],
            self._get_builder_opt_env_dir(),
            self._args["builder_opts"].get("req_file", None),
        )
