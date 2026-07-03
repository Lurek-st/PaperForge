# Source And Citation Policy

Every strong conclusion, mechanism judgment, evidence judgment, limitation judgment, and transfer judgment should have a source locator when available.

Acceptable locators:

- Page number from a readable PDF.
- Section heading.
- Figure, table, or experiment ID.
- Appendix or supplementary section.
- DOI, arXiv ID, URL, or landing page with access limitation.

Preferred format:

```text
Source locator: PDF p. 7; Section 6.2; Table 2.
Source locator: PDF page Unknown; ar5iv Section 6.4; Table 6.
Source locator: Unknown; full PDF unavailable, only abstract page inspected.
```

Never fabricate page numbers, figure IDs, table IDs, experiment IDs, quotations, or source locations.

If a source is incomplete:

- State exactly what is available.
- Restrict analysis to available material.
- Mark missing facts as `Unknown`.
- Record limitations in `source/source_manifest.md`.
- Use `PDF page Unknown` when exact PDF pages are unavailable.

Do not treat author claims as facts. Use wording such as:

```text
The paper claims...
The direct evidence covers...
The stronger external-validity conclusion remains Unknown.
```

Minimum locator density:

- `01_triage.md`: each major section has at least one source locator or explicit `Unknown`.
- `02_claim_ledger.md`: every claim row must include a `Source Locator` value.
- `03_contribution_map.md`: core sentence, counterfactual sentence, and causal chain must have locators.
- `04_mechanism.md`: key inputs, modules, outputs, and failure conditions must have locators or `Unknown`.
- `05_evidence_audit.md`: each credibility judgment must point to a supporting section, table, experiment, or `Unknown`.
- `06_transfer_analysis.md`: distinguish paper-supported evidence from Profile-based inference.
- `07_final_brief.md`: conclusion, strongest evidence, and evidence gaps must have locators.
- `08_recall_log.md`: questions must record their source basis; revealed answers must include locators.
