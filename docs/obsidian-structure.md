# Obsidian Structure

## Archive Layout

Each paper exports into its own archive folder:

```text
<your-obsidian-vault>/
└── Papers/
    └── YYYY-MM-DD__Short_Title__StableKey/
        ├── YYYY-MM-DD__Short_Title__StableKey.md
        ├── 00 - Source, Metadata, Profile Snapshot.md
        ├── 01 - Problem, Prior Limitation, Actual Contribution.md
        ├── 02 - Mechanism, Method, Causal Chain.md
        ├── 03 - Claims, Evidence, Limitations, Unproven Parts.md
        ├── 04 - Transfer Analysis, User Research Relevance, Project Ideas.md
        ├── 05 - Feynman Recall, Self-Explanation, Open Questions.md
        ├── paperforge-manifest.json
        └── Attachments/
```

The note language can be `zh`, `en`, `bilingual`, or `auto`. The examples above show the English mode.

## Reading Order

Recommended reading order:

```text
home
-> 01
-> 02
-> 03
-> 04
-> 05
read 00 when you need source metadata, Zotero links, or traceability details
```

## Note Responsibilities

| Note | Purpose |
|---|---|
| `00` | source, metadata, Zotero jump, Profile snapshot |
| `01` | paper positioning, prior limitation, actual contribution |
| `02` | mechanism, method, inputs, outputs, causal chain |
| `03` | claims, evidence, limitations, unproven parts |
| `04` | transfer analysis, user relevance, project ideas |
| `05` | Feynman recall, self-explanation, open questions |

## Link Rules

Generated links must use full Vault-relative paths.

Good:

```text
[[Papers/2026-07-04__Example_Paper__EXAMPLE123/01 - Problem, Prior Limitation, Actual Contribution|01 - Problem, Prior Limitation, Actual Contribution]]
```

Avoid:

```text
[[01]]
[[README]]
```

## Existing Notes Protection

- Existing Obsidian notes are not overwritten by default.
- Legacy bare note layouts such as `00.md` through `05.md` are detected and protected.
- If existing titled notes appear to use a different title language, export is skipped instead of silently creating duplicates.

## Movement Rule

- Prefer moving or renaming generated notes inside Obsidian so links can be maintained.
- Archive a paper by moving the whole paper folder instead of scattering internal files.
- After moving archives, run:

```bash
python skills/paper-forge/scripts/paperforge.py reindex
python skills/paper-forge/scripts/paperforge.py repair-links
```
