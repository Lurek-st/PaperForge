# Contributing to PaperForge

Thanks for your interest in PaperForge. Contributions, bug reports, documentation fixes, and reproducible test cases are welcome.

PaperForge is a **reading tool**, not a truth engine. The goal is to keep claims, evidence, limitations, source locations, and transfer judgments explicit and traceable. Contributions should preserve these properties.

## Especially welcome

- installation fixes
- Zotero compatibility reports
- Obsidian export issues
- source-locator and evidence-traceability improvements
- cross-platform verification (especially Windows / macOS / Linux)
- reproducible bug reports
- tests
- documentation

## Pull request principles

- **Keep changes scoped.** Do not mix unrelated refactors, dependency upgrades, or formatting changes into a behavior change.
- **Preserve data safety.** Do not introduce anything that auto-uploads user PDFs, workspace, Obsidian notes, or Profile to GitHub or to any remote service.
- **Preserve Zotero read-only behavior.** Do not write to Zotero `storage/`, `zotero.sqlite`, or auto-write tags to Zotero items.
- **Preserve evidence boundaries.** Do not weaken source-locator requirements, prompt-injection protections, or the claim/evidence separation.
- **Add or update tests when behavior changes.** A behavior change without test coverage should be justified in the PR description.
- **Do not modify tests to make them pass.** If a test is wrong, fix the contract it is testing, not the assertion. If a behavior is intentional, update the test to reflect the new contract and explain why in the PR description.
- **Do not claim unverified platform support.** Windows is currently verified. macOS / Linux are expected to work but have not been fully verified by the maintainer; do not promote them to "supported" without attached evidence.
- **Do not promise that the Agent is correct.** PaperForge treats the Agent's output as a structured reading artifact, not a fact verdict.

## Reporting bugs

When filing a bug report, please include:

- OS and version
- Python version (`python --version`)
- Zotero version (when the issue involves Zotero integration)
- the exact PaperForge command you ran
- expected behavior
- actual behavior
- sanitized logs (no private PDF paths, no Zotero item keys tied to private databases)
- minimal reproduction steps

**Do not include** in the bug report:

- private PDFs
- API keys, tokens, or credentials
- personal Zotero database files
- your real `~/.paper-forge/profile.md`
- your real Obsidian Vault output

## Requesting features

When proposing a feature, please describe:

- the **problem first** — what user pain or workflow gap does it address
- the **use case** — a concrete scenario where the feature helps
- the **current workaround** — how you handle it today
- the **proposed behavior**
- the **impact on evidence traceability and local-first constraints** — does it keep PaperForge local-first? does it keep source locators and claim/evidence separation?

## Repository conventions

- The canonical Skill lives in `skills/paper-forge/`.
- Use the Python standard library where reasonable.
- Do not create Plugins, MCP servers, Hooks, browser automation, cloud services, or multi-agent workflows inside the repo.
- Do not commit user Profile, user workspace, Obsidian Vault output, or private PDFs.
- Update `CHANGELOG.md` when behavior changes.

## License of contributions

By contributing, you agree that your contributions are licensed under the MIT License of this repository.
