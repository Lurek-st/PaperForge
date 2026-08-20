# PaperForge v0.3.4 — Draft Release Notes

> **Status: draft. Not yet a published GitHub Release. This file is the source-of-truth description for the upcoming v0.3.4 release and is subject to change before any tag is created.**

## What PaperForge is

PaperForge is a local-first Zotero → AI Agent → Obsidian workflow for traceable academic paper reading, structured evidence review, and long-term research knowledge management.

It is not a generic paper summarizer. It builds a controlled reading workspace where claims, evidence, limitations, source locations, transfer hypotheses, and recall are kept explicit.

## Highlights since v0.3.0

Summarized from the [CHANGELOG](../CHANGELOG.md).

- **Defined Zotero → PaperForge → Obsidian product positioning.** The workflow, configuration model, and Obsidian output conventions are now anchored to a single mental model.
- **Local-first CLI, default config, stable IDs, per-paper archive package.** Each paper gets an isolated archive folder in the Obsidian Vault; workspace state is local; nothing is uploaded to GitHub.
- **One Markdown file per numbered slot instead of folders.** Obsidian output moved from numbered folders to numbered `00.md`–`05.md` documents that re-map cleanly to PaperForge's original cognitive chain.
- **Source-located reading.** Every numbered Markdown artifact now requires a `Source locator` or an explicit `Unknown`. Reading is anchored back to the PDF, not to the model.
- **Workspace entry point `README_FOR_READING.md`.** Each paper workspace has a reading entry point that explains the numbered files in order.
- **`init-workspace` and `export-obsidian` commands.** Workspace initialization and Obsidian export are now first-class CLI operations, with `analyze` kept as a compatibility command that delegates to the new semantics.
- **Deep workflow entry point `deep`.** The `deep` command creates or reuses the workspace, runs structural validation and completeness checks, and exports to Obsidian when analysis is filled.
- **Completeness checks that distinguish filled source-located artifacts from placeholders.** A workspace whose numbered files are still templates is honestly marked `analysis_incomplete`; export is gated by default.
- **Export gating and protected Obsidian exports.** Incomplete analyses no longer pollute the reading Vault by default; completed exports refresh stale generated notes with backups first.
- **Calibrated gap markers.** Placeholder language uses markers such as `paper_not_reported`, `not_verified_in_alpha`, `unavailable_without_repo_check`, and `unknown_from_pdf_only` instead of brittle exact phrases.
- **Titled Obsidian reading notes.** Obsidian numbered notes use titled filenames such as `01 - Problem, Prior Limitation, Actual Contribution.md` so the file tree is readable at a glance; the home note, reading order, and inter-note navigation align with the new names.
- **Legacy layout protection.** Legacy `00.md`–`05.md` archives are detected and protected rather than silently migrated or overwritten.
- **Zotero inbox fallback.** `ingest-zotero` now scans the configured Zotero Inbox collection when no pending-tag items are available, and skips papers that already have a PaperForge package or analysis workspace unless `--force` is used.
- **Unicode-safe Zotero authors.** Author names flow through explicit UTF-8 / Unicode-safe handling, with conservative mojibake repair only for clearly suspicious strings.

## Verified

- **Windows** — verified by the maintainer.
- **Automated test suite.** As of this draft, `python -m unittest discover -s tests -p "test_*.py"` reports 52 tests, OK, with 0 failures and 0 errors.

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
```

For the full setup walkthrough, see the [README](../README.md) (English) or [README.zh-CN.md](../README.zh-CN.md) (简体中文).

## License

PaperForge is released under the MIT License. See [LICENSE](../LICENSE).
