from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import parse_simple_yaml
from .paths import asset_path, default_profile_path


@dataclass
class ProfileInitResult:
    target: Path
    created: bool
    existed: bool
    dry_run: bool


def template_path() -> Path:
    return asset_path("profile-template.md")


def example_profile_path() -> Path:
    return Path(__file__).resolve().parents[4] / "profile.example.md"


def create_profile_if_missing(
    target: Optional[Path] = None,
    template: Optional[Path] = None,
    dry_run: bool = False,
) -> ProfileInitResult:
    target_path = target or default_profile_path()
    template_file = template or template_path()

    if target_path.exists():
        return ProfileInitResult(target_path, created=False, existed=True, dry_run=dry_run)

    if not dry_run:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        content = template_file.read_text(encoding="utf-8")
        target_path.write_text(content, encoding="utf-8")

    return ProfileInitResult(target_path, created=True, existed=False, dry_run=dry_run)


def backup_existing_profile(target: Path) -> Path:
    if not target.exists():
        raise FileNotFoundError(f"Profile does not exist: {target}")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = target.with_name(f"{target.stem}.{timestamp}.bak{target.suffix}")
    shutil.copy2(target, backup)
    return backup


def analysis_relevant_snapshot(profile_text: str, source_path: Path) -> str:
    allowed_headings = {
        "# Research Identity",
        "# Priority Questions",
        "# Preferred Application Contexts",
        "# Output Preferences",
        "# Terminology Preferences",
        "# Low Priority Topics",
    }
    lines = profile_text.splitlines()
    captured: list[str] = []
    keep = False
    for line in lines:
        if line.startswith("# "):
            keep = line.strip() in allowed_headings
        if keep:
            captured.append(line)
    body = "\n".join(captured).strip() or "No analysis-relevant Profile content was detected."
    return (
        "# Profile Snapshot\n\n"
        "## Snapshot Source\n\n"
        f"- Source profile path: `{source_path}`\n"
        "- Snapshot purpose: reproducible relevance and transfer analysis\n\n"
        "## Analysis-Relevant Profile Content\n\n"
        f"{body}\n"
    )


PROFILE_LANGUAGE_DEFAULTS = {
    "default_output_language": "auto",
    "obsidian_note_language": "auto",
    "preferred_detail_level": "detailed",
}


def _frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    _, _, remainder = text.partition("---\n")
    frontmatter, separator, _ = remainder.partition("\n---")
    return frontmatter if separator else ""


def load_profile_preferences(target: Optional[Path] = None) -> dict[str, str]:
    profile_path = target or default_profile_path()
    preferences = dict(PROFILE_LANGUAGE_DEFAULTS)
    if not profile_path.exists():
        return preferences

    text = profile_path.read_text(encoding="utf-8")
    frontmatter = _frontmatter(text)
    if not frontmatter:
        return preferences

    try:
        data = parse_simple_yaml(frontmatter)
    except ValueError:
        return preferences

    for key in PROFILE_LANGUAGE_DEFAULTS:
        value = data.get(key)
        if value not in {None, ""}:
            preferences[key] = str(value)
    return preferences
