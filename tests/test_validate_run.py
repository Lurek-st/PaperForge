import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "paper-forge" / "scripts"
INIT_WORKSPACE = SCRIPTS / "init_workspace.py"
VALIDATE = SCRIPTS / "validate_run.py"
sys.path.insert(0, str(SCRIPTS))

from lib.validation import assess_analysis_completeness  # noqa: E402


class ValidateRunTests(unittest.TestCase):
    def run_cmd(self, *args):
        return subprocess.run(
            [sys.executable, *map(str, args)],
            text=True,
            capture_output=True,
            check=False,
        )

    def make_workspace(self, root: Path, mode: str = "recall") -> Path:
        workspace = root / "workspace"
        init = self.run_cmd(INIT_WORKSPACE, "./paper.pdf", "--workspace", workspace, "--title", "Complete Paper", "--mode", mode)
        self.assertEqual(init.returncode, 0, init.stderr)
        return workspace

    def validate(self, workspace: Path):
        return self.run_cmd(VALIDATE, workspace)

    def test_complete_deep_workspace_passes_structural_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.make_workspace(Path(tmp), mode="recall")

            result = self.validate(workspace)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Structural validation passed", result.stdout)
            self.assertIn("Semantic accuracy not automatically verified", result.stdout)

    def test_missing_required_report_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.make_workspace(Path(tmp), mode="deep")
            (workspace / "analysis" / "07_final_brief.md").unlink()

            result = self.validate(workspace)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Structural validation failed", result.stdout)
            self.assertIn("07_final_brief.md", result.stdout)

    def test_missing_reading_guide_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.make_workspace(Path(tmp), mode="deep")
            (workspace / "README_FOR_READING.md").unlink()

            result = self.validate(workspace)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("README_FOR_READING.md", result.stdout)

    def test_missing_source_locator_in_numbered_file_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.make_workspace(Path(tmp), mode="deep")
            (workspace / "analysis" / "03_contribution_map.md").write_text(
                "# Contribution Map\n\n"
                "## Core Sentence\n\n"
                "This paper's core is: by X, it solves Y, therefore it can Z.\n\n"
                "## Counterfactual Sentence\n\n"
                "If X is removed, the remaining contribution is Y.\n",
                encoding="utf-8",
            )

            result = self.validate(workspace)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Source locator", result.stdout)

    def test_missing_mermaid_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.make_workspace(Path(tmp), mode="deep")
            (workspace / "analysis" / "04_mechanism.md").write_text(
                "# Mechanism Model\n\n## Mermaid Causal Chain\n\nNo diagram.\n",
                encoding="utf-8",
            )

            result = self.validate(workspace)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Mermaid", result.stdout)

    def test_missing_claim_ledger_source_locator_structure_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.make_workspace(Path(tmp), mode="deep")
            (workspace / "analysis" / "02_claim_ledger.md").write_text(
                "# Claim Ledger\n\n## Claim Table\n\n| ID | Claim | Claim Type | Direct Evidence | Support Level |\n|---|---|---|---|---|\n",
                encoding="utf-8",
            )

            result = self.validate(workspace)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source locator", result.stdout.lower())

    def test_missing_evidence_dimensions_fail_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.make_workspace(Path(tmp), mode="deep")
            (workspace / "analysis" / "05_evidence_audit.md").write_text(
                "# Evidence Audit\n\n## Credibility Dimensions\n\n- Overall: Unknown\n",
                encoding="utf-8",
            )

            result = self.validate(workspace)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("internal evidence credibility", result.stdout.lower())

    def test_invalid_run_state_json_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.make_workspace(Path(tmp), mode="deep")
            (workspace / "run_state.json").write_text("{invalid", encoding="utf-8")

            result = self.validate(workspace)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Invalid run_state.json", result.stdout)

    def test_valid_run_state_json_is_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.make_workspace(Path(tmp), mode="deep")
            state_path = workspace / "run_state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["mode"], "deep")
            self.assertFalse(state["recall_started"])

    def test_completeness_flags_template_workspace_as_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.make_workspace(Path(tmp), mode="deep")

            result = assess_analysis_completeness(workspace)

            self.assertFalse(result.complete)
            self.assertEqual(result.status, "analysis_incomplete")
            self.assertTrue(result.incomplete_files)

    def test_completeness_passes_filled_source_located_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.make_workspace(Path(tmp), mode="deep")
            filled = {
                "analysis/01_triage.md": "# Triage\n\n## Paper Problem\n\nA real problem. Source locator: Section 1.\n\n## Recommendation\n\ndeep. Source basis: Section 1.\n",
                "analysis/02_claim_ledger.md": "# Claim Ledger\n\n## Claim Table\n\n| ID | Claim | Claim Type | Source Locator | Direct Evidence | Support Level | Limitations / Counterpoints |\n|---|---|---|---|---|---|---|\n| C1 | The method improves transfer | Author claim | Section 4 | Table 2 reports gains | Partial | Benchmark only |\n",
                "analysis/03_contribution_map.md": "# Contribution Map\n\n## Core Sentence\n\nThe paper changes X to solve Y. Source locator: Section 3.\n\n## Counterfactual Sentence\n\nWithout X, the contribution is weaker. Source locator: Section 3.\n",
                "analysis/04_mechanism.md": "# Mechanism Model\n\n## Mermaid Causal Chain\n\n```mermaid\nflowchart TD\nA --> B\n```\n\nSource locator: Section 3.\n",
                "analysis/05_evidence_audit.md": "# Evidence Audit\n\n## Credibility Dimensions\n\n- Internal evidence credibility: moderate. Source locator: Table 2.\n- External reproducibility readiness: low. Source locator: Appendix A.\n- Engineering transfer credibility: uncertain. Source locator: Section 5.\n",
                "analysis/06_transfer_analysis.md": "# Transfer Analysis\n\n## Relevance Layers\n\n- Industrial deployment relevance: uncertain. Source basis: Profile plus Section 5.\n",
                "analysis/07_final_brief.md": "# Final Brief\n\n## One-Sentence Conclusion\n\nPromising but not deployment-ready. Source locator: Sections 4-5.\n\n## Recommendation\n\nDeep read only if transfer is relevant. Source basis: evidence audit.\n",
            }
            for relative, content in filled.items():
                (workspace / relative).write_text(content, encoding="utf-8")

            result = assess_analysis_completeness(workspace)

            self.assertTrue(result.complete)
            self.assertEqual(result.status, "deep_analysis_complete")


if __name__ == "__main__":
    unittest.main()
