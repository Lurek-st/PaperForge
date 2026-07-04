# Architecture / 架构

## Overview / 概览

PaperForge is a local-first workflow:

```text
Zotero Desktop
-> PaperForge workspace
-> Codex / Agent deep reading
-> Obsidian knowledge archive
```

PaperForge is not a cloud service, not a Zotero database replacement, and not an Obsidian vault manager. Zotero remains the source of truth for PDFs and bibliographic metadata. PaperForge owns the structured analysis workspace. Obsidian is the long-term note network.

PaperForge 是本地优先的论文分析工作流，不是云服务，也不是 Zotero 数据库替代品。Zotero 负责 PDF 与标准元数据，PaperForge 负责结构化分析工作区，Obsidian 负责长期知识沉淀。

## Components / 核心组件

- `skills/paper-forge/`
  Canonical Skill, scripts, templates, and reference contracts.
- `~/.paper-forge/profile.md`
  User-owned research Profile. This is personal local data and should not be committed.
- `~/.paper-forge/config.yaml`
  Local configuration. Use [`paperforge-config.example.yaml`](../paperforge-config.example.yaml) as the starting template.
- `<your-paperforge-data-directory>/workspace/`
  User workspace root for `inbox`, `processing`, `cache`, `failed`, `archive`, and `logs`.
- `<your-obsidian-vault>/Papers/`
  Long-term Obsidian export destination.

## Data Boundaries / 数据边界

- Zotero Local API is a read-only input chain in PaperForge's current design.
- PaperForge must not write to `zotero.sqlite` or modify Zotero-managed `storage/`.
- PaperForge should not assume user data lives inside the repository.
- The repository should contain code, templates, tests, and anonymized examples only.
- PDF missing means `metadata_only`; PaperForge must not invent full-text conclusions.
- Existing Obsidian notes are protected by default and should not be silently renamed or overwritten.

## Workspace Layers / 工作区分层

### 1. Zotero layer

- Stores the original PDF, citation data, creator list, DOI, URL, and other source metadata.
- Owns attachment storage and collection organization.

### 2. PaperForge workspace layer

Typical structure:

```text
<your-paperforge-data-directory>/workspace/
├── inbox/
├── processing/
├── cache/
├── failed/
├── archive/
└── logs/
```

Each paper workspace holds the source manifest, profile snapshot, and the deep-reading artifact chain:

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
```

### 3. Obsidian layer

Typical archive structure:

```text
<your-obsidian-vault>/Papers/<paper-folder>/
├── <paper-folder>.md
├── 00 - ...
├── 01 - ...
├── 02 - ...
├── 03 - ...
├── 04 - ...
├── 05 - ...
├── paperforge-manifest.json
└── Attachments/
```

The numbered notes mirror PaperForge's reasoning chain. The home note, numbered filenames, page titles, and navigation text should stay semantically aligned.

## Language Handling / 语言处理

PaperForge supports `zh`, `en`, `bilingual`, and `auto`.

Priority:

```text
CLI explicit arguments
> profile.md preferences
> config.yaml defaults
> auto fallback
```

Current language settings affect:

- Obsidian numbered filenames
- Obsidian page headings
- Home note navigation labels
- Workspace guidance recorded for deep analysis

## Safety Model / 安全策略

- Preserve normal Unicode author names end to end.
- Use explicit UTF-8 for file I/O and local config/profile parsing.
- Never auto-migrate legacy `00.md` to `05.md` archives without user action.
- Never upload user PDFs, private vault notes, or personal Profile data by default.
