# Troubleshooting

## Zotero Desktop Is Not Detected

Symptoms:

- `doctor` reports that Zotero Desktop Local API is not reachable

Check:

1. Start Zotero Desktop.
2. Confirm the target paper exists in Zotero.
3. Rerun:

```bash
python skills/paper-forge/scripts/paperforge.py doctor
```

## Metadata Exists But PDF Is Missing

Symptoms:

- Output becomes `metadata_only`
- PaperForge refuses to claim full-text evidence review

Meaning:

- PaperForge found metadata, but no accessible PDF was available

Check:

1. Confirm the Zotero item has a real PDF attachment.
2. If needed, provide a PDF manually during ingestion.
3. Re-run `ingest-zotero`, then `deep` or `export-obsidian`.

## Obsidian Archive Did Not Export

Common reasons:

- `deep` determined the workspace is still `analysis_incomplete`
- `obsidian.vault_path` is wrong
- Existing notes were protected by the overwrite guard

Check:

```bash
python skills/paper-forge/scripts/paperforge.py status
```

## Existing Notes Were Not Overwritten

This is expected by default.

PaperForge protects:

- user-edited notes
- legacy `00.md` through `05.md` layouts
- existing titled notes in a different language mode

If you intentionally want regeneration, review the archive and use `--force` carefully.

## Language Switch Did Not Produce New Notes

PaperForge skips export when a paper archive already contains titled notes in another language mode.

Why:

- This avoids silently creating duplicate note sets such as one Chinese set plus one English set in the same folder

What to do:

- export to a separate Vault or folder
- or migrate/archive the old set manually before re-exporting

## Bare Obsidian Links Look Broken

Run:

```bash
python skills/paper-forge/scripts/paperforge.py reindex
python skills/paper-forge/scripts/paperforge.py repair-links
```

`repair-links` reports risky bare links such as `[[01]]`.

## Author Names Look Garbled

Current behavior:

- PaperForge keeps normal Unicode names unchanged
- It only attempts mojibake repair for clearly suspicious strings
- If it cannot repair a suspicious name safely, it preserves the original value and emits a warning

If you find a reproducible issue, capture the smallest possible metadata example and open an Issue.

## Local Data Safety

Do not keep these inside the repository if you plan to publish or sync code:

- user PDFs
- Zotero database copies
- generated Obsidian Vault data
- `profile.md`
- `.env`
- runtime logs and caches

The repository `.gitignore` is designed to block these by default, but you should still keep user data outside the source tree whenever possible.
