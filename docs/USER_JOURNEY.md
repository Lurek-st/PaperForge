# User Journey / 用户路径

## Overview / 概览

PaperForge is designed for a real reading loop, not a one-click "paper solved" promise.

```text
Save paper in Zotero
-> initialize PaperForge workspace
-> run deep reading with Codex / Agent
-> export structured notes to Obsidian
-> extend with your own links, ideas, and experiments
```

## 1. Prepare your tools / 准备工具

Required:

- Zotero Desktop
- Obsidian
- Python environment for PaperForge
- Codex / Agent environment for the deep workflow

Optional:

- Zotero Connector
- Git or GitHub Desktop
- VS Code

## 2. Configure your local data locations / 配置本地目录

Keep these separate:

```text
<project-root>                     source code
<your-paperforge-data-directory>   local PaperForge workspace + profile
<your-zotero-data-directory>       Zotero data
<your-obsidian-vault>              Obsidian vault
```

Do not place private PDFs, analysis outputs, or your real `profile.md` inside the repository.

## 3. Create your Research Profile / 创建 Research Profile

Copy [`profile.example.md`](../profile.example.md) to:

```text
~/.paper-forge/profile.md
```

Then edit:

- research identity
- research interests
- priority questions
- application context
- output language and detail preferences

## 4. Check the environment / 环境检查

```bash
python skills/paper-forge/scripts/paperforge.py init
python skills/paper-forge/scripts/paperforge.py doctor
```

You should see guidance about:

- Zotero as the metadata and PDF source
- PaperForge as the analysis workspace
- Obsidian as the long-term export target
- local configuration and safety boundaries

## 5. Ingest metadata / 导入元数据

Example:

```bash
python skills/paper-forge/scripts/paperforge.py ingest-zotero
```

Or ingest one anonymized example item:

```bash
python skills/paper-forge/scripts/paperforge.py ingest-zotero --metadata example-metadata.json
```

If the paper has no usable PDF, PaperForge records a `metadata_only` state instead of fabricating a full-text assessment.

## 6. Initialize the workspace / 初始化工作区

```bash
python skills/paper-forge/scripts/paperforge.py init-workspace zotero:EXAMPLE123
```

This prepares the core analysis files under `processing/` for that paper.

## 7. Run the deep workflow / 执行 deep 工作流

```bash
python skills/paper-forge/scripts/paperforge.py deep zotero:EXAMPLE123
```

If the deep artifacts are still placeholders, PaperForge will report `analysis_incomplete`. That is expected until Codex / Agent fills the files with source-located content.

## 8. Ask Codex / Agent to read deeply / 让 Codex 深读

Example prompt:

```text
使用 PaperForge deep 工作流分析 zotero:EXAMPLE123。
读取 PDF 与工作区模板，填写 analysis/*.md。
所有关键判断必须标注来源位置；无法确认的内容明确写 Unknown。
```

## 9. Re-run export to Obsidian / 重新导出到 Obsidian

```bash
python skills/paper-forge/scripts/paperforge.py export-obsidian zotero:EXAMPLE123 --obsidian-language zh
```

Result:

```text
<your-obsidian-vault>/Papers/<paper-folder>/
├── <paper-folder>.md
├── 00 - ...
├── 01 - ...
├── 02 - ...
├── 03 - ...
├── 04 - ...
└── 05 - ...
```

Recommended reading order:

```text
Home -> 01 -> 02 -> 03 -> 04 -> 05
Read 00 when you need metadata, source links, or profile context.
```

## 10. Continue personal knowledge work / 继续沉淀个人知识

Inside Obsidian you can:

- add links to project notes
- add your own experiment ideas
- write reflections and contradictions
- move the whole paper folder inside the vault

If you move folders inside Obsidian, rebuild the index when needed:

```bash
python skills/paper-forge/scripts/paperforge.py reindex
python skills/paper-forge/scripts/paperforge.py repair-links
```

## What PaperForge will not do / PaperForge 不会做什么

- It will not auto-write Zotero tags in the current release.
- It will not modify Zotero's database or attachment storage.
- It will not overwrite existing Obsidian notes by default.
- It will not claim deep full-text understanding when the PDF is missing.
