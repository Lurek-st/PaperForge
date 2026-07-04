from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .text import normalize_unicode_text, safe_unicode_text, safe_unicode_text_with_warning


def zotero_get_json(config: dict[str, Any], endpoint: str, params: dict[str, Any] | None = None) -> Any:
    base = str(config["zotero"].get("local_api_url") or "").rstrip("/")
    query = f"?{urlencode(params or {})}" if params else ""
    url = f"{base}/{endpoint.lstrip('/')}{query}"
    request = Request(url, headers={"Zotero-API-Version": "3"})
    with urlopen(request, timeout=5) as response:
        return json.loads(response.read())


def _creator_name(creator: dict[str, Any]) -> str:
    name = creator.get("name") or " ".join(
        normalize_unicode_text(part)
        for part in [creator.get("firstName"), creator.get("lastName")]
        if part
    )
    return normalize_unicode_text(name).strip()


def _year_from_date(raw: str) -> int | None:
    match = re.search(r"\b(19|20)\d{2}\b", raw or "")
    return int(match.group(0)) if match else None


def metadata_from_item(item: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    data = item.get("data", item)
    creators = data.get("creators") or []
    authors: list[str] = []
    warnings: list[str] = []
    for creator in creators:
        if not isinstance(creator, dict):
            continue
        raw_name = _creator_name(creator)
        if not raw_name:
            continue
        author, warning = safe_unicode_text_with_warning(raw_name, label="author name")
        authors.append(author)
        if warning:
            warnings.append(warning)
    metadata = {
        "title": safe_unicode_text(data.get("title") or ""),
        "authors": authors,
        "year": _year_from_date(str(data.get("date") or "")),
        "venue": safe_unicode_text(
            data.get("publicationTitle") or data.get("conferenceName") or data.get("proceedingsTitle") or ""
        ),
        "doi": safe_unicode_text(data.get("DOI") or data.get("doi") or ""),
        "arxiv_id": "",
        "source_url": safe_unicode_text(data.get("url") or ""),
        "zotero_item_key": safe_unicode_text(data.get("key") or item.get("key") or ""),
        "zotero_collection": safe_unicode_text(config["zotero"]["collection_name"]),
        "imported_at": safe_unicode_text(data.get("dateAdded") or ""),
        "date_modified": safe_unicode_text(data.get("dateModified") or ""),
    }
    if warnings:
        metadata["paperforge_warnings"] = warnings
    return metadata


def _item_tags(item: dict[str, Any]) -> set[str]:
    data = item.get("data", item)
    tags = data.get("tags") or []
    names: set[str] = set()
    for tag in tags:
        if isinstance(tag, str):
            names.add(tag)
        elif isinstance(tag, dict):
            name = str(tag.get("tag") or "").strip()
            if name:
                names.add(name)
    return names


def _collection_key_by_name(config: dict[str, Any], collection_name: str) -> str | None:
    if not collection_name:
        return None
    collections = zotero_get_json(config, "collections", {"include": "data"})
    for collection in collections:
        data = collection.get("data", collection)
        if str(data.get("name") or "").strip() == collection_name:
            return str(data.get("key") or collection.get("key") or "")
    return None


def _resolve_attachment_path(attachment: dict[str, Any], config: dict[str, Any]) -> Path | None:
    data = attachment.get("data", attachment)
    enclosure = attachment.get("links", {}).get("enclosure", {})
    href = str(enclosure.get("href") or "")
    if href.startswith("file://"):
        parsed = urlparse(href)
        return Path(unquote(parsed.path).lstrip("/"))

    raw_path = str(data.get("path") or "")
    if not raw_path:
        return None
    if raw_path.startswith("storage:"):
        data_dir = str(config["zotero"].get("data_directory") or "")
        if not data_dir:
            return None
        filename = raw_path.split(":", 1)[1]
        attachment_key = data.get("key") or attachment.get("key") or ""
        return Path(data_dir) / "storage" / attachment_key / filename
    path = Path(raw_path).expanduser()
    return path if path.is_absolute() else None


def find_pdf_attachment_path(item_key: str, config: dict[str, Any]) -> Path | None:
    try:
        children = zotero_get_json(config, f"items/{item_key}/children", {"include": "data"})
    except OSError:
        return None
    for child in children:
        data = child.get("data", child)
        if data.get("itemType") != "attachment":
            continue
        content_type = str(data.get("contentType") or "")
        title = str(data.get("title") or data.get("filename") or "")
        if "pdf" not in content_type.lower() and not title.lower().endswith(".pdf"):
            continue
        candidate = _resolve_attachment_path(child, config)
        if candidate and candidate.exists():
            return candidate
    return None


def pending_items(config: dict[str, Any], *, limit: int = 100) -> list[dict[str, Any]]:
    tag = config["zotero"]["pending_tag"]
    tagged = list(
        zotero_get_json(
            config,
            "items",
            {
                "tag": tag,
                "limit": limit,
                "include": "data",
                "itemType": "-attachment",
            },
        )
    )
    if tagged:
        return tagged

    collection_name = str(config["zotero"].get("collection_name") or "").strip()
    collection_key = _collection_key_by_name(config, collection_name)
    if not collection_key:
        return []

    items = zotero_get_json(
        config,
        f"collections/{collection_key}/items",
        {
            "limit": limit,
            "include": "data",
            "itemType": "-attachment",
        },
    )
    processed = str(config["zotero"].get("processed_tag") or "").strip()
    failed = str(config["zotero"].get("failed_tag") or "").strip()
    filtered: list[dict[str, Any]] = []
    for item in items:
        tags = _item_tags(item)
        if processed and processed in tags:
            continue
        if failed and failed in tags:
            continue
        filtered.append(item)
    return filtered
