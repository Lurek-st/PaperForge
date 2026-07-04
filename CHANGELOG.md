# Changelog / 更新日志

## 0.3.4 - Titled Obsidian Notes And Unicode-Safe Zotero Authors

中文：
- Obsidian 论文认知页面从裸 `00.md` 到 `05.md` 改为带主题名的编号文件，便于在左侧文件树中直接识别内容职责。
- 论文主页推荐阅读顺序、页面标题和页面间导航已同步到新的带标题文件名。
- 若检测到旧版 `00.md` 到 `05.md` 结构，默认只提示并跳过，不会静默迁移、重命名或覆盖用户笔记。
- Zotero Local API 仍然只读；作者名导入链路改为显式 UTF-8 / Unicode 安全处理，并仅对明显 mojibake 做保守恢复。
- 新增测试覆盖 Obsidian 文件命名、旧版结构保护、多语种作者名保持和典型 mojibake 恢复。

English:

- Obsidian reading notes now use titled numbered filenames instead of bare `00.md` through `05.md`.
- The home note reading order, page headings, and inter-note navigation now align with the titled filenames.
- Legacy `00.md` through `05.md` archives are detected and protected by default rather than silently migrated or overwritten.
- Zotero Local API remains read-only; author names now flow through explicit UTF-8 / Unicode-safe handling with conservative mojibake repair only for clearly suspicious strings.
- Added tests for titled Obsidian note names, legacy-layout protection, multilingual author preservation, and typical mojibake recovery.

## 0.3.3 - Export Gating, Calibrated Gaps, And Zotero Inbox Fallback

中文：

- `deep` 在存在 PDF 但分析仍为 `analysis_incomplete` 时，默认不再导出 Obsidian，避免未完成模板先污染阅读 Vault。
- 已完成的 deep 导出现在会自动刷新此前 incomplete 导出的旧生成笔记，并在覆盖前创建备份。
- 当 workspace 达到 `deep_analysis_complete` 后，Obsidian 编号笔记会隐藏顶部 scaffold，减少“占位模板”和“已填核心产物”混在一起的阅读干扰。
- 占位提示词改为更明确的证据边界标记：`paper_not_reported`、`not_verified_in_alpha`、`unavailable_without_repo_check`、`unknown_from_pdf_only`。
- 完整性检查不再依赖脆弱的精确短语 `Unknown. Source locator: Unknown`，而是对这些证据缺口标记做更稳健的判断。
- `ingest-zotero` 在没有 pending tag 条目时，会自动回退为扫描配置中的 Zotero Inbox collection，减少手工打标签需求。
- `ingest-zotero` 现在会默认跳过已经存在 PaperForge work package 或 analysis workspace 的论文，除非显式使用 `--force`。

English:

- `deep` now skips Obsidian export while a PDF-backed analysis workspace is still `analysis_incomplete`, preventing incomplete templates from polluting the reading Vault by default.
- Completed deep exports now automatically refresh stale generated notes from earlier incomplete exports, with backups created before replacement.
- Obsidian numbered notes hide scaffold sections after a workspace reaches `deep_analysis_complete`, reducing confusion between placeholders and filled core artifacts.
- Placeholder language now uses more calibrated gap markers such as `paper_not_reported`, `not_verified_in_alpha`, `unavailable_without_repo_check`, and `unknown_from_pdf_only`.
- Completeness checks now treat these calibrated gap markers more carefully and no longer rely on the brittle exact phrase `Unknown. Source locator: Unknown`.
- `ingest-zotero` now falls back to scanning the configured Zotero inbox collection when no pending-tag items are available, reducing the need for manual tagging.
- `ingest-zotero` also skips papers that already have an existing PaperForge package or analysis workspace unless `--force` is used.

## 0.3.2 - Deep Entry Point And Completeness Checks

中文：

- 新增 `deep` 主入口，用于创建或复用核心工作区、运行结构校验、运行完整性检查并导出 Obsidian。
- `deep` 会把仍是模板或缺少来源定位的工作区标记为 `analysis_incomplete`，不会伪装成已完成深度分析。
- 新增核心分析完整性检查，覆盖 `analysis/01_triage.md` 到 `analysis/07_final_brief.md`，并检查 Claim Ledger 来源定位与 Mermaid 机制链。
- `analyze` 调整为 `deep` 的兼容入口。
- 清理 CLI 和 Obsidian 生成模板中的乱码提示，改为稳定英文输出。
- 新增 `deep` CLI 测试和完整性检查测试。

English:

- Added `deep` as the main workflow entry point.
- Added completeness checks that distinguish filled source-located artifacts from placeholders.
- `deep` marks unfinished work as `analysis_incomplete` and exports that status honestly.
- `analyze` now delegates to the `deep` semantics as a compatibility command.

## 0.3.1 - Core Workflow Alignment

中文：

- 新增 `init-workspace` 命令，用于从 Zotero/PaperForge 工作包创建核心 `screen` / `deep` / `recall` 分析工作区。
- 新增 `export-obsidian` 命令，用于把核心分析工作区导出为 Obsidian `00.md` 到 `05.md` 编号文书。
- 保留 `analyze` 兼容命令，但明确提示它不会自动完成深度语义论文分析。
- 修复 CLI 与主要生成文书中的中文乱码。
- 将 Obsidian 编号文书重新映射到 PaperForge 原始认知链：问题与贡献、机制、证据、迁移、费曼回忆。
- Obsidian 导出现在可以导入核心工作区产物，例如 `analysis/02_claim_ledger.md` 和 `analysis/05_evidence_audit.md`。
- 更新 README、用户旅程、工作流、Obsidian 结构和核心能力审查文档。
- 新增 CLI 级别测试，覆盖 `init-workspace`、`export-obsidian` 和 `analyze` 兼容提示。

English:

- Added `init-workspace` for creating the core PaperForge analysis workspace.
- Added `export-obsidian` for exporting core artifacts into Obsidian numbered notes.
- Kept `analyze` as a compatibility command while explicitly warning that it does not perform semantic deep analysis by itself.
- Re-mapped Obsidian `00.md` through `05.md` to the original PaperForge cognitive chain.
- Added tests for the new CLI flow and core artifact import.

## 0.3.0 - Zotero To Obsidian Archive Workflow

中文：

- 明确 PaperForge 的 `Zotero -> PaperForge -> Obsidian` 产品定位。
- 新增本地 CLI、默认配置、稳定 ID、Obsidian 每论文独立文档包、PDF 缺失提示、用户内容保护、重复导入幂等、重新索引和裸链接检测。
- 将 Obsidian 默认输出从编号文件夹调整为 `00.md` 到 `05.md` 编号文书。
- 新增核心能力对齐审查，明确 Zotero/Obsidian 只是输入输出桥接层，不能替代 `screen` / `deep` / `recall`。

English:

- Defined PaperForge as a Zotero -> PaperForge -> Obsidian workflow.
- Added local CLI, default config, stable IDs, one archive package per paper, missing-PDF behavior, user-content protection, idempotent imports, reindexing, and bare-link detection.
- Changed Obsidian output from numbered folders to numbered Markdown documents.

## 0.2.1 - Source-Located Reading And Reading Entry Point

中文：

- 为编号 Markdown 产物新增 `Source locator` / `Source basis` 要求。
- 新增工作区入口 `README_FOR_READING.md`。
- `init_workspace.py` 会打印阅读指引。
- 结构校验新增对编号来源定位脚手架和阅读入口的检查。

English:

- Added `Source locator` / `Source basis` requirements for numbered Markdown artifacts.
- Added workspace entry point `README_FOR_READING.md`.
- `init_workspace.py` prints reading guidance.
- Structural validation checks numbered source locator scaffolding and the reading entry point.

## 0.2.0 - Initial Implementation

中文：

- 创建单一 `paper-forge` Skill。
- 增加 `screen`、`deep` 和 `recall` 模式。
- 增加默认路径为 `~/.paper-forge/profile.md` 的持久 Profile 策略。
- 增加本地工作区模板和结构校验。
- 增加标准库 Python 脚本：`init_profile.py`、`init_workspace.py` 和 `validate_run.py`。

English:

- Created the single `paper-forge` Skill.
- Added `screen`, `deep`, and `recall` modes.
- Added persistent Profile policy with default path `~/.paper-forge/profile.md`.
- Added local workspace templates and structural validation.
- Added standard-library Python scripts: `init_profile.py`, `init_workspace.py`, and `validate_run.py`.
