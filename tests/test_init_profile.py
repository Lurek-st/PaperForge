import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "paper-forge" / "scripts" / "init_profile.py"


class InitProfileTests(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_profile_initialization_creates_template_only_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".paper-forge" / "profile.md"
            result = self.run_script("--profile-path", target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(target.exists())
            self.assertIn("# Research Identity", target.read_text(encoding="utf-8"))
            self.assertIn("Created Profile template", result.stdout)

    def test_profile_initialization_never_overwrites_existing_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".paper-forge" / "profile.md"
            target.parent.mkdir(parents=True)
            target.write_text("CUSTOM PROFILE\n", encoding="utf-8")

            result = self.run_script("--profile-path", target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "CUSTOM PROFILE\n")
            self.assertIn("already exists", result.stdout)

    def test_profile_initialization_supports_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".paper-forge" / "profile.md"
            result = self.run_script("--profile-path", target, "--dry-run")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(target.exists())
            self.assertIn("Dry run", result.stdout)


if __name__ == "__main__":
    unittest.main()

