import subprocess
import sys
import tempfile
import unittest
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "paper-forge" / "scripts"
PAPERFORGE = SCRIPTS / "paperforge.py"
sys.path.insert(0, str(SCRIPTS))

from lib.config import load_config, parse_simple_yaml  # noqa: E402
from lib.obsidian import note_filename  # noqa: E402


class ConfigAndCliTests(unittest.TestCase):
    def run_cli(self, *args, env=None):
        run_env = os.environ.copy()
        if env:
            run_env.update(env)
        return subprocess.run(
            [sys.executable, str(PAPERFORGE), *map(str, args)],
            text=True,
            capture_output=True,
            check=False,
            env=run_env,
        )

    def write_config(self, tmpdir):
        root = Path(tmpdir)
        config_path = root / "config.yaml"
        config_path.write_text(
            f"""
workspace:
  root: "{root.as_posix()}/PaperForge"
  inbox: "{root.as_posix()}/PaperForge/inbox"
  processing: "{root.as_posix()}/PaperForge/processing"
  cache: "{root.as_posix()}/PaperForge/cache"
  failed: "{root.as_posix()}/PaperForge/failed"
  archive: "{root.as_posix()}/PaperForge/archive"
  logs: "{root.as_posix()}/PaperForge/logs"
obsidian:
  vault_path: "{root.as_posix()}/ObsidianVault"
""",
            encoding="utf-8",
        )
        return config_path

    def write_metadata(self, tmpdir, key="ABCD1234"):
        metadata_path = Path(tmpdir) / "metadata.json"
        metadata_path.write_text(
            json.dumps(
                {
                    "title": "Core Chain Test Paper",
                    "authors": ["Ada Lovelace"],
                    "year": 2026,
                    "zotero_item_key": key,
                    "imported_at": "2026-07-04T10:00:00Z",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        return metadata_path

    def write_profile(self, tmpdir, *, default_output_language="auto", obsidian_note_language="auto"):
        profile_root = Path(tmpdir) / ".paper-forge"
        profile_root.mkdir(parents=True, exist_ok=True)
        profile_path = profile_root / "profile.md"
        profile_path.write_text(
            f"""---
profile_version: 1
default_output_language: {default_output_language}
obsidian_note_language: {obsidian_note_language}
preferred_detail_level: detailed
---

# Research Identity

Example user.
""",
            encoding="utf-8",
        )
        return {"PAPERFORGE_HOME": str(profile_root)}

    def write_pdf(self, tmpdir, name="paper.pdf"):
        pdf_path = Path(tmpdir) / name
        pdf_path.write_bytes(b"%PDF-1.4\n% PaperForge test fixture\n")
        return pdf_path

    def test_simple_yaml_config_override(self):
        data = parse_simple_yaml(
            """
workspace:
  root: "D:/Custom/PaperForge"
safety:
  never_modify_zotero_data_directory: true
naming:
  max_short_title_length: 40
"""
        )

        self.assertEqual(data["workspace"]["root"], "D:/Custom/PaperForge")
        self.assertTrue(data["safety"]["never_modify_zotero_data_directory"])
        self.assertEqual(data["naming"]["max_short_title_length"], 40)

    def test_load_config_merges_defaults(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config_path.write_text("obsidian:\n  vault_path: \"D:/Vault\"\n", encoding="utf-8")

            config = load_config(config_path)

            self.assertEqual(config["obsidian"]["vault_path"], "D:/Vault")
            self.assertEqual(config["zotero"]["collection_name"], "PaperForge Inbox")

    def test_default_config_uses_user_level_paths_instead_of_developer_machine_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            previous = os.environ.get("PAPERFORGE_HOME")
            os.environ["PAPERFORGE_HOME"] = str(Path(tmpdir) / ".paper-forge")
            try:
                config = load_config(None)
            finally:
                if previous is None:
                    os.environ.pop("PAPERFORGE_HOME", None)
                else:
                    os.environ["PAPERFORGE_HOME"] = previous

        self.assertIn(".paper-forge", config["workspace"]["root"])
        self.assertIn(".paper-forge", config["obsidian"]["vault_path"])
        self.assertNotIn("D:/Research", config["workspace"]["root"])

    def test_load_config_accepts_utf8_bom(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config_path.write_text('\ufeffobsidian:\n  vault_path: "D:/VaultWithBom"\n', encoding="utf-8")

            config = load_config(config_path)

            self.assertEqual(config["obsidian"]["vault_path"], "D:/VaultWithBom")

    def test_init_cli_prints_first_run_guidance(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = self.write_config(tmpdir)
            result = self.run_cli("--config", config_path, "init")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PaperForge", result.stdout)
            self.assertIn("Zotero", result.stdout)
            self.assertIn("Obsidian", result.stdout)
            self.assertTrue(config_path.exists())

    def test_init_workspace_and_export_obsidian_cli_flow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = self.write_config(tmpdir)
            metadata_path = self.write_metadata(tmpdir)

            ingest = self.run_cli("--config", config_path, "ingest-zotero", "--metadata", metadata_path)
            self.assertEqual(ingest.returncode, 0, ingest.stdout + ingest.stderr)
            self.assertIn("paper_id: zotero:ABCD1234", ingest.stdout)

            init_workspace = self.run_cli("--config", config_path, "init-workspace", "zotero:ABCD1234")
            self.assertEqual(init_workspace.returncode, 0, init_workspace.stdout + init_workspace.stderr)
            self.assertIn("PaperForge core workspace", init_workspace.stdout)

            export = self.run_cli("--config", config_path, "export-obsidian", "zotero:ABCD1234")
            self.assertEqual(export.returncode, 0, export.stdout + export.stderr)
            self.assertIn("Obsidian archive", export.stdout)

            papers = list((Path(tmpdir) / "ObsidianVault" / "Papers").glob("*"))
            self.assertEqual(len(papers), 1)
            self.assertTrue((papers[0] / note_filename("01")).exists())
            self.assertIn("Problem, Prior Limitation", (papers[0] / note_filename("01")).read_text(encoding="utf-8"))

    def test_analyze_compatibility_notice_does_not_claim_deep_completion(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = self.write_config(tmpdir)
            metadata_path = self.write_metadata(tmpdir, key="K8LQ7Z2X")

            result = self.run_cli("--config", config_path, "analyze", "--metadata", metadata_path)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("does not perform semantic deep paper analysis by itself", result.stdout)
            self.assertIn("Obsidian archive", result.stdout)

    def test_deep_cli_creates_workspace_and_marks_template_incomplete(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = self.write_config(tmpdir)
            metadata_path = self.write_metadata(tmpdir, key="DEEP1234")

            ingest = self.run_cli("--config", config_path, "ingest-zotero", "--metadata", metadata_path)
            self.assertEqual(ingest.returncode, 0, ingest.stdout + ingest.stderr)

            result = self.run_cli("--config", config_path, "deep", "zotero:DEEP1234")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Analysis completeness check did not pass", result.stdout)
            self.assertIn("status: analysis_incomplete", result.stdout)
            papers = list((Path(tmpdir) / "ObsidianVault" / "Papers").glob("*"))
            self.assertEqual(len(papers), 1)
            manifest = json.loads((papers[0] / "paperforge-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "metadata_only")
            self.assertEqual(manifest["analysis_workspace_status"], "analysis_incomplete")

    def test_deep_cli_strict_complete_returns_nonzero_for_incomplete_workspace(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = self.write_config(tmpdir)
            metadata_path = self.write_metadata(tmpdir, key="STRICT12")

            result = self.run_cli("--config", config_path, "deep", "--metadata", metadata_path, "--strict-complete", "--no-export")

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("analysis_incomplete", result.stdout)

    def test_deep_cli_with_pdf_skips_obsidian_export_until_analysis_is_complete(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = self.write_config(tmpdir)
            metadata_path = self.write_metadata(tmpdir, key="PDFHOLD1")
            pdf_path = self.write_pdf(tmpdir)

            ingest = self.run_cli("--config", config_path, "ingest-zotero", "--metadata", metadata_path, "--pdf", pdf_path)
            self.assertEqual(ingest.returncode, 0, ingest.stdout + ingest.stderr)

            result = self.run_cli("--config", config_path, "deep", "zotero:PDFHOLD1")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("status: analysis_incomplete", result.stdout)
            self.assertIn("Skipping Obsidian export because deep analysis is still incomplete", result.stdout)
            self.assertFalse((Path(tmpdir) / "ObsidianVault" / "Papers").exists())

    def test_export_obsidian_reports_legacy_numbered_notes_without_overwriting(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = self.write_config(tmpdir)
            metadata_path = self.write_metadata(tmpdir, key="LEGACY01")

            ingest = self.run_cli("--config", config_path, "ingest-zotero", "--metadata", metadata_path)
            self.assertEqual(ingest.returncode, 0, ingest.stdout + ingest.stderr)

            first_export = self.run_cli("--config", config_path, "export-obsidian", "zotero:LEGACY01")
            self.assertEqual(first_export.returncode, 0, first_export.stdout + first_export.stderr)

            paper_dir = next((Path(tmpdir) / "ObsidianVault" / "Papers").glob("*"))
            for number in ["00", "01", "02", "03", "04", "05"]:
                legacy = paper_dir / f"{number}.md"
                titled = paper_dir / note_filename(number)
                legacy.write_text(titled.read_text(encoding="utf-8"), encoding="utf-8")
                titled.unlink()

            second_export = self.run_cli("--config", config_path, "export-obsidian", "zotero:LEGACY01")

            self.assertEqual(second_export.returncode, 0, second_export.stdout + second_export.stderr)
            self.assertIn("Legacy Obsidian note layout detected.", second_export.stdout)
            self.assertIn("PaperForge will not auto-rename, migrate, or overwrite", second_export.stdout)
            self.assertTrue((paper_dir / "01.md").exists())
            self.assertFalse((paper_dir / note_filename("01")).exists())

    def test_profile_language_setting_changes_obsidian_note_language(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = self.write_config(tmpdir)
            metadata_path = self.write_metadata(tmpdir, key="PROFILE1")
            env = self.write_profile(tmpdir, default_output_language="zh", obsidian_note_language="zh")

            self.run_cli("--config", config_path, "ingest-zotero", "--metadata", metadata_path, env=env)
            export = self.run_cli("--config", config_path, "export-obsidian", "zotero:PROFILE1", env=env)

            self.assertEqual(export.returncode, 0, export.stdout + export.stderr)
            paper_dir = next((Path(tmpdir) / "ObsidianVault" / "Papers").glob("*"))
            self.assertTrue((paper_dir / note_filename("01", "zh")).exists())
            self.assertIn("obsidian_note_language: zh", export.stdout)

    def test_cli_language_overrides_profile_language_setting(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = self.write_config(tmpdir)
            metadata_path = self.write_metadata(tmpdir, key="PROFILE2")
            env = self.write_profile(tmpdir, default_output_language="zh", obsidian_note_language="zh")

            self.run_cli("--config", config_path, "ingest-zotero", "--metadata", metadata_path, env=env)
            export = self.run_cli(
                "--config",
                config_path,
                "export-obsidian",
                "zotero:PROFILE2",
                "--language",
                "en",
                "--obsidian-language",
                "bilingual",
                env=env,
            )

            self.assertEqual(export.returncode, 0, export.stdout + export.stderr)
            paper_dir = next((Path(tmpdir) / "ObsidianVault" / "Papers").glob("*"))
            self.assertTrue((paper_dir / note_filename("01", "bilingual")).exists())
            self.assertIn("requested_output_language: en", export.stdout)
            self.assertIn("obsidian_note_language: bilingual", export.stdout)


if __name__ == "__main__":
    unittest.main()
