# Profile Policy

The persistent Profile is local state, not model memory.

Default path:

```text
~/.paper-forge/profile.md
```

Rules:

- Read the Profile for `screen` and `deep` when it exists.
- Never silently modify it.
- Never store it inside the Skill package.
- Snapshot only analysis-relevant content into `analysis/profile_snapshot.md`.
- Before updating an existing Profile, create a timestamped backup.
- Ask only for research background, research directions, target applications, judging constraints, language preference, and low-priority topics.
- Do not request or store credentials, private keys, addresses, identity documents, or unrelated sensitive information.

Use `assets/profile-template.md` for manual setup and `assets/profile-industrial-embodied-ai-example.md` as an example only.
