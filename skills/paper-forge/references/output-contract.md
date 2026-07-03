# Output Contract

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
