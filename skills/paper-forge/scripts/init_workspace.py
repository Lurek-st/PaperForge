#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.paths import asset_path, default_workspace_root  # noqa: E402
from lib.slug import dated_slug  # noqa: E402


TEMPLATES = {
    "README_FOR_READING.md": "reading-guide-template.md",
    "source/source_manifest.md": "source-manifest-template.md",
    "analysis/01_triage.md": "triage-template.md",
    "analysis/02_claim_ledger.md": "claim-ledger-template.md",
    "analysis/03_contribution_map.md": "contribution-map-template.md",
    "analysis/04_mechanism.md": "mechanism-template.md",
    "analysis/05_evidence_audit.md": "evidence-audit-template.md",
    "analysis/06_transfer_analysis.md": "transfer-analysis-template.md",
    "analysis/07_final_brief.md": "final-brief-template.md",
    "learning/08_recall_log.md": "recall-log-template.md",
}


BASE_OUTPUTS = ["README_FOR_READING.md"]
SCREEN_OUTPUTS = [*BASE_OUTPUTS, "source/source_manifest.md", "analysis/01_triage.md"]
DEEP_OUTPUTS = [
    *BASE_OUTPUTS,
    "source/source_manifest.md",
    "analysis/profile_snapshot.md",
    "analysis/01_triage.md",
    "analysis/02_claim_ledger.md",
    "analysis/03_contribution_map.md",
    "analysis/04_mechanism.md",
    "analysis/05_evidence_audit.md",
    "analysis/06_transfer_analysis.md",
    "analysis/07_final_brief.md",
]
RECALL_OUTPUTS = [*DEEP_OUTPUTS, "learning/08_recall_log.md"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize a Paper Forge local paper workspace.")
    parser.add_argument("source", nargs="?", default="", help="Paper source path, URL, DOI, or arXiv identifier.")
    parser.add_argument("--title", default="", help="Paper title used to generate the workspace slug.")
    parser.add_argument("--workspace-root", type=Path, default=None, help="Root directory for generated paper workspaces.")
    parser.add_argument("--workspace", type=Path, default=None, help="Explicit workspace path to initialize.")
    parser.add_argument("--mode", choices=["screen", "deep", "recall"], default="deep", help="Output set to initialize.")
    parser.add_argument("--dry-run", action="store_true", help="Show planned changes without writing files.")
    return parser


def infer_title(source: str) -> str:
    if not source:
        return "untitled-paper"
    candidate = source.rstrip("/").split("/")[-1]
    if candidate.lower().endswith(".pdf"):
        candidate = candidate[:-4]
    return candidate or "untitled-paper"


def desired_outputs(mode: str) -> list[str]:
    if mode == "screen":
        return SCREEN_OUTPUTS
    if mode == "recall":
        return RECALL_OUTPUTS
    return DEEP_OUTPUTS


def write_if_missing(path: Path, content: str, dry_run: bool) -> str:
    if path.exists():
        return f"skip existing {path}"
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return f"create {path}"


def profile_snapshot_template() -> str:
    return (
        "# Profile Snapshot\n\n"
        "## Snapshot Source\n\n"
        "- Source profile path: Unknown\n"
        "- Snapshot purpose: reproducible relevance and transfer analysis\n\n"
        "## Analysis-Relevant Profile Content\n\n"
        "No Profile was available when this workspace was initialized.\n"
    )


def load_template(relative_output: str, source: str) -> str:
    if relative_output == "analysis/profile_snapshot.md":
        return profile_snapshot_template()
    template_name = TEMPLATES[relative_output]
    text = asset_path(template_name).read_text(encoding="utf-8")
    if relative_output == "source/source_manifest.md" and source:
        text = text.replace("- Source path or URL: Unknown", f"- Source path or URL: {source}")
    return text


def run_state_content(mode: str, slug: str, source: str) -> str:
    data = {
        "schema_version": 1,
        "mode": mode,
        "paper_slug": slug,
        "source_input": source,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "initialized",
        "completed_outputs": [],
        "recall_started": mode == "recall",
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def numbered_outputs_for_mode(mode: str) -> list[str]:
    files = ["analysis/01_triage.md"]
    if mode in {"deep", "recall"}:
        files.extend(
            [
                "analysis/02_claim_ledger.md",
                "analysis/03_contribution_map.md",
                "analysis/04_mechanism.md",
                "analysis/05_evidence_audit.md",
                "analysis/06_transfer_analysis.md",
                "analysis/07_final_brief.md",
            ]
        )
    if mode == "recall":
        files.append("learning/08_recall_log.md")
    return files


def print_reading_guidance(workspace: Path, mode: str) -> None:
    print("")
    print("Reading guide:")
    print(f"- Workspace entry point: {workspace / 'README_FOR_READING.md'}")
    print("- Paper Forge outputs are Markdown reading artifacts, not a web UI.")
    print("- Open the numbered Markdown files with VS Code, Codex file view, Obsidian, Typora, or any Markdown reader.")
    print("- Primary files to read:")
    for relative in numbered_outputs_for_mode(mode):
        print(f"  - {relative}")
    print("- Non-numbered files are mainly for source tracking, Profile snapshots, and run state.")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    title = args.title or infer_title(args.source)
    slug = dated_slug(title)
    workspace = args.workspace or (args.workspace_root or default_workspace_root()) / slug

    planned: list[str] = []
    for directory in ["source", "analysis", "learning"]:
        path = workspace / directory
        if path.exists():
            planned.append(f"skip existing {path}")
        else:
            if not args.dry_run:
                path.mkdir(parents=True, exist_ok=True)
            planned.append(f"create {path}")

    for output in desired_outputs(args.mode):
        content = load_template(output, args.source)
        planned.append(write_if_missing(workspace / output, content, args.dry_run))

    planned.append(write_if_missing(workspace / "run_state.json", run_state_content(args.mode, slug, args.source), args.dry_run))

    print(f"Paper Forge workspace: {workspace}")
    print(f"Mode: {args.mode}")
    if args.dry_run:
        print("Dry run: no files were written.")
    for item in planned:
        print(item)
    print_reading_guidance(workspace, args.mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
