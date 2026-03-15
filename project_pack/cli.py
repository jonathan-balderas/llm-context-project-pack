from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from scripts import build_project_pack, validate_context


def _cmd_build(args: argparse.Namespace) -> int:
    return build_project_pack.main(
        ["--root", args.root, "--out", args.out]
    )


def _cmd_validate(args: argparse.Namespace) -> int:
    return validate_context.main(
        ["--root", args.root]
    )


def _cmd_check_sample(args: argparse.Namespace) -> int:
    root = Path(args.root)

    if not root.exists():
        print(f"ERROR: Context root not found: {root}")
        return 2

    print(f"[1/2] Validating sample context at {root}...")
    rc = validate_context.main(["--root", str(root)])
    if rc != 0:
        return rc

    if args.out:
        out = Path(args.out)
        print(f"[2/2] Building sample pack to {out}...")
        rc = build_project_pack.main(["--root", str(root), "--out", str(out)])
        if rc == 0:
            print(f"Sample check OK. Built archive: {out}")
        return rc

    with tempfile.TemporaryDirectory() as tmpdir:
        out = Path(tmpdir) / "Project_Pack.zip"
        print(f"[2/2] Building temporary sample pack to {out}...")
        rc = build_project_pack.main(["--root", str(root), "--out", str(out)])
        if rc == 0:
            print("Sample check OK.")
        return rc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="project-pack",
        description="CLI for Project Pack build and validation workflows.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser(
        "build",
        help="Build a Project Pack ZIP from a Context/ folder.",
    )
    build_parser.add_argument(
        "--root",
        default="Context",
        help="Context root folder (default: Context)",
    )
    build_parser.add_argument(
        "--out",
        default="Project_Pack.zip",
        help="Output ZIP filename (default: Project_Pack.zip)",
    )
    build_parser.set_defaults(func=_cmd_build)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate a Context/ folder.",
    )
    validate_parser.add_argument(
        "--root",
        default="Context",
        help="Context root folder (default: Context)",
    )
    validate_parser.set_defaults(func=_cmd_validate)

    check_sample_parser = subparsers.add_parser(
        "check-sample",
        help="Validate the sample Context/ folder and build a sample ZIP.",
    )
    check_sample_parser.add_argument(
        "--root",
        default="Context",
        help="Context root folder (default: Context)",
    )
    check_sample_parser.add_argument(
        "--out",
        help="Optional output ZIP path. If omitted, builds to a temporary file.",
    )
    check_sample_parser.set_defaults(func=_cmd_check_sample)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())