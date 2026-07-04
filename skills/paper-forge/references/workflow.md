# Paper Forge Workflow

## Core Reading Chain

PaperForge must build this chain:

```text
problem -> prior limitation -> intervention -> mechanism -> evidence -> limitation -> transfer hypothesis -> recall
```

Zotero and Obsidian are bridge layers. They must not replace `screen`, `deep`, or `recall`.

## Zotero To Obsidian Bridge

```text
paper website -> Zotero Connector -> Zotero Desktop -> PaperForge work package
-> PaperForge core workspace -> Obsidian numbered notes
```

Zotero is the source of truth for original PDFs, standard metadata, tags, collections, DOI, arXiv ID, and Zotero item keys. PaperForge must not directly manage Zotero `storage/` or `zotero.sqlite`.

The local CLI separates the bridge into explicit steps:

```bash
paperforge ingest-zotero
paperforge deep zotero:<key>
```

`deep` is the main user entry point. It creates or reuses the core workspace, runs structural validation, runs deterministic completeness checks, marks incomplete work honestly, and exports to Obsidian. It does not perform semantic paper analysis by itself; Codex must still fill the source-located deep artifacts.

`init-workspace` and `export-obsidian` remain developer/debug commands. `analyze` is a compatibility command that delegates to `deep` semantics and must not claim that semantic deep analysis is complete.

## Core Workspace Outputs

```text
README_FOR_READING.md
source/source_manifest.md
analysis/profile_snapshot.md
analysis/01_triage.md
analysis/02_claim_ledger.md
analysis/03_contribution_map.md
analysis/04_mechanism.md
analysis/05_evidence_audit.md
analysis/06_transfer_analysis.md
analysis/07_final_brief.md
learning/08_recall_log.md
run_state.json
```

## Obsidian Numbered Notes

```text
Papers/YYYY-MM-DD__Short_Title__StableKey/
  YYYY-MM-DD__Short_Title__StableKey.md
  00 - Source, Metadata, Profile Snapshot.md
  01 - Problem, Prior Limitation, Actual Contribution.md
  02 - Mechanism, Method, Causal Chain.md
  03 - Claims, Evidence, Limitations, Unproven Parts.md
  04 - Transfer Analysis, User Research Relevance, Project Ideas.md
  05 - Feynman Recall, Self-Explanation, Open Questions.md
  paperforge-manifest.json
  Attachments/
```

Mapping:

```text
00 - Source, Metadata, Profile Snapshot.md
01 - Problem, Prior Limitation, Actual Contribution.md
02 - Mechanism, Method, Causal Chain.md
03 - Claims, Evidence, Limitations, Unproven Parts.md
04 - Transfer Analysis, User Research Relevance, Project Ideas.md
05 - Feynman Recall, Self-Explanation, Open Questions.md
```

Generated cross-paper links must use full Vault-relative paths. Do not generate ambiguous bare links such as `[[01]]` or per-paper `README.md` home files.

## Screen

1. Create or detect the paper workspace.
2. Create `README_FOR_READING.md`.
3. Create `source/source_manifest.md`.
4. Load `~/.paper-forge/profile.md` if present.
5. Save `analysis/profile_snapshot.md`.
6. Produce `analysis/01_triage.md` with source locators for major claims.
7. Recommend `deep`, `skip`, or `conditional`.

## Deep

1. Preflight source access and record limitations.
2. Load Profile and select output language.
3. Route the paper type.
4. Reuse or create triage.
5. Build the Claim Ledger.
6. Build the Contribution Map.
7. Build the Mechanism Model and Mermaid diagram.
8. Run the Evidence Audit.
9. Run Transfer Analysis using the Profile when present.
10. Write the Final Brief.
11. Run structural validation.
12. Offer Recall.

## Recall

1. Load the existing paper workspace.
2. Ask one question at a time.
3. Wait for the user's answer.
4. Identify missing causal links, evidence boundaries, and assumptions.
5. Ask for improvement before revealing the answer.
6. Reveal only when the user explicitly asks.
7. Append the exchange to `learning/08_recall_log.md`.
