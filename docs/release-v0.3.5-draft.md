# PaperForge v0.3.5 — Draft Release Notes

> **Status: draft. Not yet a published GitHub Release. This file is the source-of-truth description for the upcoming v0.3.5 release and is subject to change before any tag is created.**

## What PaperForge is

PaperForge is a local-first Zotero → AI Agent → Obsidian workflow for traceable academic paper reading, structured evidence review, and long-term research knowledge management.

It is not a generic paper summarizer. It builds a controlled reading workspace where claims, evidence, limitations, source locations, transfer hypotheses, and recall are kept explicit.

## Highlights

1. **Zotero → PaperForge → AI Agent → Obsidian workflow.** The local-first pipeline keeps Zotero as the source of truth for PDFs and standard metadata, PaperForge as the controlled work-package and analysis orchestrator, and Obsidian as the long-term knowledge network.
2. **Source-located, evidence-aware reading.** Every numbered Markdown artifact carries a `Source locator` or an explicit `Unknown`; claims, evidence, limitations, and PaperForge judgment stay separated instead of being merged into a single summary.
3. **`deep` entry point, completeness checks, and export gating.** The `deep` command creates or reuses the analysis workspace, validates structure, runs completeness checks, and exports to Obsidian only when the analysis is genuinely filled.
4. **Titled Obsidian reading notes.** Numbered notes use titled filenames such as `01 - Problem, Prior Limitation, Actual Contribution.md`, with legacy `00.md`–`05.md` layouts detected and protected rather than overwritten.
5. **Unicode-safe Zotero author handling.** Author names flow through explicit UTF-8 / Unicode-safe processing with conservative mojibake repair only for clearly suspicious strings.
6. **Windows non-UTF-8 CLI robustness.** Chinese output no longer crashes with `UnicodeEncodeError` when stdout/stderr use a non-UTF-8 pipe encoding (e.g. Windows cp1252); unencodable characters degrade safely via backslash escaping without forcing a different stream encoding.
7. **Bilingual README and public discovery infrastructure.** English canonical README, independent Simplified Chinese README, hero and social-preview assets, GitHub topics, repository description, and Discussions.
8. **MIT License.** PaperForge is now explicitly open source under the MIT License, with contribution guidance and issue templates.
9. **CI matrix.** GitHub Actions runs the full test suite on Windows / Ubuntu × Python 3.9 / 3.14.

## Verified

- **Windows** — maintainer workflow verified.
- **GitHub Actions matrix:**
  - Ubuntu / Python 3.9 — PASS
  - Ubuntu / Python 3.14 — PASS
  - Windows / Python 3.9 — PASS
  - Windows / Python 3.14 — PASS
- **53 tests in each CI matrix job** (`python -m unittest discover -s tests -p "test_*.py"`, 0 failures, 0 errors).

Boundary: CI proves that the automated test suite passes on these runners. It does **not** equal full Zotero Desktop + Obsidian end-to-end verification on Linux/macOS, which still requires manual validation on the user's own machine.

## Current limitations

These limitations are intentional and should be read before adopting PaperForge for any high-stakes workflow:

- **macOS / Linux have not yet been fully verified by the maintainer.** They are expected to work because the project is pure standard-library Python, but they should be validated on the user's own machine before relying on PaperForge in a real workflow.
- **The Agent's analysis is not automatically evidence.** PaperForge treats the Agent's draft the same way it treats a paper: a structured reading artifact. The user is expected to verify important claims against the original PDF.
- **PaperForge does not guarantee correctness of paper conclusions.** Source-locator scaffolding helps the user return to the paper, but does not by itself prove that a citation, page number, or interpretation is correct. Structural validation is not semantic validation.
- **PaperForge does not replace expert peer review.** It is a reading aid, not a peer review engine, not a fact-checking engine, and not a replacement for reading the paper.
- **The PDF is the source of truth.** When the PDF is missing, the run degrades to `metadata_only` and PaperForge will not fabricate full-text conclusions.
- **Local-first only.** There is no built-in cloud sync, no built-in team sharing, and no auto-upload path. Users are responsible for backing up their own workspace, Profile, and Vault.

## Install

PaperForge is a local Python Skill with no third-party runtime dependencies.

```bash
git clone https://github.com/Lurek-st/PaperForge.git
cd PaperForge
python skills/paper-forge/scripts/paperforge.py doctor
python skills/paper-forge/scripts/paperforge.py init
python skills/paper-forge/scripts/paperforge.py ingest-zotero
```

`ingest-zotero` prints the real `paper_id` for each imported item (for example `paper_id: zotero:<key>`). Copy that actual ID and run:

```bash
python skills/paper-forge/scripts/paperforge.py deep <paper_id>
```

For the full setup walkthrough, see the [README](../README.md) (English) or [README.zh-CN.md](../README.zh-CN.md) (简体中文).

## License

PaperForge is released under the MIT License. See [LICENSE](../LICENSE).
