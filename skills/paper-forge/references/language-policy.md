# Language Policy

Default analysis language is `auto`.

Priority:

1. Explicit per-run user request.
2. Persistent Profile preference.
3. Detected primary paper language.
4. English fallback.

Allowed user requests:

- English
- Chinese
- Bilingual Chinese-English

In bilingual mode:

- Present major conclusions in Chinese followed by English.
- Make recall questions bilingual.
- Preserve source quotations in the paper's original language.
- Keep file names English.

If source language is unclear, fall back to English and disclose the uncertainty.
