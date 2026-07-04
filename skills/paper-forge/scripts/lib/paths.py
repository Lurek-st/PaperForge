import os
from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parents[2]


def assets_dir() -> Path:
    return skill_root() / "assets"


def asset_path(name: str) -> Path:
    return assets_dir() / name


def default_profile_dir() -> Path:
    override = os.getenv("PAPERFORGE_HOME")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".paper-forge"


def default_profile_path() -> Path:
    return default_profile_dir() / "profile.md"


def default_workspace_base() -> Path:
    return default_profile_dir() / "workspace"


def default_obsidian_export_root() -> Path:
    return default_profile_dir() / "obsidian-vault"


def default_workspace_root() -> Path:
    return default_workspace_base() / "processing"
