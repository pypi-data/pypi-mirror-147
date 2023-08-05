"""ideas makes it easy to experiment to experiment
with alternatives to Python's syntax.

If no source is given, ideas will start an interactive console.
"""

import argparse
from importlib import import_module
import sys

import ideas
from ideas import console
from ideas.session import config


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=__doc__,
)

parser.add_argument(
    "--version",
    help="Only displays the current version.",
    action="store_true",
)


parser.add_argument(
    "-t",
    "--transform",
    nargs=1,
    help="""Transformations to apply. Currently, only transformations found in
    ideas.examples are allowed. You do not need to include the 'ideas.examples'
    prefix.""",
)

parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="""Shows the transformed code before it is executed.""",
)

parser.add_argument(
    "source",
    nargs="?",
    help="""Name of the main Python module (path.to.my_program) to be imported.
    """,
)


def add_transform(transform):
    path = f"ideas.examples.{transform}"
    try:
        module = import_module(path)
    except ImportError:
        print(f"{path} is not a known transformer.")
    else:
        getattr(module, "add_hook")()


def main() -> None:
    args = parser.parse_args()
    if args.version:  # pragma: no cover
        print(f"\nideas version {ideas.__version__}")
        sys.exit()

    config.show_transformed = bool(args.verbose)

    if args.transform:
        for item in args.transform:
            add_transform(item)

    if args.source is not None:
        if args.source.endswith(".py"):
            args.source = args.source[:-3]
        module = import_module(args.source)
        if sys.flags.interactive:  # pragma: no cover
            console.start(locals=module.__dict__, prompt=">>> ")
    else:
        console.start(prompt=">>> ")


main()
