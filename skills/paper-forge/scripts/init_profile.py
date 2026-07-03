#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.profile import create_profile_if_missing, template_path  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Initialize the Paper Forge persistent Profile template without overwriting an existing Profile."
    )
    parser.add_argument("--profile-path", type=Path, default=None, help="Override target Profile path.")
    parser.add_argument("--template", type=Path, default=None, help="Override source Profile template path.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created without writing files.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source_template = args.template or template_path()
    result = create_profile_if_missing(args.profile_path, source_template, args.dry_run)

    print(f"Paper Forge Profile target: {result.target}")
    print(f"Profile template source: {source_template}")

    if result.existed:
        print("Profile already exists. No changes were made.")
        print("Next step: review or edit the existing Profile manually if needed.")
        return 0

    if result.dry_run:
        print("Dry run: Profile template would be created. No files were written.")
    else:
        print("Created Profile template.")

    print("Next step: edit the Profile with research directions, target applications, judging constraints, and language preference.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

