import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "paper-forge" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from lib.config import DEFAULT_CONFIG, deep_merge  # noqa: E402
from lib.links import inspect_ambiguous_links  # noqa: E402
from lib.obsidian import NOTE_TITLES, build_index, create_paper_archive, find_archive_by_paper_id, note_filename  # noqa: E402
from lib.workspace import create_analysis_workspace, update_analysis_workspace_status  # noqa: E402


def temp_config(tmp: Path):
    return deep_merge(
        DEFAULT_CONFIG,
        {
            "workspace": {
                "root": str(tmp / "PaperForge"),
                "inbox": str(tmp / "PaperForge" / "inbox"),
                "processing": str(tmp / "PaperForge" / "processing"),
                "cache": str(tmp / "PaperForge" / "cache"),
                "failed": str(tmp / "PaperForge" / "failed"),
                "archive": str(tmp / "PaperForge" / "archive"),
                "logs": str(tmp / "PaperForge" / "logs"),
            },
            "obsidian": {"vault_path": str(tmp / "ObsidianVault")},
        },
    )


class ObsidianArchiveTests(unittest.TestCase):
    def metadata(self, *, title="Example Paper", key="ABCD1234"):
        return {
            "title": title,
            "authors": ["Ada Lovelace"],
            "year": 2026,
            "zotero_item_key": key,
            "zotero_collection": "PaperForge Inbox",
            "imported_at": "2026-07-04T10:00:00Z",
            "doi": "10.1000/example",
            "source_url": "https://example.test/paper",
        }

    def metadata_with_language(self, language: str, *, obsidian_language: str | None = None, key: str | None = None):
        metadata = self.metadata(key=key or f"EXAMPLE-{language.upper()}")
        metadata["paperforge_language_settings"] = {
            "analysis_language_requested": language,
            "analysis_language": language if language != "auto" else "en",
            "obsidian_note_language_requested": obsidian_language or language,
            "obsidian_note_language": obsidian_language or language,
        }
        return metadata

    def write_pdf(self, root: Path, name="source.pdf") -> Path:
        pdf_path = root / name
        pdf_path.write_bytes(b"%PDF-1.4\n% PaperForge archive test\n")
        return pdf_path

    def test_internal_duplicate_filenames_do_not_collide_and_links_are_full_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            first = create_paper_archive(self.metadata(title="Paper A", key="ABCD1234"), config)
            second = create_paper_archive(self.metadata(title="Paper B", key="K8LQ7Z2X"), config)

            self.assertTrue((first.archive_dir / note_filename("01")).exists())
            self.assertTrue((second.archive_dir / note_filename("01")).exists())
            self.assertNotEqual(first.archive_dir, second.archive_dir)

            home = (first.archive_dir / f"{first.folder_name}.md").read_text(encoding="utf-8")
            self.assertIn(
                f"[[Papers/{first.folder_name}/01 - Problem, Prior Limitation, Actual Contribution|01 - Problem, Prior Limitation, Actual Contribution]]",
                home,
            )
            self.assertNotIn("[[paper-overview]]", home)
            self.assertFalse((first.archive_dir / "README.md").exists())
            self.assertFalse((first.archive_dir / "01 Paper Analysis").exists())

    def test_same_title_with_different_zotero_keys_creates_unique_archives(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            first = create_paper_archive(self.metadata(title="Same Title", key="ABCD1234"), config)
            second = create_paper_archive(self.metadata(title="Same Title", key="K8LQ7Z2X"), config)

            self.assertNotEqual(first.folder_name, second.folder_name)
            self.assertIn("ABCD1234", first.folder_name)
            self.assertIn("K8LQ7Z2X", second.folder_name)

            first_manifest = json.loads((first.archive_dir / "paperforge-manifest.json").read_text(encoding="utf-8"))
            second_manifest = json.loads((second.archive_dir / "paperforge-manifest.json").read_text(encoding="utf-8"))
            self.assertNotEqual(first_manifest["paper_id"], second_manifest["paper_id"])

    def test_duplicate_import_reuses_existing_archive(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            first = create_paper_archive(self.metadata(), config)
            second = create_paper_archive(self.metadata(), config)
            paper_dirs = list((Path(tmpdir) / "ObsidianVault" / "Papers").glob("*"))

            self.assertEqual(first.archive_dir, second.archive_dir)
            self.assertFalse(second.created)
            self.assertEqual(len(paper_dirs), 1)
            self.assertTrue(second.skipped_existing)

    def test_missing_pdf_creates_metadata_only_without_full_text_claims(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            result = create_paper_archive(self.metadata(), config)
            manifest = json.loads((result.archive_dir / "paperforge-manifest.json").read_text(encoding="utf-8"))
            experiment = (result.archive_dir / note_filename("01")).read_text(encoding="utf-8")

            self.assertEqual(manifest["status"], "metadata_only")
            self.assertEqual(manifest["pdf_status"], "missing")
            self.assertIn("metadata-only", experiment)
            self.assertIn("unknown_from_pdf_only", experiment)

    def test_numbered_notes_follow_core_argument_chain(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            result = create_paper_archive(self.metadata(), config)

            note01_path = result.archive_dir / note_filename("01")
            note02_path = result.archive_dir / note_filename("02")
            note03_path = result.archive_dir / note_filename("03")
            note04_path = result.archive_dir / note_filename("04")
            note05_path = result.archive_dir / note_filename("05")
            note01 = note01_path.read_text(encoding="utf-8")
            note02 = note02_path.read_text(encoding="utf-8")
            note03 = note03_path.read_text(encoding="utf-8")
            note04 = note04_path.read_text(encoding="utf-8")
            note05 = note05_path.read_text(encoding="utf-8")

            self.assertEqual(
                [path.name for path in [note01_path, note02_path, note03_path, note04_path, note05_path]],
                [note_filename("01"), note_filename("02"), note_filename("03"), note_filename("04"), note_filename("05")],
            )
            self.assertIn("# 01 - Problem, Prior Limitation, Actual Contribution", note01)
            self.assertIn("# 02 - Mechanism, Method, Causal Chain", note02)
            self.assertIn("| ID | Claim | Claim Type | Source Locator | Direct Evidence | Support Level |", note03)
            self.assertIn("# 04 - Transfer Analysis, User Research Relevance, Project Ideas", note04)
            self.assertIn("# 05 - Feynman Recall, Self-Explanation, Open Questions", note05)
            self.assertIn(
                f"[[Papers/{result.folder_name}/{note_filename('02').removesuffix('.md')}|02 - Mechanism, Method, Causal Chain]]",
                note01,
            )
            self.assertIn(
                f"[[Papers/{result.folder_name}/{note_filename('05').removesuffix('.md')}|05 - Feynman Recall, Self-Explanation, Open Questions]]",
                note04,
            )
            self.assertFalse((result.archive_dir / "01.md").exists())

    def test_export_can_import_core_workspace_artifacts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            metadata = self.metadata()
            workspace = create_analysis_workspace(metadata, config)
            claim_file = workspace.workspace_dir / "analysis" / "02_claim_ledger.md"
            claim_file.write_text(
                "# Claim Ledger\n\n"
                "| ID | Claim | Claim Type | Source Locator | Direct Evidence | Support Level | Limitations / Counterpoints |\n"
                "|---|---|---|---|---|---|---|\n"
                "| C1 | Robots can transfer web knowledge | Author claim | Section 4 | Experiment table | Partial | Needs real factory validation |\n",
                encoding="utf-8",
            )

            result = create_paper_archive(metadata, config, analysis_workspace=workspace.workspace_dir)
            note03 = (result.archive_dir / note_filename("03")).read_text(encoding="utf-8")
            manifest = json.loads((result.archive_dir / "paperforge-manifest.json").read_text(encoding="utf-8"))

            self.assertIn("Imported from PaperForge core artifact: `analysis/02_claim_ledger.md`", note03)
            self.assertIn("Robots can transfer web knowledge", note03)
            self.assertEqual(manifest["analysis_workspace_status"], "analysis_workspace_ready")

    def test_completed_export_hides_scaffold_sections(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            metadata = self.metadata()
            pdf_path = self.write_pdf(Path(tmpdir), "complete.pdf")
            workspace = create_analysis_workspace(metadata, config, source_pdf=pdf_path)
            update_analysis_workspace_status(
                workspace.workspace_dir,
                status="deep_analysis_complete",
                semantic_analysis_complete=True,
            )

            result = create_paper_archive(metadata, config, source_pdf=pdf_path, analysis_workspace=workspace.workspace_dir)
            note01 = (result.archive_dir / note_filename("01")).read_text(encoding="utf-8")

            self.assertNotIn("## Scaffold To Fill", note01)
            self.assertIn("completed PaperForge deep workspace", note01)

    def test_completed_export_refreshes_generated_incomplete_notes_without_force(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            metadata = self.metadata()
            pdf_path = self.write_pdf(Path(tmpdir), "refresh.pdf")
            workspace = create_analysis_workspace(metadata, config, source_pdf=pdf_path)
            first = create_paper_archive(metadata, config, source_pdf=pdf_path, analysis_workspace=workspace.workspace_dir)

            (workspace.workspace_dir / "analysis" / "01_triage.md").write_text(
                "# Triage\n\n## Paper Problem\n\nFilled. Source locator: Section 1.\n\n## Recommendation\n\nDeep. Source basis: Section 1.\n",
                encoding="utf-8",
            )
            update_analysis_workspace_status(
                workspace.workspace_dir,
                status="deep_analysis_complete",
                semantic_analysis_complete=True,
            )

            second = create_paper_archive(metadata, config, source_pdf=pdf_path, analysis_workspace=workspace.workspace_dir)
            note01 = (first.archive_dir / note_filename("01")).read_text(encoding="utf-8")
            backups = list((first.archive_dir / ".paperforge-backups").glob("*.bak"))

            self.assertEqual(first.archive_dir, second.archive_dir)
            self.assertIn("completed PaperForge deep workspace", note01)
            self.assertNotIn("## Scaffold To Fill", note01)
            self.assertTrue(backups)

    def test_reindex_rediscovers_archive_after_folder_move(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            result = create_paper_archive(self.metadata(), config)
            destination = result.archive_dir.parent / "Important" / result.archive_dir.name
            destination.parent.mkdir(parents=True)
            shutil.move(str(result.archive_dir), str(destination))

            found = find_archive_by_paper_id(Path(tmpdir) / "ObsidianVault", "Papers", result.paper_id)
            index = build_index(Path(tmpdir) / "ObsidianVault", "Papers")

            self.assertEqual(found, destination)
            self.assertEqual(index["papers"][result.paper_id]["path"], f"Papers/Important/{result.folder_name}")

    def test_user_authored_notes_are_not_overwritten_on_regeneration(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            result = create_paper_archive(self.metadata(), config)
            note = result.archive_dir / note_filename("03")
            note.write_text("USER NOTES\n", encoding="utf-8")

            create_paper_archive(self.metadata(), config)

            self.assertEqual(note.read_text(encoding="utf-8"), "USER NOTES\n")

    def test_force_regeneration_uses_short_backup_names_for_long_home_note(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            result = create_paper_archive(self.metadata(title="A Very Long Paper Title " * 10), config)

            create_paper_archive(self.metadata(title="A Very Long Paper Title " * 10), config, force=True)

            backups = list((result.archive_dir / ".paperforge-backups").glob("*.bak"))
            self.assertTrue(backups)
            self.assertLess(max(len(path.name) for path in backups), 40)

    def test_ambiguous_bare_links_are_reported(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            first = create_paper_archive(self.metadata(title="Paper A", key="ABCD1234"), config)
            create_paper_archive(self.metadata(title="Paper B", key="K8LQ7Z2X"), config)
            (first.archive_dir / "bad-link.md").write_text("[[01]]\n", encoding="utf-8")

            report = inspect_ambiguous_links(Path(tmpdir) / "ObsidianVault")

            self.assertFalse(report.passed)
            self.assertEqual(report.issues[0].link, "01")

    def test_existing_legacy_numbered_notes_are_skipped_without_silent_migration(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            result = create_paper_archive(self.metadata(), config)

            for number in NOTE_TITLES:
                titled = result.archive_dir / note_filename(number)
                legacy = result.archive_dir / f"{number}.md"
                legacy.write_text(f"legacy {number}\n", encoding="utf-8")
                titled.unlink()
                self.assertFalse(titled.exists())

            second = create_paper_archive(self.metadata(), config)

            self.assertTrue(second.warnings)
            self.assertIn("Legacy Obsidian numbered notes detected", second.warnings[0])
            for number in NOTE_TITLES:
                self.assertTrue((result.archive_dir / f"{number}.md").exists())
                self.assertFalse((result.archive_dir / note_filename(number)).exists())

    def test_chinese_note_language_changes_filenames_titles_and_navigation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            result = create_paper_archive(self.metadata_with_language("zh"), config)

            note01 = result.archive_dir / note_filename("01", "zh")
            home = (result.archive_dir / f"{result.folder_name}.md").read_text(encoding="utf-8")
            note01_text = note01.read_text(encoding="utf-8")

            self.assertTrue(note01.exists())
            self.assertIn("# 01 - 论文定位、原有局限与真实贡献", note01_text)
            self.assertIn("## 导航", note01_text)
            self.assertIn("[[Papers/", home)
            self.assertIn("01 - 论文定位、原有局限与真实贡献", home)

    def test_bilingual_note_language_changes_filenames_titles_and_navigation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            result = create_paper_archive(self.metadata_with_language("bilingual"), config)

            note01 = result.archive_dir / note_filename("01", "bilingual")
            note01_text = note01.read_text(encoding="utf-8")

            self.assertTrue(note01.exists())
            self.assertIn("论文定位、原有局限与真实贡献 · Problem, Prior Limitation, Actual Contribution", note01.name)
            self.assertIn("## 导航 | Navigation", note01_text)

    def test_existing_titled_notes_in_different_language_are_not_duplicated(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = temp_config(Path(tmpdir))
            first = create_paper_archive(self.metadata_with_language("zh", key="LANGSAFE1"), config)

            second = create_paper_archive(self.metadata_with_language("en", key="LANGSAFE1"), config)

            self.assertTrue(second.warnings)
            self.assertIn("different title language", second.warnings[0])
            self.assertFalse((first.archive_dir / note_filename("01", "en")).exists())


if __name__ == "__main__":
    unittest.main()
