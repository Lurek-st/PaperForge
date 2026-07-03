from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ValidationResult:
    workspace: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors


REQUIRED_DIRS = ["source", "analysis", "learning"]

READING_GUIDE_FILE = {
    "README_FOR_READING.md": ["# Reading Guide", "## Numbered Markdown Files", "## How To Open"],
}

SCREEN_FILES = {
    **READING_GUIDE_FILE,
    "source/source_manifest.md": ["# Source Manifest", "## Paper Metadata", "## Analysis Limitations"],
    "analysis/01_triage.md": ["# Triage", "## Paper Problem", "## Recommendation"],
}

DEEP_FILES = {
    **SCREEN_FILES,
    "analysis/profile_snapshot.md": [
        "# Profile Snapshot",
        "## Snapshot Source",
        "## Analysis-Relevant Profile Content",
    ],
    "analysis/02_claim_ledger.md": ["# Claim Ledger", "## Claim Table"],
    "analysis/03_contribution_map.md": ["# Contribution Map", "## Core Sentence", "## Counterfactual Sentence"],
    "analysis/04_mechanism.md": ["# Mechanism Model", "## Mermaid Causal Chain"],
    "analysis/05_evidence_audit.md": ["# Evidence Audit", "## Credibility Dimensions"],
    "analysis/06_transfer_analysis.md": ["# Transfer Analysis", "## Relevance Layers"],
    "analysis/07_final_brief.md": ["# Final Brief", "## One-Sentence Conclusion", "## Recommendation"],
}

RECALL_FILE = "learning/08_recall_log.md"

NUMBERED_SOURCE_LOCATOR_FILES = [
    "analysis/01_triage.md",
    "analysis/02_claim_ledger.md",
    "analysis/03_contribution_map.md",
    "analysis/04_mechanism.md",
    "analysis/05_evidence_audit.md",
    "analysis/06_transfer_analysis.md",
    "analysis/07_final_brief.md",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _has_heading(text: str, heading: str) -> bool:
    return any(line.strip().lower() == heading.lower() for line in text.splitlines())


def _load_run_state(path: Path, result: ValidationResult) -> dict:
    if not path.exists():
        result.errors.append("Missing run_state.json")
        return {}
    try:
        return json.loads(_read(path))
    except json.JSONDecodeError as exc:
        result.errors.append(f"Invalid run_state.json: {exc}")
        return {}


def _validate_file(path: Path, headings: list[str], result: ValidationResult) -> str:
    if not path.exists():
        result.errors.append(f"Missing required file: {path.relative_to(result.workspace)}")
        return ""
    text = _read(path)
    for heading in headings:
        if not _has_heading(text, heading):
            result.errors.append(f"Missing heading {heading!r} in {path.relative_to(result.workspace)}")
    return text


def _validate_claim_ledger(text: str, result: ValidationResult) -> None:
    lowered = " ".join(text.lower().replace("|", " | ").split())
    required = ["id", "claim", "claim type", "source locator", "direct evidence", "support level", "limitations / counterpoints"]
    for field_name in required:
        if field_name not in lowered:
            result.errors.append(f"Claim Ledger missing table field: {field_name}")


def _validate_mechanism(text: str, result: ValidationResult) -> None:
    lowered = text.lower()
    if "```mermaid" not in lowered:
        result.errors.append("Mechanism file missing Mermaid fenced block")
    if "flowchart" not in lowered:
        result.errors.append("Mechanism Mermaid block missing flowchart declaration")


def _validate_evidence_audit(text: str, result: ValidationResult) -> None:
    required = [
        "internal evidence credibility",
        "external reproducibility readiness",
        "engineering transfer credibility",
    ]
    lowered = text.lower()
    for item in required:
        if item not in lowered:
            result.errors.append(f"Evidence Audit missing credibility dimension: {item}")


def _has_source_locator(text: str) -> bool:
    lowered = text.lower()
    return "source locator" in lowered or "source basis" in lowered or "paper source locator" in lowered


def _validate_numbered_source_locators(file_texts: dict[str, str], result: ValidationResult) -> None:
    for relative in NUMBERED_SOURCE_LOCATOR_FILES:
        text = file_texts.get(relative)
        if text is not None and text and not _has_source_locator(text):
            result.errors.append(f"Numbered output missing Source locator scaffolding: {relative}")


def validate_workspace(workspace: Path, mode: str = "deep") -> ValidationResult:
    workspace = workspace.resolve()
    result = ValidationResult(workspace=workspace)

    if not workspace.exists():
        result.errors.append(f"Workspace does not exist: {workspace}")
        return result

    for directory in REQUIRED_DIRS:
        if not (workspace / directory).is_dir():
            result.errors.append(f"Missing required directory: {directory}")

    run_state = _load_run_state(workspace / "run_state.json", result)

    required_files = SCREEN_FILES if mode == "screen" else DEEP_FILES
    file_texts: dict[str, str] = {}
    for relative, headings in required_files.items():
        file_texts[relative] = _validate_file(workspace / relative, headings, result)

    if "analysis/02_claim_ledger.md" in file_texts:
        _validate_claim_ledger(file_texts["analysis/02_claim_ledger.md"], result)

    if "analysis/04_mechanism.md" in file_texts:
        _validate_mechanism(file_texts["analysis/04_mechanism.md"], result)

    if "analysis/05_evidence_audit.md" in file_texts:
        _validate_evidence_audit(file_texts["analysis/05_evidence_audit.md"], result)

    _validate_numbered_source_locators(file_texts, result)

    recall_started = bool(run_state.get("recall_started")) or run_state.get("mode") == "recall"
    if recall_started:
        recall_text = _validate_file(workspace / RECALL_FILE, ["# Recall Log"], result)
        if recall_text and "## Recall Interactions" not in recall_text:
            result.errors.append("Recall Log missing interactions section")
        if recall_text and not _has_source_locator(recall_text):
            result.errors.append("Recall Log missing source basis or source locator")

    result.warnings.append("Semantic accuracy not automatically verified")
    return result
