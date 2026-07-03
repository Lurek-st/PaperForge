# Reading Guide

## Numbered Markdown Files

Paper Forge outputs are Markdown reading artifacts, not a web UI.

For normal reading, focus on the numbered files:

```text
analysis/01_triage.md
analysis/02_claim_ledger.md
analysis/03_contribution_map.md
analysis/04_mechanism.md
analysis/05_evidence_audit.md
analysis/06_transfer_analysis.md
analysis/07_final_brief.md
learning/08_recall_log.md
```

## How To Open

Open these files with VS Code, Codex file view, Obsidian, Typora, or any Markdown reader.

## Recommended Order

1. Read `analysis/07_final_brief.md` for the shortest calibrated judgment.
2. Read `analysis/01_triage.md` to decide whether the paper deserves more time.
3. Read `analysis/02_claim_ledger.md` to separate author claims from evidence.
4. Read `analysis/03_contribution_map.md` to understand the real contribution.
5. Read `analysis/04_mechanism.md` for the causal mechanism and Mermaid diagram.
6. Read `analysis/05_evidence_audit.md` to judge evidence strength.
7. Read `analysis/06_transfer_analysis.md` for your Profile-specific transfer value.
8. Read `learning/08_recall_log.md` after recall starts.

## Source Locators

Each numbered file should include source locators such as:

```text
Source locator: PDF p. 7; Section 6.2; Table 2.
Source locator: PDF page Unknown; ar5iv Section 6.4; Table 6.
Source locator: Unknown; full PDF unavailable.
```

Do not treat missing page numbers as a minor issue. `Unknown` means the source material did not support a precise locator.

## Support Files

Non-numbered files are mainly for traceability:

- `source/source_manifest.md`: what source material was available.
- `analysis/profile_snapshot.md`: which Profile priorities were used.
- `run_state.json`: script state for structural validation.
