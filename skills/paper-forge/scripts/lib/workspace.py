from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import configured_path
from .ids import derive_identity, folder_name
from .language import resolve_language_settings
from .obsidian import metadata_hash, sha256_file
from .paths import asset_path, default_profile_path
from .text import safe_unicode_text


ANALYSIS_TEMPLATES = {
    "README_FOR_READING.md": "reading-guide-template.md",
    "analysis/01_triage.md": "triage-template.md",
    "analysis/02_claim_ledger.md": "claim-ledger-template.md",
    "analysis/03_contribution_map.md": "contribution-map-template.md",
    "analysis/04_mechanism.md": "mechanism-template.md",
    "analysis/05_evidence_audit.md": "evidence-audit-template.md",
    "analysis/06_transfer_analysis.md": "transfer-analysis-template.md",
    "analysis/07_final_brief.md": "final-brief-template.md",
    "learning/08_recall_log.md": "recall-log-template.md",
}

BASE_ANALYSIS_OUTPUTS = ["README_FOR_READING.md"]
SCREEN_ANALYSIS_OUTPUTS = [*BASE_ANALYSIS_OUTPUTS, "source/source_manifest.md", "analysis/profile_snapshot.md", "analysis/01_triage.md"]
DEEP_ANALYSIS_OUTPUTS = [
    *BASE_ANALYSIS_OUTPUTS,
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
RECALL_ANALYSIS_OUTPUTS = [*DEEP_ANALYSIS_OUTPUTS, "learning/08_recall_log.md"]


@dataclass
class PackageResult:
    package_dir: Path
    paper_id: str
    created: bool
    pdf_status: str
    planned: list[str] = field(default_factory=list)


@dataclass
class AnalysisWorkspaceResult:
    workspace_dir: Path
    paper_id: str
    mode: str
    created: bool
    status: str
    planned: list[str] = field(default_factory=list)
    skipped_existing: list[str] = field(default_factory=list)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def workspace_dirs(config: dict[str, Any]) -> list[Path]:
    return [
        configured_path(config, "workspace", key)
        for key in ["inbox", "processing", "cache", "failed", "archive", "logs"]
    ]


def ensure_workspace_dirs(config: dict[str, Any], *, dry_run: bool = False) -> list[str]:
    planned: list[str] = []
    for directory in workspace_dirs(config):
        if directory.exists():
            planned.append(f"skip existing {directory}")
        else:
            if not dry_run:
                directory.mkdir(parents=True, exist_ok=True)
            planned.append(f"create {directory}")
    return planned


def find_package_by_paper_id(config: dict[str, Any], paper_id: str) -> Path | None:
    for area in ["inbox", "processing", "archive", "failed"]:
        root = configured_path(config, "workspace", area)
        if not root.exists():
            continue
        for manifest in root.glob("*/manifest.json"):
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if data.get("paper_id") == paper_id:
                return manifest.parent
    return None


def find_analysis_workspace_by_paper_id(config: dict[str, Any], paper_id: str) -> Path | None:
    root = configured_path(config, "workspace", "processing")
    if not root.exists():
        return None
    for manifest_path in root.glob("*/paperforge-workspace-manifest.json"):
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("paper_id") == paper_id:
            return manifest_path.parent
    for state_path in root.glob("*/run_state.json"):
        try:
            data = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("paper_id") == paper_id:
            return state_path.parent
    return None


def create_work_package(
    metadata: dict[str, Any],
    config: dict[str, Any],
    *,
    pdf_path: Path | None = None,
    dry_run: bool = False,
    force: bool = False,
) -> PackageResult:
    identity = derive_identity(metadata)
    existing = find_package_by_paper_id(config, identity.paper_id)
    pattern = config["naming"]["folder_pattern"]
    max_title = int(config["naming"]["max_short_title_length"])
    package_dir = existing or configured_path(config, "workspace", "inbox") / folder_name(
        metadata,
        pattern=pattern,
        max_short_title_length=max_title,
    )
    created = existing is None and not package_dir.exists()
    result = PackageResult(
        package_dir=package_dir,
        paper_id=identity.paper_id,
        created=created,
        pdf_status="available" if pdf_path and pdf_path.exists() else "missing",
    )

    for directory in [package_dir]:
        if directory.exists():
            result.planned.append(f"skip existing {directory}")
        else:
            result.planned.append(f"create {directory}")
            if not dry_run:
                directory.mkdir(parents=True, exist_ok=True)

    source_pdf = package_dir / "source.pdf"
    if pdf_path and pdf_path.exists():
        if source_pdf.exists() and not force:
            result.planned.append(f"skip existing {source_pdf}")
        elif not dry_run:
            shutil.copy2(pdf_path, source_pdf)
            result.planned.append(f"copy {pdf_path} -> {source_pdf}")
    elif not pdf_path:
        result.planned.append("pdf missing: metadata-only package")
    else:
        result.planned.append(f"pdf missing: {pdf_path}")

    metadata_path = package_dir / "metadata.json"
    if metadata_path.exists() and not force:
        result.planned.append(f"skip existing {metadata_path}")
    elif not dry_run:
        metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result.planned.append(f"write {metadata_path}")

    manifest_path = package_dir / "manifest.json"
    manifest = {
        "paper_id": identity.paper_id,
        "id_strategy": identity.id_strategy,
        "zotero_item_key": identity.zotero_item_key,
        "folder_name": package_dir.name,
        "source_pdf_hash": sha256_file(source_pdf if source_pdf.exists() else pdf_path),
        "metadata_hash": metadata_hash(metadata),
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "status": "metadata_ready" if result.pdf_status == "missing" else "pdf_ready",
        "pdf_status": result.pdf_status,
    }
    if not dry_run:
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result.planned.append(f"write {manifest_path}")
    else:
        result.planned.append(f"write {manifest_path}")

    return result


def load_package(package_dir: Path) -> tuple[dict[str, Any], Path | None]:
    metadata_path = package_dir / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    source_pdf = package_dir / "source.pdf"
    return metadata, source_pdf if source_pdf.exists() else None


def load_analysis_workspace_metadata(workspace_dir: Path) -> tuple[dict[str, Any], Path | None, Path | None]:
    metadata_path = workspace_dir / "source" / "metadata.json"
    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing analysis workspace metadata: {metadata_path}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    package_dir: Path | None = None
    manifest_path = workspace_dir / "paperforge-workspace-manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            manifest = {}
        package_text = manifest.get("work_package") or ""
        if package_text:
            package_dir = Path(str(package_text))
    source_pdf = None
    if package_dir:
        candidate = package_dir / "source.pdf"
        if candidate.exists():
            source_pdf = candidate
    return metadata, source_pdf, package_dir


def update_analysis_workspace_status(workspace_dir: Path, *, status: str, semantic_analysis_complete: bool) -> None:
    manifest_path = workspace_dir / "paperforge-workspace-manifest.json"
    manifest: dict[str, Any] = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            manifest = {}
    manifest["status"] = status
    manifest["semantic_analysis_complete"] = semantic_analysis_complete
    manifest["updated_at"] = utc_now()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def desired_analysis_outputs(mode: str) -> list[str]:
    if mode == "screen":
        return SCREEN_ANALYSIS_OUTPUTS
    if mode == "recall":
        return RECALL_ANALYSIS_OUTPUTS
    return DEEP_ANALYSIS_OUTPUTS


def _authors(metadata: dict[str, Any]) -> list[str]:
    authors = metadata.get("authors") or metadata.get("creators") or []
    if isinstance(authors, str):
        return [safe_unicode_text(authors)]
    names: list[str] = []
    for author in authors:
        if isinstance(author, str):
            names.append(safe_unicode_text(author))
        elif isinstance(author, dict):
            name = author.get("name") or " ".join(
                safe_unicode_text(part) for part in [author.get("firstName"), author.get("lastName")] if part
            )
            if name:
                names.append(safe_unicode_text(name))
    return names


def source_manifest_content(metadata: dict[str, Any], package_dir: Path | None, source_pdf: Path | None) -> str:
    identity = derive_identity(metadata)
    title = safe_unicode_text(metadata.get("title") or "Untitled Paper")
    pdf_status = "available" if source_pdf and source_pdf.exists() else "missing"
    source_path = source_pdf.as_posix() if source_pdf else "Unknown"
    package_path = package_dir.as_posix() if package_dir else "Manual metadata input"
    authors = ", ".join(_authors(metadata)) or "Unknown"
    warnings = metadata.get("paperforge_warnings") or []
    warning_block = ""
    if warnings:
        warning_lines = "\n".join(f"- {safe_unicode_text(warning)}" for warning in warnings)
        warning_block = f"\n## Metadata Warnings\n\n{warning_lines}\n"
    return f"""# Source Manifest

## Paper Metadata

- Paper ID: `{identity.paper_id}`
- ID strategy: `{identity.id_strategy}`
- Zotero item key: `{identity.zotero_item_key or 'Unknown'}`
- Title: {title}
- Authors: {authors}
- Year: {metadata.get('year') or 'Unknown'}
- Venue: {safe_unicode_text(metadata.get('venue') or metadata.get('publicationTitle') or metadata.get('conferenceName') or 'Unknown')}
- DOI: {safe_unicode_text(metadata.get('doi') or metadata.get('DOI') or 'Unknown')}
- arXiv ID: {safe_unicode_text(metadata.get('arxiv_id') or metadata.get('arXiv') or 'Unknown')}
- Source URL: {safe_unicode_text(metadata.get('source_url') or metadata.get('url') or 'Unknown')}

## Local Source Basis

- PaperForge work package: {package_path}
- Workspace PDF path: {source_path}
- PDF status: {pdf_status}
- Source locator status: Unknown until a human/Codex deep pass fills page, section, figure, table, or URL locators.

## Safety Boundary

- Zotero remains the source of truth for the original PDF and standard metadata.
- PaperForge must not move, rename, delete, or write Zotero `storage/` or `zotero.sqlite`.
- This workspace is the PaperForge analysis workspace. It is safe for PaperForge to read and write here.

## Analysis Status

This file is a deterministic source manifest. It does not prove that semantic paper analysis is complete.

## Analysis Limitations

- Semantic accuracy is not automatically verified.
- Source locators must be filled during the PaperForge deep pass.
{warning_block}
"""


def profile_snapshot_content() -> str:
    profile_path = default_profile_path()
    if profile_path.exists():
        profile_text = profile_path.read_text(encoding="utf-8")
        return f"""# Profile Snapshot

## Snapshot Source

- Source profile path: {profile_path}
- Snapshot purpose: reproducible relevance and transfer analysis
- Snapshot created at: {utc_now()}

## Analysis-Relevant Profile Content

{profile_text}
"""
    return f"""# Profile Snapshot

## Snapshot Source

- Source profile path: {profile_path}
- Snapshot purpose: reproducible relevance and transfer analysis
- Snapshot created at: {utc_now()}

## Analysis-Relevant Profile Content

No persistent Profile was found. Transfer analysis must mark Profile-dependent judgments as Unknown or low-confidence.
"""


def run_state_content(
    mode: str,
    workspace_dir: Path,
    metadata: dict[str, Any],
    package_dir: Path | None,
    language_settings: dict[str, str],
) -> str:
    identity = derive_identity(metadata)
    data = {
        "schema_version": 1,
        "mode": mode,
        "paper_id": identity.paper_id,
        "id_strategy": identity.id_strategy,
        "zotero_item_key": identity.zotero_item_key,
        "workspace": workspace_dir.as_posix(),
        "work_package": package_dir.as_posix() if package_dir else "",
        "created_at": utc_now(),
        "status": "initialized",
        "completed_outputs": [],
        "recall_started": mode == "recall",
        "requested_output_language": language_settings["analysis_language_requested"],
        "resolved_output_language": language_settings["analysis_language"],
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def analysis_workspace_manifest(
    mode: str,
    workspace_dir: Path,
    metadata: dict[str, Any],
    package_dir: Path | None,
    source_pdf: Path | None,
    language_settings: dict[str, str],
) -> str:
    identity = derive_identity(metadata)
    data = {
        "schema_version": 1,
        "paper_id": identity.paper_id,
        "id_strategy": identity.id_strategy,
        "zotero_item_key": identity.zotero_item_key,
        "mode": mode,
        "workspace": workspace_dir.as_posix(),
        "work_package": package_dir.as_posix() if package_dir else "",
        "source_pdf_hash": sha256_file(source_pdf),
        "metadata_hash": metadata_hash(metadata),
        "status": "analysis_workspace_ready",
        "created_or_updated_at": utc_now(),
        "semantic_analysis_complete": False,
        "requested_output_language": language_settings["analysis_language_requested"],
        "resolved_output_language": language_settings["analysis_language"],
        "obsidian_note_language": language_settings["obsidian_note_language"],
        "next_step": "Use the PaperForge Skill in Codex to fill analysis/*.md, then run export-obsidian.",
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def load_analysis_template(
    relative_output: str,
    metadata: dict[str, Any],
    package_dir: Path | None,
    source_pdf: Path | None,
    language_settings: dict[str, str],
) -> str:
    if relative_output == "source/source_manifest.md":
        return source_manifest_content(metadata, package_dir, source_pdf)
    if relative_output == "analysis/profile_snapshot.md":
        return profile_snapshot_content()
    template_name = ANALYSIS_TEMPLATES[relative_output]
    text = asset_path(template_name).read_text(encoding="utf-8")
    if relative_output == "README_FOR_READING.md":
        title = metadata.get("title") or "Untitled Paper"
        text = text.replace("# Paper Forge Reading Guide", f"# Paper Forge Reading Guide: {title}")
        text += (
            "\n## Requested Output Language\n\n"
            f"- Requested mode: `{language_settings['analysis_language_requested']}`\n"
            f"- Resolved mode for this workspace: `{language_settings['analysis_language']}`\n"
            f"- Requested Obsidian note language: `{language_settings['obsidian_note_language']}`\n"
            "- The deep semantic analysis is still filled by Codex / Agent; this file only records the selected output preference.\n"
        )
    return text


def write_workspace_file(
    path: Path,
    content: str,
    result: AnalysisWorkspaceResult,
    *,
    dry_run: bool,
    force: bool,
) -> None:
    if path.exists() and not force:
        result.skipped_existing.append(path.as_posix())
        result.planned.append(f"skip existing {path}")
        return
    if dry_run:
        result.planned.append(f"write {path}")
        return
    if path.exists() and force:
        backup_dir = path.parent / ".paperforge-backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup = backup_dir / f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{path.name}.bak"
        shutil.copy2(path, backup)
        result.planned.append(f"backup {backup}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    result.planned.append(f"write {path}")


def create_analysis_workspace(
    metadata: dict[str, Any],
    config: dict[str, Any],
    *,
    package_dir: Path | None = None,
    source_pdf: Path | None = None,
    mode: str = "deep",
    dry_run: bool = False,
    force: bool = False,
) -> AnalysisWorkspaceResult:
    if mode not in {"screen", "deep", "recall"}:
        raise ValueError(f"Unsupported PaperForge mode: {mode}")
    identity = derive_identity(metadata)
    existing = find_analysis_workspace_by_paper_id(config, identity.paper_id)
    if existing:
        workspace_dir = existing
    elif package_dir:
        workspace_dir = configured_path(config, "workspace", "processing") / package_dir.name
    else:
        pattern = config["naming"]["folder_pattern"]
        max_title = int(config["naming"]["max_short_title_length"])
        workspace_dir = configured_path(config, "workspace", "processing") / folder_name(
            metadata,
            pattern=pattern,
            max_short_title_length=max_title,
        )
    result = AnalysisWorkspaceResult(
        workspace_dir=workspace_dir,
        paper_id=identity.paper_id,
        mode=mode,
        created=not workspace_dir.exists(),
        status="analysis_workspace_ready",
    )
    language_settings = metadata.get("paperforge_language_settings") or resolve_language_settings(config)

    for directory in ["source", "analysis", "learning"]:
        path = workspace_dir / directory
        if path.exists():
            result.planned.append(f"skip existing {path}")
        else:
            result.planned.append(f"create {path}")
            if not dry_run:
                path.mkdir(parents=True, exist_ok=True)

    for relative in desired_analysis_outputs(mode):
        content = load_analysis_template(relative, metadata, package_dir, source_pdf, language_settings)
        write_workspace_file(workspace_dir / relative, content, result, dry_run=dry_run, force=force)

    metadata_content = json.dumps(metadata, indent=2, ensure_ascii=False) + "\n"
    write_workspace_file(workspace_dir / "source" / "metadata.json", metadata_content, result, dry_run=dry_run, force=force)
    write_workspace_file(
        workspace_dir / "run_state.json",
        run_state_content(mode, workspace_dir, metadata, package_dir, language_settings),
        result,
        dry_run=dry_run,
        force=force,
    )

    manifest_path = workspace_dir / "paperforge-workspace-manifest.json"
    manifest = analysis_workspace_manifest(mode, workspace_dir, metadata, package_dir, source_pdf, language_settings)
    if dry_run:
        result.planned.append(f"write {manifest_path}")
    else:
        manifest_path.write_text(manifest, encoding="utf-8")
        result.planned.append(f"write {manifest_path}")

    return result
