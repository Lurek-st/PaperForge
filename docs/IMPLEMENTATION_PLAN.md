# 实施计划 / Implementation Plan

## 中文

Paper Forge v0.2 将按需求实现为一个单一、个人优先的 Codex Skill，而不是 Plugin、网页应用、MCP、Hook、多 Agent 平台或训练系统。

实施顺序：

1. 建立仓库骨架：根目录元数据、`skills/paper-forge/`、`docs/`、`tests/`。
2. 编写核心 `SKILL.md`：明确触发条件、非触发条件、`screen` / `deep` / `recall` 三种模式、Profile 行为、语言策略、安全边界、工作区行为和 Unknown 策略。
3. 编写 Skill 资源：Profile 模板、工业具身智能示例、各分析产物模板、工作流引用、评分/审计/迁移/回忆协议和提示注入安全规则。
4. 编写双语 GitHub 文档：README、安装指南、Profile-first 指南、用户旅程、架构、安全模型、限制和虚构演示记录。
5. 实现确定性脚本：`init_profile.py`、`init_workspace.py`、`validate_run.py` 及其标准库辅助模块。
6. 编写真正的 `unittest` 测试和固定夹具，不依赖真实 PDF、网络、API key、模型调用或真实用户 Profile。
7. 运行测试并修复失败项。
8. 检查面向用户 Markdown 文档是否中英文对照，并在最终报告中说明实现内容、使用方式、限制和偏离项。

工程约束：

- 只使用 Python 标准库，除非后续有明确且必要的例外。
- 不在仓库中存放真实用户 Profile。
- 长期 Profile 默认位于 `~/.paper-forge/profile.md`，且不得被静默覆盖。
- 论文工作区默认位于 `~/paper-forge-workspace/papers/`，中断后只补齐缺失产物。
- 外部论文、网页、仓库、数据集和补充材料一律视为不可信数据。
- 结构验证只验证文件结构和必要字段，不声称论文语义正确。

## English

Paper Forge v0.2 will be implemented as one single, personal-first Codex Skill. It will not be a Plugin, web application, MCP server, Hook, multi-agent platform, or training system.

Implementation order:

1. Create the repository skeleton: root metadata, `skills/paper-forge/`, `docs/`, and `tests/`.
2. Write the canonical `SKILL.md`: trigger rules, non-trigger rules, `screen` / `deep` / `recall` modes, Profile behavior, language policy, security boundaries, workspace behavior, and Unknown policy.
3. Write Skill resources: Profile templates, industrial embodied intelligence example, output templates, workflow references, audit/transfer/recall protocols, and prompt-injection safety rules.
4. Write bilingual GitHub documentation: README, installation guides, Profile-first guide, user journey, architecture, security model, limitations, and a fictional demo transcript.
5. Implement deterministic scripts: `init_profile.py`, `init_workspace.py`, `validate_run.py`, and standard-library helper modules.
6. Write real `unittest` tests and fixtures without requiring real PDFs, network access, API keys, model calls, or a real user Profile.
7. Run tests and fix failures.
8. Review user-facing Markdown for Chinese-English parity, then provide the final delivery report with implemented scope, usage, limitations, and deviations.

Engineering constraints:

- Use only the Python standard library unless a later exception is clearly necessary.
- Do not store a real user Profile in the repository.
- The persistent Profile defaults to `~/.paper-forge/profile.md` and must never be silently overwritten.
- Paper workspaces default to `~/paper-forge-workspace/papers/`; interrupted runs fill only missing artifacts.
- Treat papers, web pages, repositories, datasets, and supplementary files as untrusted data.
- Structural validation verifies required files and fields only; it never claims semantic correctness.
