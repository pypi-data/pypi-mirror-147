"""Parse and validate command line arguments."""

import argparse
from collections.abc import Iterable, Mapping
import os
from typing import Optional, Tuple, TypedDict

from skelly import __version__


class Args(TypedDict):
    """Args type."""

    builder: str
    builder_opts: Mapping[str, str]
    template_path: Optional[str]
    template_vars: Mapping[str, str]
    name: str
    branch: str
    no_git: bool
    silent: bool
    target: str


def parse_args() -> Args:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        "skelly", formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-B",
        "--builder",
        default="default",
        help="registered builder that will create the project (default: default)",
    )
    parser.add_argument(
        "-b",
        "--builder-opt",
        action="append",
        nargs=2,
        help="builder option and value; can be specified multiple times, e.g.,\n"
        + "    -o env_dir '.venv310' -o req_file 'requirements.txt'",
        metavar=("OPTION", "VALUE"),
    )
    parser.add_argument(
        "-T", "--template-path", help="project template (default: builder template)"
    )
    parser.add_argument(
        "-t",
        "--template-var",
        action="append",
        nargs=2,
        help="template variable and value; can be specified multiple times, e.g.,\n"
        + "    -t author 'Charlotte Jane' -t email 'cjs@example.com'",
        metavar=("VARIABLE", "VALUE"),
    )
    parser.add_argument(
        "-n", "--name", help="project name (default: derived from target)"
    )
    parser.add_argument(
        "-g",
        "--git",
        default="main",
        help="target repo's main branch (default: main)",
        metavar=("BRANCH"),
    )
    parser.add_argument(
        "-G", "--no-git", action="store_true", help="don't create a repo in target"
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="don't prompt for missing template variables",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"skelly {__version__}"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="project directory (default: current directory)",
    )

    args = parser.parse_args()
    target = os.path.abspath(args.target)
    name = args.name if args.name else os.path.basename(target)
    if args.template_var:
        template_vars = {pair[0]: pair[1] for pair in args.template_var}
    else:
        template_vars = {}
    if args.builder_opt:
        builder_opts = {pair[0]: pair[1] for pair in args.builder_opt}
    else:
        builder_opts = {}

    return {
        "builder": args.builder,
        "builder_opts": builder_opts,
        "template_path": args.template_path,
        "template_vars": template_vars,
        "name": name,
        "branch": args.git,
        "no_git": args.no_git,
        "silent": args.silent,
        "target": target,
    }


PromptSpec = Iterable[Tuple[Optional[str], str, Optional[str]]]


def prompt_args(spec: PromptSpec) -> Mapping[str, str]:
    """Prompt for args with defaults."""
    args = {
        name: input(f"{prompt if prompt else name}: ").strip() or default
        for prompt, name, default in spec
    }
    return {name: value for name, value in args.items() if value}
