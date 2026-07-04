from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
BARE_NUMBERED_NOTE_RE = re.compile(r"^\d{2}$")


@dataclass
class LinkIssue:
    file: Path
    link: str
    message: str


@dataclass
class LinkReport:
    issues: list[LinkIssue] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.issues


def note_stems(vault_path: Path) -> dict[str, list[Path]]:
    stems: dict[str, list[Path]] = {}
    for markdown in vault_path.glob("**/*.md"):
        stems.setdefault(markdown.stem, []).append(markdown)
    return stems


def inspect_ambiguous_links(vault_path: Path) -> LinkReport:
    stems = note_stems(vault_path)
    report = LinkReport()
    for markdown in vault_path.glob("**/*.md"):
        try:
            text = markdown.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in WIKI_LINK_RE.finditer(text):
            target = match.group(1).strip()
            if "/" in target:
                continue
            if BARE_NUMBERED_NOTE_RE.fullmatch(target):
                report.issues.append(
                    LinkIssue(
                        file=markdown,
                        link=target,
                        message="Bare numbered Obsidian link; use the titled full Vault-relative path.",
                    )
                )
                continue
            candidates = stems.get(Path(target).stem, [])
            if len(candidates) > 1:
                report.issues.append(
                    LinkIssue(
                        file=markdown,
                        link=target,
                        message="Ambiguous bare Obsidian link; use a full Vault-relative path.",
                    )
                )
    return report
