"""Stub out a Python package."""

from collections.abc import Mapping
from importlib.metadata import entry_points, EntryPoint
import sys
from typing import Optional

from .args import Args, parse_args
from .builder.builder import Builder


def main(args: Optional[Args] = None) -> int:
    """Get the args and run the specified builder."""
    if not args:
        args = parse_args()

    group = entry_points().select(group="skelly.builders")  # type: ignore
    builders: Mapping[str, EntryPoint] = {ept.name: ept for ept in group}

    try:
        builder_class = builders[args["builder"]].load()
    except KeyError:
        print(
            f"builder '{args['builder']}' not registered"
            + f": registered builders: {', '.join(sorted(builders))}",
            file=sys.stderr,
        )
        return 1

    builder: Builder = builder_class(args)
    builder.build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
