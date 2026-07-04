from __future__ import annotations

import hashlib
import json
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import configured_path
from .ids import derive_identity, folder_name, import_date
from .language import NOTE_TITLE_CATALOG, UI_TEXT, resolve_language_settings
from .text import safe_unicode_text


ANALYSIS_VERSION = "paperforge-obsidian-core-chain-v4"

PAPER_DIRS = [
    "Attachments/figures",
    "Attachments/supplementary-materials",
    "Attachments/notes-from-video",
    "Attachments/my-diagrams",
]

NOTE_TITLES = NOTE_TITLE_CATALOG["en"]

READING_ORDER = ["01", "02", "03", "04", "05", "00"]
LEGACY_NOTE_NAMES = {f"{number}.md" for number in NOTE_TITLES}
TITLED_NOTE_RE = re.compile(r"^\d{2} - .+\.md$")


@dataclass
class ArchiveResult:
    paper_id: str
    archive_dir: Path
    folder_name: str
    created: bool
    status: str
    planned: list[str] = field(default_factory=list)
    skipped_existing: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stable_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256_file(path: Path | None) -> str:
    if not path or not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def metadata_hash(metadata: dict[str, Any]) -> str:
    return hashlib.sha256(stable_json(metadata).encode("utf-8")).hexdigest()


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def yaml_list(values: Any) -> list[str]:
    if not values:
        return []
    if isinstance(values, str):
        return [values]
    result: list[str] = []
    for value in values:
        if isinstance(value, dict):
            name = value.get("name") or " ".join(
                safe_unicode_text(part) for part in [value.get("firstName"), value.get("lastName")] if part
            )
            if name:
                result.append(safe_unicode_text(name))
        else:
            result.append(safe_unicode_text(value))
    return result


def paper_title(metadata: dict[str, Any]) -> str:
    return safe_unicode_text(metadata.get("title") or "Untitled Paper")


def note_title(number: str, language_mode: str = "en") -> str:
    return NOTE_TITLE_CATALOG.get(language_mode, NOTE_TITLE_CATALOG["en"])[number]

def note_filename(number: str, language_mode: str = "en") -> str:
    return f"{number} - {note_title(number, language_mode)}.md"


def note_stem(number: str, language_mode: str = "en") -> str:
    return note_filename(number, language_mode).removesuffix(".md")


def note_heading(number: str, language_mode: str = "en") -> str:
    return note_stem(number, language_mode)


def note_relative_without_ext(number: str, language_mode: str = "en") -> str:
    return note_stem(number, language_mode)


def legacy_note_paths(archive_dir: Path) -> list[Path]:
    return [archive_dir / name for name in sorted(LEGACY_NOTE_NAMES)]


def has_legacy_numbered_notes(archive_dir: Path) -> bool:
    legacy_paths = legacy_note_paths(archive_dir)
    if not any(path.exists() for path in legacy_paths):
        return False
    return not any((archive_dir / note_filename(number)).exists() for number in NOTE_TITLES)


def existing_titled_note_paths(archive_dir: Path) -> list[Path]:
    return [path for path in archive_dir.glob("*.md") if TITLED_NOTE_RE.fullmatch(path.name)]


def pdf_status(metadata: dict[str, Any], source_pdf: Path | None) -> str:
    if source_pdf and source_pdf.exists():
        return "available"
    return str(metadata.get("pdf_status") or "missing")


def analysis_workspace_state(analysis_workspace: Path | None) -> str:
    if not analysis_workspace:
        return "missing"
    manifest_path = analysis_workspace / "paperforge-workspace-manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return "invalid_manifest"
        if manifest.get("semantic_analysis_complete") is True:
            return "deep_analysis_complete"
        return str(manifest.get("status") or "analysis_workspace_ready")
    state_path = analysis_workspace / "run_state.json"
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return "invalid_run_state"
        status = str(state.get("status") or "initialized")
        if status in {"completed", "deep_completed", "processed"}:
            return "deep_analysis_complete"
        return status
    return "untracked_workspace"


def status_for(metadata: dict[str, Any], source_pdf: Path | None, analysis_workspace: Path | None) -> str:
    if pdf_status(metadata, source_pdf) != "available":
        return "metadata_only"
    state = analysis_workspace_state(analysis_workspace)
    if state == "deep_analysis_complete":
        return "exported_from_deep_analysis"
    if state == "analysis_incomplete":
        return "analysis_incomplete"
    return "analysis_pending"


def source_warning(metadata: dict[str, Any], source_pdf: Path | None, analysis_workspace: Path | None) -> str:
    if pdf_status(metadata, source_pdf) != "available":
        return (
            "**Status:** metadata-only scaffold. PDF is unavailable, so PaperForge must not claim full-text "
            "experiment review, evidence review, or Feynman understanding."
        )
    state = analysis_workspace_state(analysis_workspace)
    if state == "deep_analysis_complete":
        return (
            "**Status:** exported from a completed PaperForge deep workspace. "
            "Still verify source locators before relying on claims."
        )
    if state == "analysis_incomplete":
        return (
            "**Status:** analysis incomplete. The core workspace exists, but required deep artifacts still look "
            "like placeholders or lack source-located evidence. Do not treat this as a completed paper assessment."
        )
    return (
        "**Status:** analysis workspace is prepared, but semantic deep analysis is not automatically complete. "
        "Fill the PaperForge core files with source-located analysis, then export again."
    )


def obsidian_link(vault_relative_without_ext: str, label: str) -> str:
    return f"[[{vault_relative_without_ext}|{label}]]"


def paper_link(folder: str, relative_without_ext: str, label: str) -> str:
    return obsidian_link(f"Papers/{folder}/{relative_without_ext}", label)


def note_link(folder: str, number: str, language_mode: str = "en", label: str | None = None) -> str:
    display = label or note_heading(number, language_mode)
    return paper_link(folder, note_relative_without_ext(number, language_mode), display)


def zotero_link_content(metadata: dict[str, Any]) -> str:
    title = paper_title(metadata)
    zotero_key = safe_unicode_text(metadata.get("zotero_item_key") or metadata.get("key") or "")
    if zotero_key:
        return f"""[Open this item in Zotero](zotero://select/library/items/{zotero_key})

- Zotero Item Key: `{zotero_key}`
- Title: {title}
"""
    return f"""No stable Zotero item key was available when this archive was created.

- Title: {title}
- Recovery hint: search Zotero by title, DOI, arXiv ID, or source URL.
"""


def source_links_content(metadata: dict[str, Any]) -> str:
    return f"""- DOI: {safe_unicode_text(metadata.get('doi') or metadata.get('DOI') or 'Unknown')}
- arXiv ID: {safe_unicode_text(metadata.get('arxiv_id') or metadata.get('arXiv') or 'Unknown')}
- Source URL: {safe_unicode_text(metadata.get('source_url') or metadata.get('url') or 'Unknown')}
- Zotero remains the source of truth for the managed PDF.
"""


def artifact_text(analysis_workspace: Path | None, relative: str) -> str:
    if not analysis_workspace:
        return ""
    path = analysis_workspace / relative
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def artifact_block(analysis_workspace: Path | None, relative: str, title: str) -> str:
    text = artifact_text(analysis_workspace, relative)
    if not text:
        return f"## {title}\n\nCore artifact `{relative}` is not available yet.\n"
    return f"## {title}\n\nImported from PaperForge core artifact: `{relative}`.\n\n{text}\n"


def scaffold_visible(analysis_workspace: Path | None) -> bool:
    return analysis_workspace_state(analysis_workspace) != "deep_analysis_complete"


def navigation_block(folder: str, current_number: str, language_mode: str) -> str:
    ui = UI_TEXT[language_mode]
    current_index = READING_ORDER.index(current_number)
    previous_number = READING_ORDER[current_index - 1] if current_index > 0 else None
    next_number = READING_ORDER[current_index + 1] if current_index + 1 < len(READING_ORDER) else None
    lines = [
        f"## {ui['navigation']}",
        "",
        f"- {ui['home']}: {paper_link(folder, folder, folder)}",
    ]
    if previous_number:
        lines.append(f"- {ui['previous']}: {note_link(folder, previous_number, language_mode)}")
    if next_number:
        lines.append(f"- {ui['next']}: {note_link(folder, next_number, language_mode)}")
    return "\n".join(lines)


def _generated_scaffold_should_refresh(path: Path, new_content: str) -> bool:
    try:
        existing = path.read_text(encoding="utf-8")
    except OSError:
        return False
    if existing == new_content:
        return False
    lowered = existing.lower()
    if "paperforge_generated: true" not in lowered:
        return False
    if "paperforge_user_extendable: true" in lowered:
        return False
    stale_status = (
        "**status:** analysis incomplete." in lowered
        or "**status:** analysis workspace is prepared" in lowered
    )
    stale_scaffold = "## scaffold to fill" in lowered and "## scaffold to fill" not in new_content.lower()
    return stale_status or stale_scaffold


def home_note_content(
    metadata: dict[str, Any],
    folder: str,
    source_pdf: Path | None,
    analysis_workspace: Path | None,
    language_mode: str = "en",
) -> str:
    title = paper_title(metadata)
    warning = source_warning(metadata, source_pdf, analysis_workspace)
    ui = UI_TEXT[language_mode]
    zotero_key = safe_unicode_text(metadata.get("zotero_item_key") or metadata.get("key") or "")
    zotero_link = (
        f"[Open in Zotero](zotero://select/library/items/{zotero_key})"
        if zotero_key
        else "Zotero item key unavailable. Search Zotero by title, DOI, or arXiv ID."
    )
    return f"""---
paperforge_generated: true
paper_folder: "Papers/{folder}"
analysis_version: "{ANALYSIS_VERSION}"
---
# {title}

{warning}

## {ui['recommended_reading_order']}

1. {note_link(folder, "01", language_mode)}
2. {note_link(folder, "02", language_mode)}
3. {note_link(folder, "03", language_mode)}
4. {note_link(folder, "04", language_mode)}
5. {note_link(folder, "05", language_mode)}
6. {note_link(folder, "00", language_mode)}

## {ui['quick_entry']}

- {ui['source_and_zotero']}: {note_link(folder, "00", language_mode)}
- {ui['problem_entry']}: {note_link(folder, "01", language_mode)}
- {ui['mechanism_entry']}: {note_link(folder, "02", language_mode)}
- {ui['claims_entry']}: {note_link(folder, "03", language_mode)}
- {ui['transfer_entry']}: {note_link(folder, "04", language_mode)}
- {ui['recall_entry']}: {note_link(folder, "05", language_mode)}

## {ui['zotero_source_item']}

{zotero_link}
"""


def source_note_content(
    metadata: dict[str, Any],
    folder: str,
    source_pdf: Path | None,
    config: dict[str, Any],
    analysis_workspace: Path | None,
    language_mode: str = "en",
) -> str:
    identity = derive_identity(metadata)
    authors = yaml_list(metadata.get("authors") or metadata.get("creators"))
    warnings = metadata.get("paperforge_warnings") or []
    lines = [
        "---",
        f"paper_id: {yaml_scalar(identity.paper_id)}",
        f"id_strategy: {yaml_scalar(identity.id_strategy)}",
        f"zotero_item_key: {yaml_scalar(identity.zotero_item_key)}",
        f"title: {yaml_scalar(paper_title(metadata))}",
    ]
    if authors:
        lines.append("authors:")
        lines.extend(f"  - {yaml_scalar(author)}" for author in authors)
    else:
        lines.append("authors: []")
    lines.extend(
        [
            f"year: {yaml_scalar(metadata.get('year'))}",
            f"venue: {yaml_scalar(safe_unicode_text(metadata.get('venue') or metadata.get('publicationTitle') or metadata.get('conferenceName') or ''))}",
            f"doi: {yaml_scalar(safe_unicode_text(metadata.get('doi') or metadata.get('DOI') or ''))}",
            f"arxiv_id: {yaml_scalar(safe_unicode_text(metadata.get('arxiv_id') or metadata.get('arXiv') or ''))}",
            f"source_url: {yaml_scalar(safe_unicode_text(metadata.get('source_url') or metadata.get('url') or ''))}",
            f"zotero_collection: {yaml_scalar(safe_unicode_text(metadata.get('zotero_collection') or config['zotero']['collection_name']))}",
            f"imported_at: {yaml_scalar(safe_unicode_text(metadata.get('imported_at') or import_date(metadata)))}",
            f"exported_at: {yaml_scalar(utc_now())}",
            f"paperforge_status: {yaml_scalar(status_for(metadata, source_pdf, analysis_workspace))}",
            f"analysis_workspace_status: {yaml_scalar(analysis_workspace_state(analysis_workspace))}",
            f"analysis_version: {yaml_scalar(ANALYSIS_VERSION)}",
            f"pdf_status: {yaml_scalar(pdf_status(metadata, source_pdf))}",
            f"paper_folder: {yaml_scalar('Papers/' + folder)}",
            "---",
            "",
            f"# {note_heading('00', language_mode)}",
            "",
            source_warning(metadata, source_pdf, analysis_workspace),
            "",
            navigation_block(folder, "00", language_mode),
            "",
            f"## {UI_TEXT[language_mode]['source_boundary']}",
            "",
            "- Zotero is the source of truth for original PDFs and standard bibliographic metadata.",
            "- PaperForge records a traceable analysis snapshot and must not modify Zotero `storage/` or `zotero.sqlite`.",
            "- Obsidian keeps the long-term Markdown research archive; it should not become a duplicate Zotero PDF library.",
            "",
            "## Zotero Link",
            "",
            zotero_link_content(metadata).strip(),
            "",
            f"## {UI_TEXT[language_mode]['source_links']}",
            "",
            source_links_content(metadata).strip(),
            "",
        ]
    )
    if analysis_workspace:
        lines.extend(
            [
                f"## {UI_TEXT[language_mode]['core_workspace']}",
                "",
                f"- Workspace: `{analysis_workspace.as_posix()}`",
                f"- Status: `{analysis_workspace_state(analysis_workspace)}`",
                "",
                artifact_block(analysis_workspace, "source/source_manifest.md", "Source Manifest").strip(),
                "",
                artifact_block(analysis_workspace, "analysis/profile_snapshot.md", "Profile Snapshot").strip(),
                "",
            ]
        )
    if warnings:
        lines.extend(
            [
                f"## {UI_TEXT[language_mode]['metadata_warnings']}",
                "",
                *[f"- {safe_unicode_text(warning)}" for warning in warnings],
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def problem_contribution_note_content(
    metadata: dict[str, Any],
    folder: str,
    source_pdf: Path | None,
    analysis_workspace: Path | None,
    language_mode: str = "en",
) -> str:
    scaffold = ""
    if scaffold_visible(analysis_workspace):
        scaffold = """
## Scaffold To Fill

### One-Sentence Conclusion

unknown_from_pdf_only. Source locator: paper_not_reported.

### Core Problem

unknown_from_pdf_only. Source locator: paper_not_reported.

### Why Prior Methods Were Insufficient

unknown_from_pdf_only. Source locator: paper_not_reported.

### Actual Intervention

not_verified_in_alpha. Source locator: unknown_from_pdf_only.

### Claimed Contributions

- not_verified_in_alpha. Source locator: unknown_from_pdf_only.

### Real Technical Increment After Removing Marketing Language

not_verified_in_alpha. Source locator: unknown_from_pdf_only.

### Information Gaps

- unavailable_without_repo_check. Source basis: repo, checkpoint, or dataset manifest not yet audited in this run.
"""
    return f"""---
paperforge_generated: true
---
# {note_heading('01', language_mode)}

{source_warning(metadata, source_pdf, analysis_workspace)}

## {UI_TEXT[language_mode]['reading_purpose']}

This note answers: What problem is this paper solving, why were prior approaches insufficient, and what did the authors actually change?

{navigation_block(folder, "01", language_mode)}

{scaffold}

{artifact_block(analysis_workspace, "analysis/01_triage.md", "Core Artifact: Triage")}

{artifact_block(analysis_workspace, "analysis/03_contribution_map.md", "Core Artifact: Contribution Map")}
"""


def mechanism_note_content(
    metadata: dict[str, Any],
    folder: str,
    source_pdf: Path | None,
    analysis_workspace: Path | None,
    language_mode: str = "en",
) -> str:
    scaffold = ""
    if scaffold_visible(analysis_workspace):
        scaffold = """
## Scaffold To Fill

### Inputs

unknown_from_pdf_only. Source locator: paper_not_reported.

### Key Components

unknown_from_pdf_only. Source locator: paper_not_reported.

### Training Or Inference Flow

not_verified_in_alpha. Source locator: unknown_from_pdf_only.

### Outputs

unknown_from_pdf_only. Source locator: paper_not_reported.

### Causal Chain

```mermaid
flowchart TD
    A[Problem Input] --> B[Paper Intervention]
    B --> C[Mechanism Change]
    C --> D[Measured Result]
    D --> E[Claimed Implication]
```

Source locator: unknown_from_pdf_only.

### Assumptions And Likely Failure Points

- paper_not_reported. Source locator: unknown_from_pdf_only.
"""
    return f"""---
paperforge_generated: true
---
# {note_heading('02', language_mode)}

{source_warning(metadata, source_pdf, analysis_workspace)}

## {UI_TEXT[language_mode]['reading_purpose']}

This note answers: How does the method work, what are the inputs and outputs, and what causal chain connects the intervention to the claimed result?

{navigation_block(folder, "02", language_mode)}

{scaffold}

{artifact_block(analysis_workspace, "analysis/04_mechanism.md", "Core Artifact: Mechanism Model")}
"""


def evidence_note_content(
    metadata: dict[str, Any],
    folder: str,
    source_pdf: Path | None,
    analysis_workspace: Path | None,
    language_mode: str = "en",
) -> str:
    scaffold = ""
    if scaffold_visible(analysis_workspace):
        scaffold = """
## Claim Ledger

| ID | Claim | Claim Type | Source Locator | Direct Evidence | Support Level | Limitations / Counterpoints |
|---|---|---|---|---|---|---|
| C1 | Unknown | Author claim | Source locator: paper_not_reported | not_verified_in_alpha | unknown_from_pdf_only | unavailable_without_repo_check |

## Evidence Audit Dimensions

- Control experiments: paper_not_reported. Source locator: unknown_from_pdf_only.
- Ablations: paper_not_reported. Source locator: unknown_from_pdf_only.
- Statistical significance or repeated trials: paper_not_reported. Source locator: unknown_from_pdf_only.
- Failure cases: paper_not_reported. Source locator: unknown_from_pdf_only.
- Benchmark-only risk: not_verified_in_alpha. Source locator: unknown_from_pdf_only.
- Data leakage, selection bias, or overfitting: unavailable_without_repo_check. Source basis: dataset split and code audit not yet performed.
- Cross-environment, cross-device, cross-task validation: paper_not_reported. Source locator: unknown_from_pdf_only.
- Reproduction code, parameters, and data: unavailable_without_repo_check. Source basis: external repository not yet audited.
- Generalization scope: not_verified_in_alpha. Source locator: unknown_from_pdf_only.
- Engineering deployment credibility: paper_not_reported. Source locator: unknown_from_pdf_only.

## Unproven Or Overextended Parts

- not_verified_in_alpha. Source locator: unknown_from_pdf_only.
"""
    return f"""---
paperforge_generated: true
---
# {note_heading('03', language_mode)}

{source_warning(metadata, source_pdf, analysis_workspace)}

## {UI_TEXT[language_mode]['reading_purpose']}

This note keeps author claims separate from proven facts. It asks which evidence supports which claim, what is still unproven, and how credible the engineering conclusion is.

{navigation_block(folder, "03", language_mode)}

{scaffold}

{artifact_block(analysis_workspace, "analysis/02_claim_ledger.md", "Core Artifact: Claim Ledger")}

{artifact_block(analysis_workspace, "analysis/05_evidence_audit.md", "Core Artifact: Evidence Audit")}

{artifact_block(analysis_workspace, "analysis/07_final_brief.md", "Core Artifact: Final Brief")}
"""


def transfer_note_content(
    metadata: dict[str, Any],
    folder: str,
    source_pdf: Path | None,
    analysis_workspace: Path | None,
    language_mode: str = "en",
) -> str:
    scaffold = ""
    if scaffold_visible(analysis_workspace):
        scaffold = """
## Scaffold To Fill

### Relevance To User Profile

not_verified_in_alpha. Source basis: Profile inference plus paper evidence. Paper source locator: unknown_from_pdf_only.

### Industrial Embodied Intelligence Relevance

paper_not_reported. Source locator: unknown_from_pdf_only.

### Directly Transferable Modules

- not_verified_in_alpha. Source locator: unknown_from_pdf_only.

### Non-Transferable Parts

- paper_not_reported. Source locator: unknown_from_pdf_only.

### Verification Experiments

1. unavailable_without_repo_check. Source basis: external code and checkpoint audit not yet performed.
2. not_verified_in_alpha. Source basis: engineering inference from evidence gaps.
3. paper_not_reported. Source locator: unknown_from_pdf_only.

### PaperForge Product Inspiration

not_verified_in_alpha. Source basis: product inference plus paper evidence where applicable.
"""
    return f"""---
paperforge_generated: true
paperforge_user_extendable: true
---
# {note_heading('04', language_mode)}

{source_warning(metadata, source_pdf, analysis_workspace)}

## {UI_TEXT[language_mode]['reading_purpose']}

This note connects the paper to the user's research direction, engineering projects, and industrial embodied-intelligence questions. Transfer judgments are hypotheses unless directly supported by paper evidence.

{navigation_block(folder, "04", language_mode)}

{scaffold}

{artifact_block(analysis_workspace, "analysis/06_transfer_analysis.md", "Core Artifact: Transfer Analysis")}
"""


def recall_note_content(
    metadata: dict[str, Any],
    folder: str,
    source_pdf: Path | None,
    analysis_workspace: Path | None,
    language_mode: str = "en",
) -> str:
    return f"""---
paperforge_generated: true
paperforge_user_extendable: true
---
# {note_heading('05', language_mode)}

{source_warning(metadata, source_pdf, analysis_workspace)}

{navigation_block(folder, "05", language_mode)}

## Important Boundary

Feynman learning is not automatically complete. PaperForge can generate prompts, but the user must restate, correct, and test their own understanding.

## Explain To An Engineer

Unknown. Source locator: Unknown.

## Explain Without Equations

Unknown. Source locator: Unknown.

## Can I Explain Input, Process, Output?

- Input: Unknown.
- Process: Unknown.
- Output: Unknown.
- Evidence boundary: Unknown.

## Active Recall Prompts

1. What problem does the paper solve, and why did prior methods fall short?
2. What exactly changed in the method?
3. Which evidence supports the main claim, and which part remains unproven?
4. What would fail first in a real industrial deployment?
5. If reproducing the paper, what would you verify first?

## My Understanding

Write your own explanation here.

## Unresolved Questions

1. Unknown.
2. Unknown.
3. Unknown.

{artifact_block(analysis_workspace, "learning/08_recall_log.md", "Core Artifact: Recall Log")}
"""


def file_templates(
    metadata: dict[str, Any],
    folder: str,
    source_pdf: Path | None,
    config: dict[str, Any],
    analysis_workspace: Path | None,
    language_mode: str,
) -> dict[str, str]:
    home = f"{folder}.md"
    return {
        home: home_note_content(metadata, folder, source_pdf, analysis_workspace, language_mode),
        note_filename("00", language_mode): source_note_content(metadata, folder, source_pdf, config, analysis_workspace, language_mode),
        note_filename("01", language_mode): problem_contribution_note_content(metadata, folder, source_pdf, analysis_workspace, language_mode),
        note_filename("02", language_mode): mechanism_note_content(metadata, folder, source_pdf, analysis_workspace, language_mode),
        note_filename("03", language_mode): evidence_note_content(metadata, folder, source_pdf, analysis_workspace, language_mode),
        note_filename("04", language_mode): transfer_note_content(metadata, folder, source_pdf, analysis_workspace, language_mode),
        note_filename("05", language_mode): recall_note_content(metadata, folder, source_pdf, analysis_workspace, language_mode),
    }


def manifest_content(
    metadata: dict[str, Any],
    folder: str,
    source_pdf: Path | None,
    analysis_workspace: Path | None,
    *,
    existing_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    identity = derive_identity(metadata)
    now = utc_now()
    state = analysis_workspace_state(analysis_workspace)
    return {
        "paper_id": identity.paper_id,
        "id_strategy": identity.id_strategy,
        "zotero_item_key": identity.zotero_item_key,
        "folder_name": folder,
        "source_pdf_hash": sha256_file(source_pdf),
        "metadata_hash": metadata_hash(metadata),
        "analysis_version": ANALYSIS_VERSION,
        "created_at": (existing_manifest or {}).get("created_at") or now,
        "updated_at": now,
        "status": status_for(metadata, source_pdf, analysis_workspace),
        "pdf_status": pdf_status(metadata, source_pdf),
        "analysis_workspace": analysis_workspace.as_posix() if analysis_workspace else "",
        "analysis_workspace_status": state,
        "semantic_analysis_complete": state == "deep_analysis_complete",
    }


def find_archive_by_paper_id(vault_path: Path, papers_root: str, paper_id: str) -> Path | None:
    root = vault_path / papers_root
    if not root.exists():
        return None
    manifest_paths = list(root.glob("**/paperforge-manifest.json")) + list(root.glob("**/00 Source/ingestion-manifest.json"))
    for manifest in manifest_paths:
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("paper_id") == paper_id:
            if manifest.name == "paperforge-manifest.json":
                return manifest.parent
            return manifest.parents[1]
    return None


def write_text_if_safe(path: Path, content: str, result: ArchiveResult, *, force: bool) -> None:
    refresh_generated = path.exists() and not force and _generated_scaffold_should_refresh(path, content)
    if path.exists() and not force and not refresh_generated:
        result.skipped_existing.append(path.as_posix())
        return
    if path.exists() and (force or refresh_generated):
        backup_dir = path.parent / ".paperforge-backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        digest = hashlib.sha1(str(path.name).encode("utf-8")).hexdigest()[:10]
        suffix = path.suffix.lstrip(".") or "file"
        backup = backup_dir / f"{timestamp}-{digest}.{suffix}.bak"
        shutil.copy2(path, backup)
        result.planned.append(f"backup {backup}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    action = "refresh generated" if refresh_generated else "write"
    result.planned.append(f"{action} {path.as_posix()}")


def ensure_vault_roots(vault_path: Path, config: dict[str, Any], *, dry_run: bool = False) -> list[str]:
    planned: list[str] = []
    roots = [
        config["obsidian"]["papers_root"],
        config["obsidian"]["global_concepts_root"],
        config["obsidian"]["projects_root"],
        config["obsidian"]["reviews_root"],
        config["obsidian"]["templates_root"],
        config["obsidian"]["assets_root"],
    ]
    for root in roots:
        path = vault_path / root
        if path.exists():
            planned.append(f"skip existing {path}")
        else:
            if not dry_run:
                path.mkdir(parents=True, exist_ok=True)
            planned.append(f"create {path}")
    return planned


def create_paper_archive(
    metadata: dict[str, Any],
    config: dict[str, Any],
    *,
    source_pdf: Path | None = None,
    analysis_workspace: Path | None = None,
    dry_run: bool = False,
    force: bool = False,
) -> ArchiveResult:
    identity = derive_identity(metadata)
    vault_path = configured_path(config, "obsidian", "vault_path")
    papers_root = config["obsidian"]["papers_root"]
    pattern = config["naming"]["folder_pattern"]
    max_title = int(config["naming"]["max_short_title_length"])
    folder = folder_name(metadata, pattern=pattern, max_short_title_length=max_title)
    language_settings = metadata.get("paperforge_language_settings") or resolve_language_settings(config)
    note_language = str(language_settings.get("obsidian_note_language") or "en")

    existing_dir = find_archive_by_paper_id(vault_path, papers_root, identity.paper_id)
    archive_dir = existing_dir or (vault_path / papers_root / folder)
    folder = archive_dir.name
    result = ArchiveResult(
        paper_id=identity.paper_id,
        archive_dir=archive_dir,
        folder_name=folder,
        created=existing_dir is None and not archive_dir.exists(),
        status=status_for(metadata, source_pdf, analysis_workspace),
    )

    for directory in PAPER_DIRS:
        path = archive_dir / directory
        if path.exists():
            result.planned.append(f"skip existing {path}")
        else:
            result.planned.append(f"create {path}")
            if not dry_run:
                path.mkdir(parents=True, exist_ok=True)

    existing_manifest = None
    manifest_path = archive_dir / "paperforge-manifest.json"
    legacy_manifest_path = archive_dir / "00 Source" / "ingestion-manifest.json"
    if manifest_path.exists():
        try:
            existing_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing_manifest = None
    elif legacy_manifest_path.exists():
        try:
            existing_manifest = json.loads(legacy_manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing_manifest = None

    templates = file_templates(metadata, folder, source_pdf, config, analysis_workspace, note_language)
    manifest = manifest_content(metadata, folder, source_pdf, analysis_workspace, existing_manifest=existing_manifest)
    manifest["obsidian_note_language"] = note_language
    templates["paperforge-manifest.json"] = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"

    if archive_dir.exists() and has_legacy_numbered_notes(archive_dir):
        result.warnings.append(
            "Legacy Obsidian numbered notes detected (`00.md` through `05.md`). "
            "PaperForge skipped the new titled note layout to avoid duplicating, renaming, or overwriting user content."
        )
        result.warnings.append(
            "Automatic migration from legacy bare numbered notes is not performed by default. "
            "Keep the existing archive as-is, or migrate it manually before re-exporting."
        )
        result.skipped_existing.extend(path.as_posix() for path in legacy_note_paths(archive_dir) if path.exists())
        return result

    if archive_dir.exists():
        current_note_names = {note_filename(number, note_language) for number in NOTE_TITLES}
        existing_titled = existing_titled_note_paths(archive_dir)
        if existing_titled and any(path.name not in current_note_names for path in existing_titled):
            result.warnings.append(
                "Existing Obsidian note filenames appear to use a different title language or naming mode. "
                "PaperForge skipped automatic regeneration to avoid creating duplicate note sets."
            )
            result.warnings.append(
                "If you want a different note language, export into a separate location or migrate the existing archive manually."
            )
            result.skipped_existing.extend(path.as_posix() for path in existing_titled)
            return result

    if not dry_run:
        for relative, content in templates.items():
            target = archive_dir / relative
            if relative == "paperforge-manifest.json":
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                result.planned.append(f"write {target.as_posix()}")
            else:
                write_text_if_safe(target, content, result, force=force)
    else:
        for relative in templates:
            target = archive_dir / relative
            action = "skip existing" if target.exists() else "write"
            result.planned.append(f"{action} {target.as_posix()}")

    return result


def build_index(vault_path: Path, papers_root: str) -> dict[str, Any]:
    root = vault_path / papers_root
    papers: dict[str, Any] = {}
    if root.exists():
        manifest_paths = list(root.glob("**/paperforge-manifest.json")) + list(root.glob("**/00 Source/ingestion-manifest.json"))
        for manifest_path in manifest_paths:
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            paper_id = manifest.get("paper_id")
            if paper_id:
                archive_dir = manifest_path.parent if manifest_path.name == "paperforge-manifest.json" else manifest_path.parents[1]
                papers[paper_id] = {
                    "folder": manifest.get("folder_name") or archive_dir.name,
                    "path": _relative(archive_dir, vault_path),
                    "status": manifest.get("status"),
                    "updated_at": manifest.get("updated_at"),
                    "analysis_workspace_status": manifest.get("analysis_workspace_status"),
                }
    return {"schema_version": 1, "generated_at": utc_now(), "papers": papers}
