# Output Contract

Obsidian archive outputs for Zotero -> PaperForge -> Obsidian flows:

```text
Papers/<folder>/
  <folder>.md
  00 - Source, Metadata, Profile Snapshot.md
  01 - Problem, Prior Limitation, Actual Contribution.md
  02 - Mechanism, Method, Causal Chain.md
  03 - Claims, Evidence, Limitations, Unproven Parts.md
  04 - Transfer Analysis, User Research Relevance, Project Ideas.md
  05 - Feynman Recall, Self-Explanation, Open Questions.md
  paperforge-manifest.json
  Attachments/
```

The archive folder and home note use:

```text
YYYY-MM-DD__Short_Title__StableKey
```

Stable key priority:

```text
Zotero Item Key -> DOI -> arXiv ID -> title + authors + year hash
```

Numbered reading documents:

- `00 - Source, Metadata, Profile Snapshot.md`
- `01 - Problem, Prior Limitation, Actual Contribution.md`
- `02 - Mechanism, Method, Causal Chain.md`
- `03 - Claims, Evidence, Limitations, Unproven Parts.md`
- `04 - Transfer Analysis, User Research Relevance, Project Ideas.md`
- `05 - Feynman Recall, Self-Explanation, Open Questions.md`

`paperforge-manifest.json` must record `paper_id`, `id_strategy`, `zotero_item_key`, `folder_name`, `source_pdf_hash`, `metadata_hash`, `analysis_version`, `created_at`, `updated_at`, `status`, and `pdf_status`.

Valid archive status values include:

- `metadata_only`: PDF unavailable; do not claim full-text analysis.
- `analysis_pending`: core workspace exists but has not been checked as complete.
- `analysis_incomplete`: core workspace exists, but required deep artifacts still look like templates or lack source-located evidence.
- `exported_from_deep_analysis`: deep artifacts passed deterministic completeness checks.

Completeness checks are structural and evidence-discipline checks only. They do not prove semantic correctness.

Generated cross-paper links must be full Vault-relative links, for example:

```text
[[Papers/2026-07-04__Example_Paper__EXAMPLE123/01 - Problem, Prior Limitation, Actual Contribution|01 - Problem, Prior Limitation, Actual Contribution]]
```

Do not generate ambiguous bare links such as `[[01]]`, and do not create per-paper `README.md` home files.

If a paper archive already contains legacy bare filenames such as `00.md` through `05.md`, PaperForge must skip automatic migration by default and warn the user instead of silently renaming or overwriting notes.

Author names imported from Zotero Local API must preserve Unicode through metadata JSON, workspace artifacts, and Obsidian Markdown. Explicit UTF-8 I/O is required; mojibake repair is allowed only for clearly suspicious strings and must not rewrite already-correct Unicode names.

Required deep outputs:

- `README_FOR_READING.md`
- `source/source_manifest.md`
- `analysis/profile_snapshot.md`
- `analysis/01_triage.md`
- `analysis/02_claim_ledger.md`
- `analysis/03_contribution_map.md`
- `analysis/04_mechanism.md`
- `analysis/05_evidence_audit.md`
- `analysis/06_transfer_analysis.md`
- `analysis/07_final_brief.md`

Recall output after recall starts:

- `learning/08_recall_log.md`

Primary reading outputs are the numbered Markdown files:

- `analysis/01_triage.md`
- `analysis/02_claim_ledger.md`
- `analysis/03_contribution_map.md`
- `analysis/04_mechanism.md`
- `analysis/05_evidence_audit.md`
- `analysis/06_transfer_analysis.md`
- `analysis/07_final_brief.md`
- `learning/08_recall_log.md`

`README_FOR_READING.md` must explain how to open the Markdown files and which numbered files to read first.

Claim Ledger table header:

```text
| ID | Claim | Claim Type | Source Locator | Direct Evidence | Support Level | Limitations / Counterpoints |
```

Mechanism must contain a fenced Mermaid block and a basic `flowchart TD` declaration.

Evidence Audit must include:

- Internal evidence credibility
- External reproducibility readiness
- Engineering transfer credibility

Final Brief should include:

- One-sentence conclusion
- Problem
- Real technical increment
- Strongest evidence
- Most important evidence gaps
- Three credibility dimensions
- Transfer value for the user
- Recommendation

Source locator requirements:

- Every numbered output file must include `Source locator` or a source-basis equivalent.
- Exact page, figure, table, and experiment identifiers are preferred when available.
- If exact pages are unavailable, write `PDF page Unknown` and provide the best available section/table/figure/URL locator.
- If no locator exists, write `Source locator: Unknown` and explain what source material is missing.
