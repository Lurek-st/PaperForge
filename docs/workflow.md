# Workflow

## End-To-End Flow

```text
paper website
-> Zotero Connector
-> Zotero Desktop
-> PaperForge work package
-> PaperForge core workspace
-> Codex / Agent deep analysis
-> Obsidian paper archive
```

## Role Boundaries

- Zotero owns original PDFs and standard bibliographic metadata.
- PaperForge owns workspace initialization, structural validation, completeness checks, and Obsidian export.
- Codex / Agent fills the semantic deep-analysis artifacts.
- Obsidian is the long-term knowledge network, not the original PDF source of truth.

## Main User Entry Point

```bash
python skills/paper-forge/scripts/paperforge.py deep zotero:EXAMPLE123
```

What `deep` does:

- Creates or reuses the core workspace
- Runs structural validation
- Marks incomplete analysis honestly
- Exports to Obsidian only when safe to do so

What `deep` does not do by itself:

- It does not automatically perform semantic paper reading without Codex / Agent filling `analysis/*.md`

## Workspace Artifacts

Core workspace outputs:

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

## Obsidian Reading Notes

The long-term reading archive keeps the `00` to `05` ordering but now uses titled filenames.

English:

```text
00 - Source, Metadata, Profile Snapshot.md
01 - Problem, Prior Limitation, Actual Contribution.md
02 - Mechanism, Method, Causal Chain.md
03 - Claims, Evidence, Limitations, Unproven Parts.md
04 - Transfer Analysis, User Research Relevance, Project Ideas.md
05 - Feynman Recall, Self-Explanation, Open Questions.md
```

The actual filename language can be `zh`, `en`, `bilingual`, or `auto`, depending on CLI arguments, Profile, and config.

## Language Priority

```text
CLI explicit parameter
>
profile.md
>
config.yaml
>
auto fallback rule
```

## Safety Rules

- Zotero Local API is read-only in the current workflow.
- PaperForge must not move, rename, delete, or write Zotero `storage/` or `zotero.sqlite`.
- Existing Obsidian notes are protected by default.
- Legacy bare note layouts such as `00.md` through `05.md` are not auto-migrated.
- Switching note language does not silently create duplicate note sets.
