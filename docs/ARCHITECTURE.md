# 架构 / Architecture

## 中文

Paper Forge 的架构刻意保持小而本地化：

- 一个核心 Skill：`skills/paper-forge/`。
- 一个用户拥有的长期 Profile：`~/.paper-forge/profile.md`。
- 每篇论文一个本地工作区：`~/paper-forge-workspace/papers/<date_slug>/`。
- Markdown 产物用于可读、可审计、可手动修改的分析结果。
- 每个工作区包含 `README_FOR_READING.md`，提醒用户主要阅读 `01` 到 `08` 的编号 Markdown 文件。
- 少量 Python 标准库脚本用于初始化和结构验证。

主要目录：

- `skills/paper-forge/SKILL.md`：触发规则、三种模式、Profile、语言、安全和输出要求。
- `skills/paper-forge/assets/`：Profile 和分析产物模板。
- `skills/paper-forge/references/`：工作流、判据、安全和输出契约。
- `skills/paper-forge/scripts/`：确定性辅助脚本。
- `docs/`：面向 GitHub 用户的中英文文档。
- `tests/`：不依赖网络、真实 PDF、API key 或真实 Profile 的标准库测试。

Paper Forge 不包含 Plugin manifest、MCP server、Hook、数据库、浏览器自动化、云服务或多 Agent 编排。分析质量来自 Skill 指令、用户提供的论文材料、Profile 和模型判断；结构验证检查文件结构、必要字段和 source locator 脚手架，不证明论文结论正确。

## English

Paper Forge is intentionally small and local-first:

- One core Skill: `skills/paper-forge/`.
- One user-owned persistent Profile: `~/.paper-forge/profile.md`.
- One local workspace per paper: `~/paper-forge-workspace/papers/<date_slug>/`.
- Markdown outputs for readable, auditable, manually editable analysis.
- Each workspace includes `README_FOR_READING.md`, reminding users to read numbered Markdown files `01` through `08`.
- A few Python standard-library scripts for initialization and structural validation.

Main directories:

- `skills/paper-forge/SKILL.md`: trigger rules, three modes, Profile, language, security, and output requirements.
- `skills/paper-forge/assets/`: Profile and analysis output templates.
- `skills/paper-forge/references/`: workflow, rubrics, safety rules, and output contract.
- `skills/paper-forge/scripts/`: deterministic helper scripts.
- `docs/`: bilingual documentation for GitHub users.
- `tests/`: standard-library tests that do not require network access, real PDFs, API keys, or a real Profile.

Paper Forge contains no Plugin manifest, MCP server, Hook, database, browser automation, cloud service, or multi-agent orchestration. Analysis quality comes from Skill instructions, user-provided paper material, the Profile, and model judgment; structural validation checks file structure, required fields, and source locator scaffolding, but does not prove that paper conclusions are correct.
