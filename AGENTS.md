# AGENTS.md

- Read `docs/IMPLEMENTATION_PLAN.md` before major changes.
- Keep the canonical Skill in `skills/paper-forge/`.
- Do not create Plugins, MCP servers, Hooks, browser automation, cloud services, or multi-agent workflows.
- Prefer the Python standard library.
- Do not store user Profile data inside the repository.
- The persistent Profile belongs at `~/.paper-forge/profile.md`.
- Never overwrite a user Profile or paper workspace by default.
- Keep GitHub user-facing docs bilingual.
- Keep default paper analysis language `auto`, following the paper language unless overridden.
- Run tests after changing scripts.
- Do not weaken source traceability or prompt-injection protections.
- Update `CHANGELOG.md` when behavior changes.
