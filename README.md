# PaperForge

面向 Zotero 文献库的论文深度分析工作流，将 PDF 与标准元数据组织为可追溯的分析工作区，并导出到 Obsidian 形成长期知识网络。

核心链路：

```text
Zotero
  保存 PDF 与标准元数据
        ↓
PaperForge
  建立可追溯的分析工作区
        ↓
Codex / Agent
  阅读 PDF，填写结构化分析与证据审查
        ↓
PaperForge
  导出到用户自己的 Obsidian Vault
```

> PaperForge 不是“自动替你读完所有论文并保证结论正确”的工具。
> 它的作用是建立稳定工作区、约束分析结构、保存证据链，并把深度阅读结果沉淀为长期知识资产。

## 目录

- [项目是什么](#项目是什么)
- [适合谁使用](#适合谁使用)
- [核心工作流](#核心工作流)
- [功能边界与数据安全](#功能边界与数据安全)
- [安装前准备](#安装前准备)
- [下载与安装](#下载与安装)
- [首次配置](#首次配置)
- [配置数据目录](#配置数据目录)
- [配置 Zotero](#配置-zotero)
- [配置 Obsidian](#配置-obsidian)
- [配置个人 Research Profile](#配置个人-research-profile)
- [配置输出语言](#配置输出语言)
- [最小可用流程](#最小可用流程)
- [使用 Codex / Agent 执行深度分析](#使用-codex--agent-执行深度分析)
- [Obsidian 输出结构与阅读顺序](#obsidian-输出结构与阅读顺序)
- [常用命令](#常用命令)
- [如何重新运行与保护已有笔记](#如何重新运行与保护已有笔记)
- [常见问题与故障排查](#常见问题与故障排查)
- [隐私数据与 Zotero 写入边界](#隐私数据与-zotero-写入边界)
- [测试与开发](#测试与开发)
- [项目结构](#项目结构)
- [贡献与反馈](#贡献与反馈)

## 项目是什么

PaperForge 是一个本地优先的 Zotero → PaperForge → Obsidian 工作流。

三者职责分工：

| 组件 | 负责什么 | 不负责什么 |
|---|---|---|
| Zotero | 保存 PDF、标准元数据、条目组织 | 不做 PaperForge 式证据审查 |
| PaperForge | 初始化工作区、组织深度分析、验证结构、导出 Obsidian | 不会自动替你保证论文结论正确 |
| Codex / Agent | 按 PaperForge 结构读取论文并填写分析文件 | 不是 Zotero 数据库管理器 |
| Obsidian | 长期知识网络、批注、关联、复习 | 不是原始 PDF 事实来源 |

PaperForge 的核心推理链保持不变：

```text
problem -> prior limitation -> intervention -> mechanism -> evidence -> limitation -> transfer hypothesis -> recall
```

## 适合谁使用

适合：

- 已经用 Zotero 管理论文，想把“读过”变成“可复盘、可迁移、可追溯”的研究资产的人
- 需要把论文阅读结果长期沉淀到 Obsidian 的研究者、工程师、学生、创业者
- 希望让 Codex / Agent 按固定结构做深读，而不是输出一次性摘要的人

不太适合：

- 只想要一段快速摘要、不需要证据定位与长期笔记沉淀的人
- 不使用 Zotero 和 Obsidian，也不打算维护本地 Markdown 工作流的人

## 核心工作流

```text
1. 在 Zotero Desktop 中保存论文和 PDF
2. PaperForge 读取元数据和 PDF，建立受控工作区
3. Codex / Agent 按 PaperForge deep 结构填写 analysis/*.md
4. PaperForge 验证结构完整性并导出到 Obsidian
5. 用户在 Obsidian 中继续补充批注、链接、实验联想和复习记录
```

## 功能边界与数据安全

> 请把“项目源码目录”和“用户自己的论文数据目录”严格分开。

PaperForge 当前明确支持：

- Zotero 作为可选的 PDF 与标准元数据来源
- PaperForge 工作区初始化、结构化深度分析工作流、证据审查、Obsidian 导出
- 用户通过 Profile 定义研究偏好与输出语言

PaperForge 当前明确不做：

- 不会自动上传你的 PDF、工作区、Obsidian 笔记或 Profile 到 GitHub
- 不会自动修改 Zotero `storage/` 或 `zotero.sqlite`
- 不会自动给 Zotero 条目写 tag
- 不会在 PDF 缺失时伪造全文分析
- 不会把深度分析结果包装成“绝对正确”的事实

## 安装前准备

必需：

- Git，或能从 GitHub 下载 ZIP
- Python 3.9 或更高版本
- Zotero Desktop
- 你自己的 Zotero 文献库
- Obsidian
- 可以运行 Codex / Agent 的环境

可选：

- GitHub Desktop
- VS Code
- 单独的 Python 虚拟环境

当前验证情况：

- Windows：已验证
- macOS / Linux：理论上可用，但请按相同 Python 环境方式配置并自行验证

## 下载与安装

方式 A：使用 Git 克隆

```bash
git clone https://github.com/Lurek-st/PaperForge.git
cd PaperForge
```

方式 B：下载 ZIP

```text
GitHub 页面 -> Code -> Download ZIP -> 解压 -> 在终端进入 PaperForge 目录
```

可选：创建虚拟环境

Windows：

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

当前项目没有额外第三方运行依赖，核心命令可直接执行。

安装后先做环境检查：

```bash
python skills/paper-forge/scripts/paperforge.py doctor
```

你应看到这类信息：

- PaperForge doctor
- Workspace root
- Obsidian vault
- Zotero Desktop Local API is reachable 或明确的失败原因

## 首次配置

建议先执行：

```bash
python skills/paper-forge/scripts/paperforge.py init
```

这会在默认位置创建用户级配置与工作目录。默认情况下，PaperForge 使用：

```text
PAPERFORGE_HOME 未设置时：
~/.paper-forge/
```

你也可以通过环境变量指定：

```text
PAPERFORGE_HOME=<your-paperforge-data-directory>
```

## 配置数据目录

请确保以下目录分离：

```text
<project-root>/PaperForge
<your-paperforge-data-directory>
<your-zotero-data-directory>
<your-obsidian-vault>
```

推荐结构：

```text
<project-root>/PaperForge
├── skills/
├── docs/
├── tests/
└── README.md

<your-paperforge-data-directory>
├── config.yaml
├── profile.md
├── workspace/
│   ├── inbox/
│   ├── processing/
│   ├── cache/
│   ├── failed/
│   ├── archive/
│   └── logs/
└── obsidian-vault/
```

配置模板见：

- [paperforge-config.example.yaml](paperforge-config.example.yaml)
- [skills/paper-forge/assets/default-config.yaml](skills/paper-forge/assets/default-config.yaml)

用户级配置文件位置：

```text
~/.paper-forge/config.yaml
```

或：

```text
<PAPERFORGE_HOME>/config.yaml
```

关键配置项：

| 配置项 | 作用 |
|---|---|
| `zotero.data_directory` | 你自己的 Zotero 数据目录 |
| `workspace.root` | PaperForge 用户数据目录下的 workspace 根目录 |
| `obsidian.vault_path` | 你自己的 Obsidian Vault 路径 |
| `language.default_output_language` | deep 分析的默认语言偏好 |
| `language.obsidian_note_language` | Obsidian 文件名、页面标题、导航语言 |

## 配置 Zotero

PaperForge 当前通过 Zotero Local API 读取数据。

这条链路当前只读：

- 读取论文元数据
- 查找 PDF 附件
- 建立 PaperForge 工作区

它不会：

- 自动修改 Zotero 本地条目
- 自动给 Zotero 条目写 tag
- 自动重写 Zotero collection

建议配置步骤：

1. 安装并启动 Zotero Desktop。
2. 在 Zotero 中创建 `PaperForge Inbox` collection，或在配置里使用你自己的 collection 名。
3. 用 Zotero Connector 保存论文与 PDF。
4. 运行：

```bash
python skills/paper-forge/scripts/paperforge.py doctor
```

如果成功，你应看到：

```text
Zotero Desktop Local API is reachable.
```

常见失败原因：

- Zotero Desktop 没有启动
- Local API 不可用
- 本地端口不可达
- 条目没有 PDF
- 配置中的 collection 名与实际不一致

## 配置 Obsidian

Obsidian 是 PaperForge 的长期知识网络输出端。

你需要在配置中提供自己的 Vault 路径：

```text
obsidian:
  vault_path: "<your-obsidian-vault>"
```

PaperForge 只会向这个位置导出。

保护策略：

- 已有笔记默认不覆盖
- 发现旧版 `00.md` 到 `05.md` 时默认跳过并提示
- 发现不同语言版本的现有标题文件时默认跳过，避免静默生成重复页面

## 配置个人 Research Profile

公开仓库提供模板：

- [profile.example.md](profile.example.md)
- [skills/paper-forge/assets/profile-template.md](skills/paper-forge/assets/profile-template.md)

真实使用的 Profile 文件位置：

```text
~/.paper-forge/profile.md
```

或：

```text
<PAPERFORGE_HOME>/profile.md
```

创建方式 1：直接复制模板

```bash
copy profile.example.md %USERPROFILE%\.paper-forge\profile.md
```

macOS / Linux：

```bash
mkdir -p ~/.paper-forge
cp profile.example.md ~/.paper-forge/profile.md
```

创建方式 2：使用初始化脚本

```bash
python skills/paper-forge/scripts/init_profile.py
```

Profile 会影响：

- deep 分析时强调哪些问题
- transfer analysis 关注哪些工程或研究约束
- 默认输出语言
- Obsidian 标题与文件名语言
- 输出详略偏好

建议字段：

| 字段 | 作用 |
|---|---|
| `default_output_language` | deep 分析默认语言：`auto` / `zh` / `en` / `bilingual` |
| `obsidian_note_language` | Obsidian 文件名、标题、导航语言 |
| `preferred_detail_level` | 输出详略偏好 |
| `Research Interests` | 你长期关心的主题 |
| `Priority Questions` | 评估论文时最重要的问题 |
| `Reliability And Transfer Priorities` | 工程稳定性、可复现性、部署约束等 |

不要写入：

- 密码
- Token
- API Key
- 身份证件
- 地址
- 与论文分析无关的个人隐私

## 配置输出语言

PaperForge 现在支持四种语言模式：

| 模式 | deep 分析语言 | Obsidian 文件名 / 标题 / 导航 |
|---|---|---|
| `zh` | 中文 | 中文 |
| `en` | 英文 | 英文 |
| `bilingual` | 中英文对照 | 中英文对照 |
| `auto` | 自动 | 自动 |

当前优先级：

```text
CLI 显式参数
>
profile.md
>
config.yaml
>
auto 的回退规则
```

当前 `auto` 规则：

- deep 分析语言：若没有更明确设置，回退到配置中的 `fallback_output_language`
- Obsidian note 语言：若仍是 `auto`，跟随已解析出的 deep 输出语言；若仍无法确定，则回退到英文

CLI 覆盖示例：

```bash
python skills/paper-forge/scripts/paperforge.py export-obsidian zotero:EXAMPLE123 --language zh --obsidian-language bilingual
```

对应的 Obsidian 文件名示例：

```text
zh:
01 - 论文定位、旧路径局限与真实贡献.md

en:
01 - Problem, Prior Limitation, Actual Contribution.md

bilingual:
01 - 论文定位、旧路径局限与真实贡献 | Problem, Prior Limitation, Actual Contribution.md
```

## 最小可用流程

下面是一套不依赖真实私人数据的最小流程。

1. 检查环境

```bash
python skills/paper-forge/scripts/paperforge.py doctor
```

目的：

- 确认工作区目录可写
- 确认 Zotero Local API 是否可达
- 确认 Obsidian Vault 路径是否可用

2. 从 Zotero 读取条目

```bash
python skills/paper-forge/scripts/paperforge.py ingest-zotero
```

成功后应看到：

- `Paper package: ...`
- `paper_id: zotero:...`

如果你没有现成 Zotero 条目，也可以用匿名化 metadata JSON 手动导入。

3. 初始化核心分析工作区

```bash
python skills/paper-forge/scripts/paperforge.py init-workspace zotero:EXAMPLE123 --language zh
```

成功后应看到：

- `PaperForge core workspace: ...`
- `status: analysis_workspace_ready`

4. 使用 Codex / Agent 填充 deep 分析文件

参考提示词：

```text
使用 PaperForge deep 工作流分析 zotero:EXAMPLE123。
读取 PDF，按 Profile 与选定语言填充 analysis/*.md。
所有关键结论必须附带可追溯证据位置。
区分论文事实、作者主张与 PaperForge 判断。
```

5. 运行 deep 校验并导出

```bash
python skills/paper-forge/scripts/paperforge.py deep zotero:EXAMPLE123 --obsidian-language zh
```

如果 deep 分析仍不完整，CLI 会明确报告 `analysis_incomplete`。

如果你只想单独导出已有工作区：

```bash
python skills/paper-forge/scripts/paperforge.py export-obsidian zotero:EXAMPLE123 --obsidian-language zh
```

## 使用 Codex / Agent 执行深度分析

当前状态请务必注意：

- `deep` CLI 会创建或复用工作区
- 会做结构校验与完整性检查
- 会在合适时导出 Obsidian

但它不会自己完成论文语义分析。

真正的语义深读仍需要你在 Codex / Agent 中执行 PaperForge deep 工作流，填写这些文件：

```text
analysis/01_triage.md
analysis/02_claim_ledger.md
analysis/03_contribution_map.md
analysis/04_mechanism.md
analysis/05_evidence_audit.md
analysis/06_transfer_analysis.md
analysis/07_final_brief.md
```

## Obsidian 输出结构与阅读顺序

示例结构：

```text
<your-obsidian-vault>/
└── Papers/
    └── 2026-07-04__Example_Paper__EXAMPLE123/
        ├── 2026-07-04__Example_Paper__EXAMPLE123.md
        ├── 00 - Source, Metadata, Profile Snapshot.md
        ├── 01 - Problem, Prior Limitation, Actual Contribution.md
        ├── 02 - Mechanism, Method, Causal Chain.md
        ├── 03 - Claims, Evidence, Limitations, Unproven Parts.md
        ├── 04 - Transfer Analysis, User Research Relevance, Project Ideas.md
        ├── 05 - Feynman Recall, Self-Explanation, Open Questions.md
        └── paperforge-manifest.json
```

推荐阅读顺序：

```text
主页
→ 01
→ 02
→ 03
→ 04
→ 05
需要查看来源、元数据、PDF 定位时，再读 00
```

各文件回答什么问题：

| 文件 | 回答什么 | 何时读 |
|---|---|---|
| `00` | 来源、元数据、Zotero 跳转、Profile 快照 | 查来源时 |
| `01` | 论文在解决什么问题，旧路径为什么不够 | 刚开始读 |
| `02` | 方法如何工作，因果链是什么 | 机制梳理 |
| `03` | 证据是否真的支持主张，哪些仍未证 | 证据审查 |
| `04` | 能否迁移到你的研究或工程场景 | 迁移判断 |
| `05` | 你是否真的能自己解释清楚 | 复习与 recall |

请始终区分：

- 论文事实：论文明确写了什么、实验展示了什么
- 作者主张：作者如何解释自己的方法和结果
- PaperForge 判断：基于证据做出的可信度、迁移性和风险判断

## 常用命令

```bash
python skills/paper-forge/scripts/paperforge.py init
python skills/paper-forge/scripts/paperforge.py doctor
python skills/paper-forge/scripts/paperforge.py ingest-zotero
python skills/paper-forge/scripts/paperforge.py init-workspace zotero:EXAMPLE123
python skills/paper-forge/scripts/paperforge.py deep zotero:EXAMPLE123
python skills/paper-forge/scripts/paperforge.py export-obsidian zotero:EXAMPLE123
python skills/paper-forge/scripts/paperforge.py status
python skills/paper-forge/scripts/paperforge.py reindex
python skills/paper-forge/scripts/paperforge.py repair-links
python skills/paper-forge/scripts/init_profile.py
python -m unittest discover
```

## 如何重新运行与保护已有笔记

默认保护策略：

- 不覆盖已有 Obsidian 用户笔记
- 不自动迁移旧版 `00.md` 到 `05.md`
- 不因语言切换静默创建重复的一套标题页面

如果你显式使用 `--force`：

- 会先创建备份
- 仍建议先检查 `git status` 和导出目录

如果你想导出另一种语言版本：

- 最安全的方式是导出到不同 Vault 或不同 paper folder
- 或先人工迁移 / 归档旧版本再导出

## 常见问题与故障排查

Q1：`doctor` 检查失败怎么办？

- 先看 CLI 输出是路径、写权限还是 Zotero Local API 问题
- 若是 Zotero 问题，确认 Zotero Desktop 已启动
- 若是路径问题，检查 `config.yaml` 中 `workspace.root` 和 `obsidian.vault_path`

Q2：Zotero 已启动，但读不到条目怎么办？

- 确认 collection 名与配置一致
- 确认条目不是 attachment 子条目
- 重新运行 `doctor`

Q3：条目存在但没有 PDF，为什么不能生成完整分析？

- 因为 PaperForge 不会在 PDF 缺失时伪造全文结论
- 这类情况会降级为 `metadata_only`

Q4：为什么输出是 `metadata_only`？

- 常见原因是 PDF 缺失或不可访问
- 检查 Zotero 附件是否真实存在

Q5：为什么 Obsidian 目录没有生成？

- 看 `deep` 是否因为 `analysis_incomplete` 跳过导出
- 或 `obsidian.vault_path` 配置错误

Q6：为什么已有笔记没有被覆盖？

- 这是默认保护策略
- PaperForge 优先保护用户手写内容

Q7：如何重新分析同一篇论文？

- 重新运行 `deep`
- 只会补写缺失内容或在显式 `--force` 时备份后重写

Q8：如何改成中文、英文或中英文对照？

- 在 `profile.md` 中设置 `default_output_language` 与 `obsidian_note_language`
- 或在 CLI 中使用 `--language` / `--obsidian-language`

Q9：如何修改自己的 Research Profile？

- 直接编辑 `~/.paper-forge/profile.md`
- 修改后，新的 deep / export 会读取新的偏好

Q10：为什么文件名是“编号 + 主题”？

- 为了保证 Obsidian 左侧文件树可读，同时保留固定排序

Q11：我可以直接编辑 Obsidian 文件吗？

- 可以
- 但请理解之后重新导出时，PaperForge 会优先保护已有内容

Q12：如何避免把论文、PDF 和笔记上传到 GitHub？

- 不要把这些数据放在项目源码目录内
- 本仓库 `.gitignore` 已忽略常见用户数据目录、PDF、Profile 和 Vault 输出

Q13：PaperForge 会不会自动修改我的 Zotero 标签？

- 不会
- 当前 Zotero Local API 链路只读

Q14：作者名乱码或非英文名字显示异常怎么办？

- 当前实现会显式按 UTF-8 / Unicode 安全方式处理
- 仅在字符串明显像 mojibake 时才尝试保守恢复
- 若仍异常，请保留最小复现实例并提交 Issue

Q15：Codex / Agent 没有正确填充 analysis 文件怎么办？

- 检查提示词是否明确要求“附带 source locator”
- 检查 PDF 是否可访问
- 检查 `analysis/*.md` 是否仍是模板占位符

更多排查可见：

- [docs/troubleshooting.md](docs/troubleshooting.md)
- [docs/workflow.md](docs/workflow.md)
- [docs/obsidian-structure.md](docs/obsidian-structure.md)

## 隐私数据与 Zotero 写入边界

PaperForge 的安全边界：

1. 不会自动向 GitHub 上传用户 PDF、工作区、Obsidian 笔记或 Profile
2. 用户应把论文、工作区、Vault 放在仓库之外，或确保它们被 Git 忽略
3. 当前通过 Zotero Local API 读取数据
4. 当前 Local API 链路只读
5. 不会自动给 Zotero 条目写 tag
6. PDF 缺失时不会伪造全文结论
7. 关键结论仍应回查原 PDF、图表、实验设置和附录
8. 不要把 API Key、Token、私人 PDF、个人 Profile 或 Vault 提交到 Git

## 测试与开发

运行测试：

```bash
python -m unittest discover
```

提交代码前建议至少确认：

- CLI 主要命令能运行
- `python -m unittest discover` 通过
- 没有把 PDF、`.env`、Profile、Vault 输出或用户工作区加入 Git

## 项目结构

```text
PaperForge/
├── skills/
│   └── paper-forge/
├── docs/
├── tests/
├── profile.example.md
├── paperforge-config.example.yaml
├── CHANGELOG.md
└── README.md
```

## 贡献与反馈

欢迎提交：

- Issue
- 文档改进
- 测试补充
- CLI / 导出 / 结构验证改进

贡献时请不要提交：

- 私人 PDF
- 真实 Zotero 数据
- 个人 Profile
- Obsidian Vault
- `.env`
- Token、API Key、凭据文件

相关文档：

- [CHANGELOG.md](CHANGELOG.md)
- [docs/workflow.md](docs/workflow.md)
- [docs/obsidian-structure.md](docs/obsidian-structure.md)
- [docs/troubleshooting.md](docs/troubleshooting.md)
