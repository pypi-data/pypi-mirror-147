"""Utilities for target builders."""

from abc import ABCMeta, abstractmethod
from collections.abc import Iterable, Mapping
import os
import os.path
import re
import shutil
import tempfile
from types import TracebackType
from typing import Callable, Optional, Pattern, Tuple, Type, TypeVar

from ..args import Args, prompt_args


class Template:
    """
    Context manager for a template directory, which can either be a static directory,
    or an archive that the context manager will unpacked to a temp directory and
    delete when complete.
    """

    def __init__(self, template_path: str) -> None:
        self._template_path = template_path
        self._temp_dir: Optional[str] = None

    def __enter__(self) -> str:
        # Template is a directory, so return its path
        if os.path.isdir(self._template_path):
            return self._template_path

        # Template is a file, so it should be an archive, so try to unpack it
        self._temp_dir = tempfile.mkdtemp()
        try:
            shutil.unpack_archive(self._template_path, self._temp_dir)
        except BaseException:
            shutil.rmtree(self._temp_dir)
            raise
        return self._temp_dir

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self._temp_dir:
            shutil.rmtree(self._temp_dir)


class Builder(metaclass=ABCMeta):  # pylint: disable=too-few-public-methods
    """ABC for builder plugins."""

    @abstractmethod
    def __init__(self, args: Args) -> None:
        self._args = args
        self._name = self._args["builder"]
        self._template_vars = dict(self._args["template_vars"])
        self.template_path = self._args["template_path"]

    @abstractmethod
    def build(self) -> None:
        """Build the project."""

    def _prompt_template_vars(self, spec: Iterable[Tuple[str, str]]) -> None:
        """Prompt for missing template variables."""
        self._template_vars.update(
            prompt_args(
                [
                    (prompt, name, None)
                    for prompt, name in spec
                    if name not in self._template_vars
                ]
            )
        )

    def _assert_template_vars(
        self, required_vars: Iterable[str], strict: bool = False
    ) -> None:
        """Assert the required template vars are present."""
        expected = sorted(required_vars)
        actual = sorted(self._template_vars.keys())
        if strict:
            if not all(exp in actual for exp in expected):
                raise AssertionError(
                    "incorrect template variables"
                    + f": template variables = {actual}"
                    + f": expected variables = {expected}"
                )
        else:
            if expected > actual:
                raise AssertionError(
                    "missing required template variables"
                    + f": template variables = {actual}"
                    + f": expected variables = {expected}"
                )

    def _get_template_var_name(self) -> str:
        """Get or derive the name for use in templates."""
        return self._template_vars.get("name", self._args["name"])

    def _get_template_var_issue_url(self) -> str:
        """Get or derive the issue tracking URL for use in templates."""
        issue_url = self._template_vars.get("issue_url", None)
        if issue_url:
            return issue_url
        repo = self._template_vars.get("repo", None)
        if not repo:
            raise ValueError("missing repo, could not derive issue_url")
        if repo.startswith("https://gitlab.com"):
            return f"{repo}/-/issues"
        if repo.startswith("https://github.com"):
            return f"{repo}/issues"
        raise ValueError(f"unknown repo: {repo}: could not derive issue_url")

    def _fill_target(self, fill: Callable[[str], None]) -> None:
        """Fill a template and copy it to the target."""
        if not self.template_path:
            raise RuntimeError(f"builder '{self._name}' template path not set")

        target = self._args["target"]

        # Template can be copied as the target and filled there since the target
        # doesn't exist yet
        if not os.path.exists(target):
            with Template(self.template_path) as template:
                shutil.copytree(template, target)
            fill(target)
            return

        if not os.path.isdir(target):
            raise NotADirectoryError(
                f"builder '{self._name}' target is not a directory: {target}"
            )

        # Fill the template in a staging directory so the fill function won't modify
        # any items already in the target
        with tempfile.TemporaryDirectory() as stage_dir:
            with Template(self.template_path) as template:
                shutil.copytree(template, stage_dir, dirs_exist_ok=True)
            fill(stage_dir)
            shutil.copytree(stage_dir, target, dirs_exist_ok=True)


ValueT = TypeVar("ValueT")


def create_literal_mapping(
    mapping: Mapping[str, ValueT], prefix: str = "{{", suffix: str = "}}"
) -> Mapping[str, ValueT]:
    """
    Return a copy of a mapping where all the keys have a prefix and suffix added
    to them.
    """
    return {f"{prefix}{key}{suffix}": value for key, value in mapping.items()}


def create_re_any(
    terms: Iterable[str], prefix: str = "{{", suffix: str = "}}"
) -> Pattern[str]:
    """
    Return a compiled regular expression that will match any of an iterable of terms.
    """
    j_ts = "|".join(
        sorted(re.escape(term.strip(prefix).strip(suffix)) for term in terms)
    )
    return re.compile(rf"{re.escape(prefix)}\s*({j_ts})\s*{re.escape(suffix)}")


def map_replace(
    src: str,
    substitutions: Mapping[str, str],
    terms_re: Optional[Pattern[str]] = None,
    prefix: str = "{{",
    suffix: str = "}}",
) -> Tuple[str, int]:
    """Use a mapping to replace keys with values in a str and return the new str."""
    if not substitutions:
        return (src, 0)
    if not terms_re:
        terms_re = create_re_any(substitutions.keys(), prefix, suffix)
    return terms_re.subn(
        lambda m_obj: substitutions[f"{prefix}{m_obj.group(1)}{suffix}"], src
    )


def map_rename(
    filepath: str,
    substitutions: Mapping[str, str],
    terms_re: Optional[Pattern[str]] = None,
    prefix: str = "{{",
    suffix: str = "}}",
) -> str:
    """
    Use a mapping to replace keys with values in a file name, rename the file and
    return the new file name.
    """
    basename = os.path.basename(filepath)
    new_basename, count = map_replace(basename, substitutions, terms_re, prefix, suffix)
    if count:
        new_filepath = os.path.join(os.path.dirname(filepath), new_basename)
        os.rename(filepath, new_filepath)
        return new_filepath
    return filepath


def tree_map_rename(
    src: str, substitutions: Mapping[str, str], terms: Pattern[str]
) -> None:
    """Rename files in a diretory tree using substitutions for placeholder in names."""
    for root, dirs, files in os.walk(src, topdown=False):
        for name in [*files, *dirs]:
            map_rename(os.path.join(root, name), substitutions, terms)


def tree_map_replace(
    src: str, substitutions: Mapping[str, str], terms: Pattern[str]
) -> None:
    """
    Fill in the template variables in files in a directory tree using substitutions.
    """
    for root, _, files in os.walk(src):
        for file in files:
            with open(os.path.join(root, file), "r+", encoding="utf-8") as fileptr:
                template_text = fileptr.read()
                rendered_text, count = map_replace(template_text, substitutions, terms)
                if count:
                    fileptr.seek(0)
                    fileptr.write(rendered_text)
                    fileptr.truncate()
