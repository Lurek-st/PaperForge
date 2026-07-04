from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from .paths import default_obsidian_export_root, default_profile_dir, default_workspace_base

DEFAULT_CONFIG: dict[str, Any] = {
    "zotero": {
        "enabled": True,
        "integration_mode": "local_api",
        "collection_name": "PaperForge Inbox",
        "pending_tag": "paperforge:pending",
        "processed_tag": "paperforge:processed",
        "failed_tag": "paperforge:failed",
        "data_directory": "",
        "local_api_url": "http://127.0.0.1:23119/api/users/0",
    },
    "workspace": {
        "root": str(default_workspace_base()),
        "inbox": str(default_workspace_base() / "inbox"),
        "processing": str(default_workspace_base() / "processing"),
        "cache": str(default_workspace_base() / "cache"),
        "failed": str(default_workspace_base() / "failed"),
        "archive": str(default_workspace_base() / "archive"),
        "logs": str(default_workspace_base() / "logs"),
    },
    "obsidian": {
        "vault_path": str(default_obsidian_export_root()),
        "papers_root": "Papers",
        "global_concepts_root": "Global Concepts",
        "projects_root": "Projects",
        "reviews_root": "Reviews",
        "templates_root": "Templates",
        "assets_root": "Assets",
    },
    "language": {
        "default_output_language": "auto",
        "obsidian_note_language": "en",
        "fallback_output_language": "en",
        "bilingual_separator": " | ",
    },
    "naming": {
        "folder_pattern": "{import_date}__{short_title}__{stable_key}",
        "home_note_pattern": "{import_date}__{short_title}__{stable_key}.md",
        "sanitize_for_windows": True,
        "max_short_title_length": 50,
    },
    "safety": {
        "never_modify_zotero_data_directory": True,
        "never_overwrite_user_authored_notes": True,
        "require_confirmation_before_force_overwrite": True,
        "create_versions_before_regeneration": True,
    },
}


def default_config_path() -> Path:
    return default_profile_dir() / "config.yaml"


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if not value:
        return ""
    if value[0:1] in {"'", '"'} and value[-1:] == value[0]:
        return value[1:-1]
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none", "~"}:
        return None
    try:
        return int(value)
    except ValueError:
        return value


def parse_simple_yaml(text: str) -> dict[str, Any]:
    """Parse the small nested mapping shape used by PaperForge config files."""
    result: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, result)]

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2:
            raise ValueError(f"Unsupported YAML indentation at line {line_number}")
        line = raw_line.strip()
        if ":" not in line:
            raise ValueError(f"Expected key/value pair at line {line_number}")
        key, raw_value = line.split(":", 1)
        key = key.strip().lstrip("\ufeff")
        if not key:
            raise ValueError(f"Empty key at line {line_number}")

        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if raw_value.strip() == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = _parse_scalar(raw_value)

    return result


def load_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or default_config_path()
    if not config_path.exists():
        return copy.deepcopy(DEFAULT_CONFIG)
    text = config_path.read_text(encoding="utf-8-sig")
    if config_path.suffix.lower() == ".json":
        override = json.loads(text)
    else:
        override = parse_simple_yaml(text)
    return deep_merge(DEFAULT_CONFIG, override)


def dump_simple_yaml(data: dict[str, Any], indent: int = 0) -> str:
    lines: list[str] = []
    prefix = " " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            lines.append(dump_simple_yaml(value, indent + 2).rstrip())
        else:
            if isinstance(value, bool):
                rendered = "true" if value else "false"
            elif value is None:
                rendered = "null"
            elif isinstance(value, int):
                rendered = str(value)
            else:
                escaped = str(value).replace('"', '\\"')
                rendered = f'"{escaped}"'
            lines.append(f"{prefix}{key}: {rendered}")
    return "\n".join(lines) + "\n"


def ensure_config_file(path: Path | None = None, *, dry_run: bool = False) -> tuple[Path, bool]:
    config_path = path or default_config_path()
    if config_path.exists():
        return config_path, False
    if not dry_run:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(dump_simple_yaml(DEFAULT_CONFIG), encoding="utf-8")
    return config_path, True


def configured_path(config: dict[str, Any], *keys: str) -> Path:
    value: Any = config
    for key in keys:
        value = value[key]
    return Path(str(value)).expanduser()
