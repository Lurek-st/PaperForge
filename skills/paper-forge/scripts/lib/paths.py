from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parents[2]


def assets_dir() -> Path:
    return skill_root() / "assets"


def asset_path(name: str) -> Path:
    return assets_dir() / name


def default_profile_dir() -> Path:
    return Path.home() / ".paper-forge"


def default_profile_path() -> Path:
    return default_profile_dir() / "profile.md"


def default_workspace_root() -> Path:
    return Path.home() / "paper-forge-workspace" / "papers"

