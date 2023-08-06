"""Parse and validate command line arguments."""

import argparse
from collections.abc import Iterable, Mapping
import os
from typing import Optional, Tuple, TypedDict


class Args(TypedDict):
    """Args type."""

    silent: bool
    name: str
    template_path: Optional[str]
    template_vars: Mapping[str, str]
    builder_opts: Mapping[str, str]
    builder: str
    target: str


def parse_args() -> Args:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        "skelly", formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-b",
        "--builder",
        default="default",
        help="registered builder that will create the project (default: default)",
    )
    parser.add_argument(
        "-o",
        "--builder-opt",
        action="append",
        nargs=2,
        metavar=("OPTION", "VALUE"),
        help="builder option and value; can be specified multiple times, e.g.,\n"
        + "    -o env_dir '.venv310' -o req_file 'requirements.txt'",
    )
    parser.add_argument(
        "-n", "--name", help="project name (default: derived from target)"
    )
    parser.add_argument(
        "-p", "--template-path", help="project template (default: builder template)"
    )
    parser.add_argument(
        "-t",
        "--template-var",
        action="append",
        nargs=2,
        metavar=("VARIABLE", "VALUE"),
        help="template variable and value; can be specified multiple times, e.g.,\n"
        + "    -t author 'Charlotte Jane' -t email 'cjs@example.com'",
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="don't prompt for missing template variables",
    )
    parser.add_argument("-v", "--version", action="version", version="skelly 0.0.1")
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
        "silent": args.silent,
        "name": name,
        "template_path": args.template_path,
        "template_vars": template_vars,
        "builder_opts": builder_opts,
        "builder": args.builder,
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
