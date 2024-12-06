import argparse
from typing import Any

from ._loader import Loader
from ._models import Operation


def run(
    path: str,
    manifest: str,
    handle: str | None,
) -> Any:
    """
    Verse Run
    """
    loader = Loader(path=path, manifest=manifest, handle=handle)
    root_component = loader.load_root()
    operation = Operation(
        name="run",
        args=dict(path=path, manifest=manifest, root=handle),
    )
    return root_component.run(operation=operation)


def requirements(
    path: str,
    manifest: str,
    root: str | None,
    out: str | None,
):
    """
    Verse Requirements
    """
    loader = Loader(path=path, manifest=manifest, handle=root)
    requirements = loader.generate_requirements(out=out)
    return requirements


def main():
    parser = argparse.ArgumentParser(prog="verse", description="Verse CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Run the Verse application")
    requirements_parser = subparsers.add_parser(
        "requirements", help="Generate the pip requirements"
    )
    run_parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Project directory",
    )
    run_parser.add_argument(
        "--manifest",
        type=str,
        default=Loader.MANIFEST_FILE,
        help="Manifest filename",
    )
    run_parser.add_argument(
        "--handle",
        type=str,
        default=None,
        help="Root handle",
    )

    requirements_parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Project directory",
    )
    requirements_parser.add_argument(
        "--manifest",
        type=str,
        default=Loader.MANIFEST_FILE,
        help="Manifest filename",
    )
    requirements_parser.add_argument(
        "--handle",
        type=str,
        default=None,
        help="Root handle",
    )
    requirements_parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output path",
    )

    args = parser.parse_args()
    if args.command == "run":
        run(
            path=args.path,
            manifest=args.manifest,
            handle=args.handle,
        )
    elif args.command == "requirements":
        requirements(
            path=args.path,
            manifest=args.manifest,
            root=args.handle,
            out=args.out,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
