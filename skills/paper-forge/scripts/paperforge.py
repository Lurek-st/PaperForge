#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.config import configured_path, ensure_config_file, load_config  # noqa: E402
from lib.ids import derive_identity  # noqa: E402
from lib.language import VALID_LANGUAGE_MODES, resolve_language_settings  # noqa: E402
from lib.links import inspect_ambiguous_links  # noqa: E402
from lib.obsidian import build_index, create_paper_archive, ensure_vault_roots  # noqa: E402
from lib.validation import assess_analysis_completeness, validate_workspace  # noqa: E402
from lib.workspace import (  # noqa: E402
    create_analysis_workspace,
    create_work_package,
    ensure_workspace_dirs,
    find_analysis_workspace_by_paper_id,
    find_package_by_paper_id,
    load_analysis_workspace_metadata,
    load_package,
    update_analysis_workspace_status,
)
from lib.zotero import find_pdf_attachment_path, metadata_from_item, pending_items  # noqa: E402


CLOUD_MARKERS = {"onedrive", "dropbox", "google drive", "googledrive", "iclouddrive"}


def print_initialization_prompt() -> None:
    print("")
    print("PaperForge initialized.")
    print("")
    print("Recommended workflow:")
    print("1. Install and open Zotero Desktop.")
    print("2. Create the Zotero collection: PaperForge Inbox.")
    print("3. Save papers with Zotero Connector into PaperForge Inbox.")
    print("4. Run ingest-zotero to create controlled work packages.")
    print("5. Run deep zotero:<key> as the main PaperForge entry point.")
    print("6. Fill source-located deep artifacts in Codex, then rerun deep to export.")
    print("")
    print("Important:")
    print("- Zotero is the source of truth for original PDFs and standard metadata.")
    print("- PaperForge does not modify Zotero storage/ or zotero.sqlite.")
    print("- Do not place the Zotero data directory inside a cloud sync folder.")
    print("- Prefer moving or renaming PaperForge notes inside Obsidian.")


def print_no_zotero_desktop_prompt() -> None:
    print("Zotero Desktop Local API is not reachable.")
    print("")
    print("You may have installed only Zotero Connector. Connector collects papers from web pages,")
    print("but the local PaperForge workflow needs Zotero Desktop to manage PDFs and metadata.")
    print("")
    print("Please install and open Zotero Desktop, then rerun this command.")


def print_pdf_missing_prompt() -> None:
    print("Metadata was found, but no accessible PDF was found.")
    print("")
    print("PaperForge will create metadata-only scaffolding. It must not claim full-text experiment review,")
    print("evidence review, or Feynman understanding until a PDF is available.")
    print("Please confirm the PDF exists in Zotero, or provide a PDF manually and rerun.")


def print_existing_archive_prompt(path: Path) -> None:
    print("This paper already has a PaperForge Obsidian archive.")
    print("")
    print("Existing directory:")
    print(path.as_posix())
    print("")
    print("Default behavior: keep user-written content and skip existing notes.")
    print("Use --force only after reviewing the change list; existing files will be backed up first.")


def print_legacy_archive_prompt() -> None:
    print("Legacy Obsidian note layout detected.")
    print("")
    print("This archive still uses bare numbered notes like `00.md` through `05.md`.")
    print("PaperForge will not auto-rename, migrate, or overwrite those files by default.")
    print("Review the existing notes first, then migrate manually if you want the new titled-note layout.")


def print_metadata_warnings(metadata: dict) -> None:
    warnings = metadata.get("paperforge_warnings") or []
    for warning in warnings:
        print(f"warning: {warning}")


def print_language_settings(metadata: dict) -> None:
    settings = metadata.get("paperforge_language_settings") or {}
    if not settings:
        return
    print(f"requested_output_language: {settings.get('analysis_language_requested')}")
    print(f"resolved_output_language: {settings.get('analysis_language')}")
    print(f"obsidian_note_language: {settings.get('obsidian_note_language')}")


def print_analyze_compatibility_notice() -> None:
    print("Compatibility notice:")
    print("`analyze` prepares a PaperForge core workspace and exports an Obsidian archive shell.")
    print("It does not perform semantic deep paper analysis by itself.")
    print("Use `deep` as the main PaperForge entry point.")
    print("")


def print_workspace_next_step(workspace: Path) -> None:
    print("")
    print("Next PaperForge deep step:")
    print(f"- Core workspace: {workspace}")
    print("- Fill the source-located analysis files under analysis/:")
    print("  analysis/01_triage.md")
    print("  analysis/02_claim_ledger.md")
    print("  analysis/03_contribution_map.md")
    print("  analysis/04_mechanism.md")
    print("  analysis/05_evidence_audit.md")
    print("  analysis/06_transfer_analysis.md")
    print("  analysis/07_final_brief.md")
    print("- Then rerun `paperforge deep <paper_id>` to validate and export.")


def is_cloud_path(path: Path) -> bool:
    lowered_parts = {part.lower() for part in path.parts}
    return any(marker in lowered_parts or marker in str(path).lower() for marker in CLOUD_MARKERS)


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def check_zotero_local_api(config: dict) -> tuple[bool, str]:
    url = str(config["zotero"].get("local_api_url") or "").rstrip("/") + "/items?limit=1"
    request = Request(url, headers={"Zotero-API-Version": "3"})
    try:
        with urlopen(request, timeout=2) as response:
            response.read(1)
        return True, url
    except (OSError, URLError, TimeoutError) as exc:
        return False, str(exc)


def load_metadata_file(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def package_paper_id(package_dir: Path) -> str:
    manifest_path = package_dir / "manifest.json"
    if manifest_path.exists():
        try:
            return str(json.loads(manifest_path.read_text(encoding="utf-8")).get("paper_id") or "")
        except json.JSONDecodeError:
            return ""
    return ""


def metadata_paper_id(metadata: dict) -> str:
    return derive_identity(metadata).paper_id


def apply_language_settings(
    metadata: dict,
    config: dict,
    *,
    explicit_language: str | None,
    explicit_obsidian_language: str | None,
) -> dict:
    enriched = dict(metadata)
    enriched["paperforge_language_settings"] = resolve_language_settings(
        config,
        explicit_language=explicit_language,
        explicit_obsidian_language=explicit_obsidian_language,
    )
    return enriched


def resolve_target(
    config: dict,
    target: str | None,
    *,
    metadata_path: Path | None = None,
    pdf_path: Path | None = None,
) -> tuple[dict, Path | None, Path | None]:
    if metadata_path:
        return load_metadata_file(metadata_path), pdf_path, None
    if not target:
        raise ValueError("A paper_id, package directory, or --metadata is required.")
    target_path = Path(target)
    if target_path.exists():
        if (target_path / "source" / "metadata.json").exists():
            metadata, source_pdf, package_dir = load_analysis_workspace_metadata(target_path)
            return metadata, source_pdf, package_dir
        metadata, source_pdf = load_package(target_path)
        return metadata, source_pdf, target_path
    package = find_package_by_paper_id(config, target)
    if not package:
        raise FileNotFoundError(f"No PaperForge work package found for {target}")
    metadata, source_pdf = load_package(package)
    return metadata, source_pdf, package


def find_workspace_for_metadata(config: dict, metadata: dict, package_dir: Path | None) -> Path | None:
    paper_id = package_paper_id(package_dir) if package_dir else metadata_paper_id(metadata)
    if paper_id:
        return find_analysis_workspace_by_paper_id(config, paper_id)
    return None


def export_archive(
    metadata: dict,
    config: dict,
    *,
    source_pdf: Path | None,
    analysis_workspace: Path | None,
    dry_run: bool,
    force: bool,
) -> int:
    result = create_paper_archive(
        metadata,
        config,
        source_pdf=source_pdf,
        analysis_workspace=analysis_workspace,
        dry_run=dry_run,
        force=force,
    )
    if not result.created:
        print_existing_archive_prompt(result.archive_dir)
    if result.status == "metadata_only":
        print_pdf_missing_prompt()
    print_metadata_warnings(metadata)
    print_language_settings(metadata)
    print(f"Obsidian archive: {result.archive_dir}")
    print(f"paper_id: {result.paper_id}")
    print(f"status: {result.status}")
    if analysis_workspace:
        print(f"analysis_workspace: {analysis_workspace}")
    for line in result.planned:
        print(line)
    for warning in result.warnings:
        print(warning)
    if result.warnings:
        print_legacy_archive_prompt()
    if result.skipped_existing:
        print("Skipped existing files to protect user-authored content:")
        for item in result.skipped_existing:
            print(f"- {item}")
        print("Use --force only after reviewing backups and intended changes.")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    config_path, created = ensure_config_file(args.config, dry_run=args.dry_run)
    config = load_config(config_path) if config_path.exists() else load_config(None)
    print(f"Config: {config_path}")
    print("create config" if created else "skip existing config")

    for line in ensure_workspace_dirs(config, dry_run=args.dry_run):
        print(line)
    for line in ensure_vault_roots(configured_path(config, "obsidian", "vault_path"), config, dry_run=args.dry_run):
        print(line)
    if not args.dry_run:
        print_initialization_prompt()
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    issues = 0

    print("PaperForge doctor")
    print(f"Workspace root: {configured_path(config, 'workspace', 'root')}")
    print(f"Obsidian vault: {configured_path(config, 'obsidian', 'vault_path')}")

    for directory in ensure_workspace_dirs(config, dry_run=args.dry_run):
        print(directory)

    vault_path = configured_path(config, "obsidian", "vault_path")
    if args.dry_run:
        print(f"check writable {vault_path}")
    else:
        try:
            vault_path.mkdir(parents=True, exist_ok=True)
            probe = vault_path / ".paperforge-write-test"
            probe.write_text("ok\n", encoding="utf-8")
            probe.unlink()
            print(f"writable {vault_path}")
        except OSError as exc:
            issues += 1
            print(f"Obsidian Vault is not writable: {exc}")

    zotero_dir_text = str(config["zotero"].get("data_directory") or "")
    if zotero_dir_text:
        zotero_dir = Path(zotero_dir_text).expanduser()
        if is_cloud_path(zotero_dir):
            issues += 1
            print("High-risk directory structure detected.")
            print("Zotero data should not live in OneDrive, Dropbox, Google Drive, or another sync folder.")
        if is_relative_to(vault_path, zotero_dir):
            issues += 1
            print("High-risk directory structure detected.")
            print("Obsidian Vault should not be nested inside the Zotero data directory.")
            print("Recommended layout:")
            print("D:\\Research\\ZoteroData")
            print("D:\\Research\\PaperForge")
            print("D:\\Research\\ObsidianVault")

    if config["zotero"].get("enabled") and config["zotero"].get("integration_mode") == "local_api":
        ok, detail = check_zotero_local_api(config)
        if ok:
            print("Zotero Desktop Local API is reachable.")
        else:
            issues += 1
            print_no_zotero_desktop_prompt()
            print(f"Technical detail: {detail}")

    return 0 if issues == 0 else 1


def cmd_ingest_zotero(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    if not args.metadata:
        ok, detail = check_zotero_local_api(config)
        if not ok:
            print_no_zotero_desktop_prompt()
            print(f"Technical detail: {detail}")
            return 1
        print("Zotero Desktop Local API is reachable.")
        items = pending_items(config, limit=args.limit)
        if not items:
            print(f"No Zotero items found with pending tag or eligible items in collection: {config['zotero']['collection_name']}")
            print("Tip: save a paper into the PaperForge Inbox collection or use --metadata and --pdf for manual import.")
            return 0
        skipped_existing: list[str] = []
        imported_any = False
        for item in items:
            metadata = apply_language_settings(
                metadata_from_item(item, config),
                config,
                explicit_language=args.language,
                explicit_obsidian_language=args.obsidian_language,
            )
            paper_id = metadata_paper_id(metadata)
            if not args.force and (find_package_by_paper_id(config, paper_id) or find_analysis_workspace_by_paper_id(config, paper_id)):
                skipped_existing.append(f"{paper_id} {metadata.get('title') or 'Untitled Paper'}")
                continue
            item_key = metadata.get("zotero_item_key") or ""
            pdf_path = find_pdf_attachment_path(item_key, config) if item_key else None
            result = create_work_package(metadata, config, pdf_path=pdf_path, dry_run=args.dry_run, force=args.force)
            print_metadata_warnings(metadata)
            print_language_settings(metadata)
            print(f"Paper package: {result.package_dir}")
            print(f"paper_id: {result.paper_id}")
            for line in result.planned:
                print(line)
            if result.pdf_status == "missing":
                print_pdf_missing_prompt()
            imported_any = True
        if skipped_existing:
            print("Skipped already-ingested Zotero items:")
            for item in skipped_existing:
                print(f"- {item}")
        if not imported_any:
            print("No new Zotero items required ingestion.")
        return 0

    metadata = apply_language_settings(
        load_metadata_file(args.metadata),
        config,
        explicit_language=args.language,
        explicit_obsidian_language=args.obsidian_language,
    )
    result = create_work_package(metadata, config, pdf_path=args.pdf, dry_run=args.dry_run, force=args.force)
    print_metadata_warnings(metadata)
    print_language_settings(metadata)
    print(f"Paper package: {result.package_dir}")
    print(f"paper_id: {result.paper_id}")
    for line in result.planned:
        print(line)
    if result.pdf_status == "missing":
        print_pdf_missing_prompt()
    return 0


def cmd_init_workspace(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        metadata, source_pdf, package_dir = resolve_target(
            config,
            args.target,
            metadata_path=args.metadata,
            pdf_path=args.pdf,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(str(exc))
        return 2 if isinstance(exc, ValueError) else 1
    metadata = apply_language_settings(
        metadata,
        config,
        explicit_language=args.language,
        explicit_obsidian_language=args.obsidian_language,
    )

    result = create_analysis_workspace(
        metadata,
        config,
        package_dir=package_dir,
        source_pdf=source_pdf,
        mode=args.mode,
        dry_run=args.dry_run,
        force=args.force,
    )
    print(f"PaperForge core workspace: {result.workspace_dir}")
    print(f"paper_id: {result.paper_id}")
    print(f"mode: {result.mode}")
    print(f"status: {result.status}")
    print_language_settings(metadata)
    for line in result.planned:
        print(line)
    if result.skipped_existing:
        print("Skipped existing analysis files to protect user-authored or already-filled content:")
        for item in result.skipped_existing:
            print(f"- {item}")
    if source_pdf is None:
        print_pdf_missing_prompt()
    print_workspace_next_step(result.workspace_dir)
    return 0


def cmd_export_obsidian(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        metadata, source_pdf, package_dir = resolve_target(
            config,
            args.target,
            metadata_path=args.metadata,
            pdf_path=args.pdf,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(str(exc))
        return 2 if isinstance(exc, ValueError) else 1
    metadata = apply_language_settings(
        metadata,
        config,
        explicit_language=args.language,
        explicit_obsidian_language=args.obsidian_language,
    )

    analysis_workspace = args.analysis_workspace or find_workspace_for_metadata(config, metadata, package_dir)
    if not analysis_workspace:
        print("No PaperForge core analysis workspace was found for this paper.")
        print("This export will create titled Obsidian reading notes as a safe scaffold, not completed deep analysis.")
    return export_archive(
        metadata,
        config,
        source_pdf=source_pdf,
        analysis_workspace=analysis_workspace,
        dry_run=args.dry_run,
        force=args.force,
    )


def cmd_deep(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        metadata, source_pdf, package_dir = resolve_target(
            config,
            args.target,
            metadata_path=args.metadata,
            pdf_path=args.pdf,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(str(exc))
        return 2 if isinstance(exc, ValueError) else 1
    metadata = apply_language_settings(
        metadata,
        config,
        explicit_language=args.language,
        explicit_obsidian_language=args.obsidian_language,
    )

    workspace = args.analysis_workspace or find_workspace_for_metadata(config, metadata, package_dir)
    if not workspace:
        created = create_analysis_workspace(
            metadata,
            config,
            package_dir=package_dir,
            source_pdf=source_pdf,
            mode="deep",
            dry_run=args.dry_run,
            force=False,
        )
        workspace = created.workspace_dir
        print(f"PaperForge core workspace: {workspace}")
        print("status: analysis_workspace_ready")
        for line in created.planned:
            print(line)
    else:
        print(f"Using existing PaperForge core workspace: {workspace}")

    if args.dry_run:
        print("Dry run: deep workflow planning completed; no validation status was written.")
        return 0

    if source_pdf is None:
        print_pdf_missing_prompt()

    structural = validate_workspace(workspace, mode="deep")
    if structural.passed:
        print("Structural validation passed.")
    else:
        print("Structural validation failed.")
        for error in structural.errors:
            print(f"- {error}")

    completeness = assess_analysis_completeness(workspace)
    update_analysis_workspace_status(
        workspace,
        status=completeness.status,
        semantic_analysis_complete=completeness.complete,
    )

    if completeness.complete:
        print("Analysis completeness check passed.")
        print("status: deep_analysis_complete")
    else:
        print("Analysis completeness check did not pass.")
        print("status: analysis_incomplete")
        for issue in completeness.issues:
            print(f"- {issue}")
        print_workspace_next_step(workspace)

    should_export = not args.no_export and (source_pdf is None or completeness.complete)
    if should_export:
        export_archive(
            metadata,
            config,
            source_pdf=source_pdf,
            analysis_workspace=workspace,
            dry_run=False,
            force=args.force,
        )
    elif not args.no_export:
        print("")
        print("Skipping Obsidian export because deep analysis is still incomplete.")
        print("Use `paperforge export-obsidian <paper_id>` only if you explicitly want an incomplete scaffold.")

    if args.strict_complete and (not structural.passed or not completeness.complete):
        return 1
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    print_analyze_compatibility_notice()
    return cmd_deep(args)


def cmd_status(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    for area in ["inbox", "archive", "failed"]:
        root = configured_path(config, "workspace", area)
        print(f"{area}: {root}")
        if not root.exists():
            continue
        for manifest_path in root.glob("*/manifest.json"):
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                print(f"- invalid manifest: {manifest_path}")
                continue
            print(f"- {manifest.get('paper_id')} [{manifest.get('status')}] {manifest_path.parent.name}")

    processing = configured_path(config, "workspace", "processing")
    print(f"processing: {processing}")
    if processing.exists():
        for manifest_path in processing.glob("*/paperforge-workspace-manifest.json"):
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                print(f"- invalid analysis manifest: {manifest_path}")
                continue
            print(f"- {manifest.get('paper_id')} [{manifest.get('status')}] {manifest_path.parent.name}")
    return 0


def cmd_reindex(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    vault_path = configured_path(config, "obsidian", "vault_path")
    index = build_index(vault_path, config["obsidian"]["papers_root"])
    cache_dir = configured_path(config, "workspace", "cache")
    index_path = cache_dir / "obsidian-index.json"
    if not args.dry_run:
        cache_dir.mkdir(parents=True, exist_ok=True)
        index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Indexed {len(index['papers'])} paper archives.")
    print(f"Index path: {index_path}")
    return 0


def cmd_repair_links(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    vault_path = configured_path(config, "obsidian", "vault_path")
    report = inspect_ambiguous_links(vault_path)
    if report.passed:
        print("No ambiguous bare Obsidian links found.")
        return 0
    print("Ambiguous bare Obsidian links found:")
    for issue in report.issues:
        print(f"- {issue.file}: [[{issue.link}]] - {issue.message}")
    print("Use full Vault-relative links such as [[Papers/<paper-folder>/01|Problem And Contribution]].")
    return 1


def cmd_clean_cache(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    cache_dir = configured_path(config, "workspace", "cache").resolve()
    workspace_root = configured_path(config, "workspace", "root").resolve()
    if not is_relative_to(cache_dir, workspace_root):
        print(f"Refusing to clean cache outside workspace root: {cache_dir}")
        return 1
    if not args.yes:
        print("Refusing to clean cache without --yes. This command never deletes Zotero-managed PDFs.")
        return 2
    if not cache_dir.exists():
        print(f"Cache directory does not exist: {cache_dir}")
        return 0
    for child in cache_dir.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
        print(f"deleted {child}")
    return 0


def cmd_watch(args: argparse.Namespace) -> int:
    print("watch is not enabled in the deterministic local MVP.")
    print("Use `paperforge ingest-zotero`, then `paperforge deep <paper_id>`.")
    return 2


def add_target_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("target", nargs="?", help="Paper ID, work package directory, or analysis workspace directory.")
    parser.add_argument("--metadata", type=Path, help="Metadata JSON, bypassing a work package.")
    parser.add_argument("--pdf", type=Path, help="Optional PDF for source availability and hashing.")


def add_deep_like_args(parser: argparse.ArgumentParser) -> None:
    add_target_args(parser)
    parser.add_argument("--language", choices=sorted(VALID_LANGUAGE_MODES), help="Requested analysis output language.")
    parser.add_argument(
        "--obsidian-language",
        choices=sorted(VALID_LANGUAGE_MODES),
        help="Requested Obsidian file name and navigation language. Defaults to --language when provided.",
    )
    parser.add_argument("--analysis-workspace", type=Path, help="Existing PaperForge core workspace to import.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Version existing Obsidian files before overwriting them.")
    parser.add_argument("--no-export", action="store_true", help="Validate and update workspace state without exporting to Obsidian.")
    parser.add_argument("--strict-complete", action="store_true", help="Return non-zero if the deep workspace is incomplete.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PaperForge local Zotero-to-Obsidian helper CLI.")
    parser.add_argument("--config", type=Path, default=None, help="Path to PaperForge config YAML or JSON.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Initialize config, workspace directories, and Obsidian roots.")
    init.add_argument("--dry-run", action="store_true")
    init.set_defaults(func=cmd_init)

    doctor = subparsers.add_parser("doctor", help="Check workspace, Vault, and Zotero Local API availability.")
    doctor.add_argument("--dry-run", action="store_true")
    doctor.set_defaults(func=cmd_doctor)

    ingest = subparsers.add_parser("ingest-zotero", help="Create a PaperForge work package from Zotero or manual metadata.")
    ingest.add_argument("--metadata", type=Path, help="Metadata JSON exported from Zotero or prepared manually.")
    ingest.add_argument("--pdf", type=Path, help="PDF copied/exported from Zotero into a controlled location.")
    ingest.add_argument("--limit", type=int, default=100, help="Maximum pending Zotero items to import when using Local API.")
    ingest.add_argument("--language", choices=sorted(VALID_LANGUAGE_MODES), help="Requested analysis output language.")
    ingest.add_argument(
        "--obsidian-language",
        choices=sorted(VALID_LANGUAGE_MODES),
        help="Requested Obsidian file name and navigation language. Defaults to --language when provided.",
    )
    ingest.add_argument("--dry-run", action="store_true")
    ingest.add_argument("--force", action="store_true", help="Overwrite package metadata/PDF after explicit user choice.")
    ingest.set_defaults(func=cmd_ingest_zotero)

    init_workspace = subparsers.add_parser("init-workspace", help="Create the core PaperForge screen/deep/recall workspace.")
    add_target_args(init_workspace)
    init_workspace.add_argument("--language", choices=sorted(VALID_LANGUAGE_MODES), help="Requested analysis output language.")
    init_workspace.add_argument(
        "--obsidian-language",
        choices=sorted(VALID_LANGUAGE_MODES),
        help="Requested Obsidian file name and navigation language. Defaults to --language when provided.",
    )
    init_workspace.add_argument("--mode", choices=["screen", "deep", "recall"], default="deep")
    init_workspace.add_argument("--dry-run", action="store_true")
    init_workspace.add_argument("--force", action="store_true", help="Back up and overwrite existing core workspace files.")
    init_workspace.set_defaults(func=cmd_init_workspace)

    deep = subparsers.add_parser("deep", help="Main PaperForge workflow entry point for one paper.")
    add_deep_like_args(deep)
    deep.set_defaults(func=cmd_deep)

    export = subparsers.add_parser("export-obsidian", help="Export a work package or core workspace into titled Obsidian reading notes.")
    add_target_args(export)
    export.add_argument("--language", choices=sorted(VALID_LANGUAGE_MODES), help="Requested analysis output language.")
    export.add_argument(
        "--obsidian-language",
        choices=sorted(VALID_LANGUAGE_MODES),
        help="Requested Obsidian file name and navigation language. Defaults to --language when provided.",
    )
    export.add_argument("--analysis-workspace", type=Path, help="Existing PaperForge core workspace to import into titled reading notes.")
    export.add_argument("--dry-run", action="store_true")
    export.add_argument("--force", action="store_true", help="Version existing files before overwriting them.")
    export.set_defaults(func=cmd_export_obsidian)

    analyze = subparsers.add_parser(
        "analyze",
        help="Compatibility command: use `deep` semantics and print a compatibility notice.",
    )
    add_deep_like_args(analyze)
    analyze.set_defaults(func=cmd_analyze)

    status = subparsers.add_parser("status", help="Show work package and core workspace status.")
    status.set_defaults(func=cmd_status)

    reindex = subparsers.add_parser("reindex", help="Rebuild the Obsidian archive index from manifests.")
    reindex.add_argument("--dry-run", action="store_true")
    reindex.set_defaults(func=cmd_reindex)

    repair = subparsers.add_parser("repair-links", help="Detect ambiguous bare Obsidian links.")
    repair.set_defaults(func=cmd_repair_links)

    clean = subparsers.add_parser("clean-cache", help="Safely clean PaperForge cache files only.")
    clean.add_argument("--yes", action="store_true", help="Confirm cache cleanup.")
    clean.set_defaults(func=cmd_clean_cache)

    watch = subparsers.add_parser("watch", help="Reserved for future polling of pending Zotero items.")
    watch.set_defaults(func=cmd_watch)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
