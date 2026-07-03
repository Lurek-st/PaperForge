#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.validation import validate_workspace  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Structurally validate a Paper Forge paper workspace.")
    parser.add_argument("workspace", type=Path, help="Paper workspace path.")
    parser.add_argument("--mode", choices=["screen", "deep"], default="deep", help="Validation scope.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable validation output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = validate_workspace(args.workspace, mode=args.mode)

    if args.json:
        print(
            json.dumps(
                {
                    "workspace": str(result.workspace),
                    "passed": result.passed,
                    "errors": result.errors,
                    "warnings": result.warnings,
                    "semantic_accuracy": "not automatically verified",
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        if result.passed:
            print("Structural validation passed")
        else:
            print("Structural validation failed")
            for error in result.errors:
                print(f"- {error}")
        print("Semantic accuracy not automatically verified")
        for warning in result.warnings:
            if warning != "Semantic accuracy not automatically verified":
                print(f"Warning: {warning}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
