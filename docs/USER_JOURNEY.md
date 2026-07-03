# 用户旅程 / User Journey

## 中文

## 阶段 1：发现项目

用户可能通过 GitHub、Bilibili、YouTube、AI Skills 合集、朋友、同学、老师或社交媒体发现 Paper Forge。README 首屏应说明输入和输出：

输入包括本地 PDF、公开 PDF URL、arXiv 链接或编号、DOI、论文落地页。

输出包括论文真正解决的问题、真实贡献、旧方法为什么不足、机制与因果链、证据审计、局限与不确定性、与用户研究方向的相关性、费曼式主动回忆。

## 阶段 2：先设置 Profile

安装说明之前，用户应先看到 `Step 0 - Set Your Persistent Research Profile`。Paper Forge 可以无 Profile 运行，但 Profile 能显著提升相关性和迁移价值判断。Profile 存在 `~/.paper-forge/profile.md`，属于用户，不是模型记忆，也不在 Skill 包内。

## 阶段 3：安装

用户可以复制仓库 URL 给 Codex，请 Codex 安装单一 `paper-forge` Skill。安装 Agent 应先检查 README、Skill 目录、`SKILL.md` 和脚本，说明将安装哪些文件，不安装 Plugin、MCP、Hook、浏览器扩展、系统服务或无关依赖。

## 阶段 4：安装后 Profile 引导

安装完成后，Agent 应报告 Skill 安装目录、版本或 Git commit、调用方式、`~/.paper-forge/profile.md` 是否存在、Profile 作用，以及如何现在配置它。若 Profile 不存在，应提供对话设置、手动编辑或暂时跳过三种选择。

## 阶段 5：Profile 设置

用户可以说“帮我设置 Paper Forge 的 Profile”“展示我的 Paper Forge Profile”“将默认输出语言设为中文”等。Agent 必须只询问论文分析相关信息，先展示拟写入内容和路径，等待明确确认后才写入，并在更新已有 Profile 前创建备份。

## 阶段 6：Screen

用户运行 `$paper-forge screen ./paper.pdf`。Paper Forge 创建工作区、`README_FOR_READING.md`、来源清单和筛选结论，说明是否建议 deep、skip 或 conditional。运行结束时，Agent 应提醒用户主要阅读编号 Markdown 文件，并可用 VS Code、Codex 文件视图、Obsidian、Typora 或其他 Markdown 阅读器打开。

## 阶段 7：Deep

用户运行 `$paper-forge deep ./paper.pdf`。Paper Forge 依次完成来源预检、Profile、语言选择、论文类型路由、主张账本、贡献图谱、机制图、证据审计、迁移分析、最终简报和结构验证。`01` 到 `07` 的编号文件应包含 source locator 或 source basis，帮助用户回到原论文定位页码、章节、图表或实验。

## 阶段 8：Recall

Deep 完成后，Paper Forge 邀请用户运行 `$paper-forge recall`。Recall 一次只问一个问题，先指出用户答案缺失的逻辑，不自动透露完整答案；只有用户明确要求时才揭示答案，并写入 `learning/08_recall_log.md`。问题应记录来源基础；揭示完整答案时应带 source locator。

## English

## Stage 1: Discovery

Users may discover Paper Forge through GitHub, Bilibili, YouTube, AI Skills collections, friends, labmates, teachers, or social media. The README first screen should explain inputs and outputs:

Inputs include local PDFs, public PDF URLs, arXiv links or identifiers, DOIs, and paper landing pages.

Outputs include the real paper problem, real contribution, why prior methods were insufficient, mechanism and causal chain, evidence audit, limitations and uncertainty, relevance to the user's research direction, and Feynman-style active recall.

## Stage 2: Profile First

Before installation instructions, users should see `Step 0 - Set Your Persistent Research Profile`. Paper Forge can run without a Profile, but a Profile substantially improves relevance and transfer analysis. The Profile lives at `~/.paper-forge/profile.md`, belongs to the user, is not model memory, and is not stored inside the Skill package.

## Stage 3: Installation

The user can paste the repository URL into Codex and ask Codex to install the single `paper-forge` Skill. The installing agent should inspect README, the Skill directory, `SKILL.md`, and scripts first, explain which files will be installed, and avoid installing any Plugin, MCP server, Hook, browser extension, system service, or unrelated dependency.

## Stage 4: Post-Install Profile Onboarding

After installation, the agent should report the installed Skill directory, version or Git commit, invocation method, whether `~/.paper-forge/profile.md` exists, what the Profile is for, and how to configure it now. If no Profile exists, it should offer conversational setup, manual editing, or skipping for now.

## Stage 5: Profile Setup

Users may say "Set up my Paper Forge profile", "Show my Paper Forge profile", or "Set Paper Forge output language to Chinese". The agent must ask only for paper-analysis-relevant information, show the exact proposed content and path before writing, wait for explicit approval, and create a backup before updating an existing Profile.

## Stage 6: Screen

The user runs `$paper-forge screen ./paper.pdf`. Paper Forge creates a workspace, `README_FOR_READING.md`, source manifest, and triage report, then recommends `deep`, `skip`, or `conditional`. At the end, the agent should remind the user to read the numbered Markdown files and open them with VS Code, Codex file view, Obsidian, Typora, or another Markdown reader.

## Stage 7: Deep

The user runs `$paper-forge deep ./paper.pdf`. Paper Forge performs source preflight, Profile loading, language selection, paper type routing, claim ledger, contribution map, mechanism diagram, evidence audit, transfer analysis, final brief, and structural validation. Numbered files `01` through `07` should include source locators or source basis fields so the user can return to paper pages, sections, figures, tables, or experiments.

## Stage 8: Recall

After Deep completes, Paper Forge invites the user to run `$paper-forge recall`. Recall asks one question at a time, points out missing logic first, does not reveal the full answer automatically, reveals only when explicitly asked, and writes to `learning/08_recall_log.md`. Questions should record their source basis; revealed answers should include source locators.
