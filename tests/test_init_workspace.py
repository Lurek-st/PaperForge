import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "paper-forge" / "scripts"
INIT_WORKSPACE = SCRIPTS / "init_workspace.py"
sys.path.insert(0, str(SCRIPTS))

from lib.slug import safe_slug  # noqa: E402


class InitWorkspaceTests(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run(
            [sys.executable, str(INIT_WORKSPACE), *map(str, args)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_workspace_initialization_creates_expected_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "paper"
            result = self.run_script("./Example Paper.pdf", "--workspace", workspace, "--title", "Example Paper")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((workspace / "source").is_dir())
            self.assertTrue((workspace / "analysis").is_dir())
            self.assertTrue((workspace / "learning").is_dir())
            self.assertTrue((workspace / "source" / "source_manifest.md").exists())
            self.assertTrue((workspace / "README_FOR_READING.md").exists())
            self.assertTrue((workspace / "analysis" / "07_final_brief.md").exists())
            self.assertTrue((workspace / "run_state.json").exists())
            self.assertIn("Reading guide:", result.stdout)
            self.assertIn("analysis/01_triage.md", result.stdout)
            self.assertIn("VS Code", result.stdout)

    def test_workspace_initialization_never_overwrites_existing_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "paper"
            self.run_script("--workspace", workspace)
            triage = workspace / "analysis" / "01_triage.md"
            triage.write_text("CUSTOM TRIAGE\n", encoding="utf-8")

            result = self.run_script("--workspace", workspace)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(triage.read_text(encoding="utf-8"), "CUSTOM TRIAGE\n")
            self.assertIn("skip existing", result.stdout)

    def test_safe_slug_generation_works(self):
        self.assertEqual(safe_slug("A/B: Test & Delta!"), "a-b-test-delta")
        self.assertEqual(safe_slug("论文 Δ"), "paper")
        self.assertEqual(safe_slug("  Many---spaces___here  "), "many-spaces-here")


if __name__ == "__main__":
    unittest.main()
