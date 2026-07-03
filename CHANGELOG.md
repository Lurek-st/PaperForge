# 更新日志 / Changelog

## 中文

## 0.2.1 - 可定位阅读与阅读入口

- 为编号 Markdown 产物增加 `Source locator` / `Source basis` 要求。
- 新增工作区入口 `README_FOR_READING.md`，说明用户应主要阅读 `01` 到 `08` 的编号 Markdown 文件。
- `init_workspace.py` 结束时输出阅读指引，推荐 VS Code、Codex 文件视图、Obsidian、Typora 或其他 Markdown 阅读器。
- 结构验证新增编号文件 source locator 检查和阅读入口检查。
- 增加 `docs/READING_OUTPUTS.md`。

## 0.2.0 - 初始实现

- 创建单一 `paper-forge` Skill。
- 添加 `screen`、`deep`、`recall` 三种论文阅读模式的工作流指令。
- 添加长期 Profile 策略，默认路径为 `~/.paper-forge/profile.md`。
- 添加本地论文工作区模板、来源清单、主张账本、贡献图谱、机制图、证据审计、迁移分析、最终简报和回忆日志模板。
- 添加标准库 Python 脚本：`init_profile.py`、`init_workspace.py`、`validate_run.py`。
- 添加结构验证与 `unittest` 测试。
- 添加中英文对照文档和安全边界说明。

## English

## 0.2.1 - Source-Located Reading And Reading Entry Point

- Added `Source locator` / `Source basis` requirements for numbered Markdown artifacts.
- Added workspace entry point `README_FOR_READING.md`, explaining that users normally read numbered Markdown files `01` through `08`.
- `init_workspace.py` now prints reading guidance and recommends VS Code, Codex file view, Obsidian, Typora, or another Markdown reader.
- Structural validation now checks numbered source locator scaffolding and the reading entry point.
- Added `docs/READING_OUTPUTS.md`.

## 0.2.0 - Initial Implementation

- Created the single `paper-forge` Skill.
- Added workflow instructions for `screen`, `deep`, and `recall` modes.
- Added persistent Profile policy with default path `~/.paper-forge/profile.md`.
- Added local paper workspace templates for source manifest, triage, claim ledger, contribution map, mechanism model, evidence audit, transfer analysis, final brief, and recall log.
- Added standard-library Python scripts: `init_profile.py`, `init_workspace.py`, and `validate_run.py`.
- Added structural validation and `unittest` coverage.
- Added bilingual documentation and security boundary guidance.
