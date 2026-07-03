# Paper Forge Workflow

## Screen

1. Create or detect the paper workspace.
2. Create `README_FOR_READING.md`.
3. Create `source/source_manifest.md`.
4. Load `~/.paper-forge/profile.md` if present.
5. Save `analysis/profile_snapshot.md` with analysis-relevant Profile content only.
6. Produce `analysis/01_triage.md` with source locators for major claims.
7. Recommend `deep`, `skip`, or `conditional`.
8. Tell the user to read the numbered Markdown files with VS Code, Codex file view, Obsidian, Typora, or another Markdown reader.

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
12. Tell the user that the main reading outputs are numbered Markdown files `01` through `07`, with `08` added after recall starts.
13. Offer Recall.

## Recall

1. Load the existing paper workspace.
2. Ask one question at a time.
3. Wait for the user's answer.
4. Identify missing causal links, evidence boundaries, and assumptions.
5. Ask for improvement before revealing the answer.
6. Reveal only when the user explicitly asks.
7. Append the exchange to `learning/08_recall_log.md`, including the source basis for the question and locators for any revealed answer.
8. Remind the user that `08_recall_log.md` is the numbered recall reading artifact.
