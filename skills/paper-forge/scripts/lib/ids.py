from __future__ import annotations

import base64
import hashlib
import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from typing import Any


WINDOWS_FORBIDDEN = '<>:"/\\|?*'
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


@dataclass(frozen=True)
class PaperIdentity:
    paper_id: str
    id_strategy: str
    stable_key: str
    zotero_item_key: str


def sanitize_windows_segment(value: str, *, fallback: str = "Paper", max_length: int = 80) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    cleaned = "".join("_" if char in WINDOWS_FORBIDDEN or ord(char) < 32 else char for char in ascii_text)
    cleaned = re.sub(r"\s+", "_", cleaned)
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", cleaned)
    cleaned = cleaned.strip("._ ")
    if not cleaned:
        cleaned = fallback
    if cleaned.upper() in WINDOWS_RESERVED_NAMES:
        cleaned = f"{cleaned}_paper"
    cleaned = cleaned[:max_length].strip("._ ")
    return cleaned or fallback


def short_title(title: str, max_length: int = 80) -> str:
    cleaned = sanitize_windows_segment(title, fallback="Untitled_Paper", max_length=max_length)
    cleaned = re.sub(r"[_-]+", "_", cleaned).strip("_")
    return cleaned or "Untitled_Paper"


def _stable_hash(value: str, length: int = 8) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return base64.b32encode(digest).decode("ascii").rstrip("=")[:length]


def _first_text(metadata: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = metadata.get(key)
        if value:
            return str(value).strip()
    return ""


def _author_string(metadata: dict[str, Any]) -> str:
    authors = metadata.get("authors") or metadata.get("creators") or []
    if isinstance(authors, str):
        return authors
    parts: list[str] = []
    for author in authors:
        if isinstance(author, str):
            parts.append(author)
        elif isinstance(author, dict):
            name = author.get("name") or " ".join(part for part in [author.get("firstName"), author.get("lastName")] if part)
            if name:
                parts.append(str(name))
    return "; ".join(parts)


def derive_identity(metadata: dict[str, Any]) -> PaperIdentity:
    zotero_key = _first_text(metadata, "zotero_item_key", "zoteroKey", "key")
    if zotero_key:
        stable_key = sanitize_windows_segment(zotero_key, fallback="zotero_key", max_length=40)
        return PaperIdentity(f"zotero:{zotero_key}", "zotero_item_key", stable_key, zotero_key)

    doi = _first_text(metadata, "doi", "DOI")
    if doi:
        stable_key = sanitize_windows_segment(doi, fallback="doi", max_length=40)
        return PaperIdentity(f"doi:{doi}", "doi", stable_key, "")

    arxiv_id = _first_text(metadata, "arxiv_id", "arXiv", "arxiv")
    if arxiv_id:
        stable_key = sanitize_windows_segment(arxiv_id, fallback="arxiv", max_length=40)
        return PaperIdentity(f"arxiv:{arxiv_id}", "arxiv_id", stable_key, "")

    title = _first_text(metadata, "title")
    year = _first_text(metadata, "year", "date")
    hash_input = "|".join([title, _author_string(metadata), year])
    stable_key = _stable_hash(hash_input or "untitled")
    return PaperIdentity(f"hash:{stable_key}", "title_author_year_hash", stable_key, "")


def import_date(metadata: dict[str, Any], run_date: date | None = None) -> str:
    for key in ("import_date", "imported_at", "date_added"):
        value = metadata.get(key)
        if value:
            text = str(value)
            match = re.match(r"\d{4}-\d{2}-\d{2}", text)
            if match:
                return match.group(0)
    return (run_date or date.today()).isoformat()


def folder_name(metadata: dict[str, Any], *, pattern: str, max_short_title_length: int, run_date: date | None = None) -> str:
    identity = derive_identity(metadata)
    title = _first_text(metadata, "short_title") or _first_text(metadata, "title") or "Untitled Paper"
    values = {
        "import_date": import_date(metadata, run_date),
        "short_title": short_title(title, max_short_title_length),
        "stable_key": identity.stable_key,
        "zotero_key": identity.zotero_item_key or identity.stable_key,
    }
    return sanitize_windows_segment(pattern.format(**values), fallback=identity.stable_key, max_length=180)
