<p align="right">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <img src="assets/paperforge-hero.svg" alt="PaperForge — 论文可追溯阅读" width="100%">
</p>

# PaperForge

**PaperForge 是一个本地优先的 Zotero → AI Agent → Obsidian 工作流，用于可追溯的论文阅读、结构化证据审查、长期研究知识管理。**

它**不是**一个通用论文摘要器。它建立的是一个**受控阅读工作区**，把论文主张、证据、局限、来源位置、迁移假设、回忆记录都显式分开。

## 工作流

```text
Zotero
  (PDF 与标准元数据的唯一事实来源)
        ↓
PaperForge
  (受控工作包 + 分析工作区)
        ↓
Codex / Agent
  (读取 PDF，按结构填充带来源位置的分析)
        ↓
PaperForge
  (结构校验 + 完整性检查 + 导出到 Obsidian)
        ↓
Obsidian
  (长期知识网络、个人批注、双向链接)
```

PaperForge 在每一步都保持四个属性显式：

- **Local-first（本地优先）** — 你的 PDF、工作区、Profile、Obsidian Vault 都留在本地磁盘，不会自动上传到 GitHub。
- **Traceable（可追溯）** — 关键主张必须携带回到 PDF 的来源位置（页码、章节、表格、图表、实验，或显式的 `Unknown`）。
- **Source-located（来源明确）** — 论文事实、作者主张、PaperForge 判断三栏分开记录，绝不混入同一段摘要。
- **Evidence-aware（证据自觉）** — 使用 `paper_not_reported`、`not_verified_in_alpha`、`unavailable_without_repo_check`、`unknown_from_pdf_only` 等显式占位标记，防止未完成的工作被误读为已完成。

## 为什么是 PaperForge

很多 AI 论文工具生成看起来像结论的摘要。PaperForge 为需要始终区分三件事的研究者设计：

1. **论文真正说了什么**（论文事实）
2. **作者怎么主张**（作者主张）
3. **哪些是合理可推断或可迁移的**（基于你 Research Profile 的 PaperForge 判断）

PaperForge 不会试图用一段摘要替代判断。它构建的是一个受控阅读工作区，让论文主张、证据、局限、来源位置、迁移假设、回忆记录都保持显式。

核心论证链端到端保持不变：

```text
problem -> prior limitation -> intervention -> mechanism -> evidence -> limitation -> transfer hypothesis -> recall
```

## 适合谁使用

PaperForge 适合：

- 已经在用 Zotero 管理论文、想把"读过"变成"**可复盘、可迁移、可追溯**"研究资产的人
- 需要把深度阅读结果长期沉淀到 Obsidian Vault 的研究者、工程师、学生、创业者
- 希望让 Codex / Agent 按固定结构做深读，而不是一次性摘要的人
- 关心来源定位、主张/证据分离、持久 Profile、显式局限的人

PaperForge **不**适合：

- 只想要一段快速摘要、不需要证据定位与长期笔记沉淀的人
- 不使用 Zotero 和 Obsidian、也不打算维护本地 Markdown 工作流的人
- 期待系统"替你读完所有论文"并保证正确性的人

## PaperForge 做什么

| 组件 | 负责什么 | 不负责什么 |
|---|---|---|
| **Zotero** | 保存 PDF、标准元数据、DOI/arXiv、collections、item keys | 不做 PaperForge 式证据审查 |
| **PaperForge** | 初始化工作包、组织结构化深度分析、验证结构与完整性、导出到 Obsidian | 不会自动保证论文结论正确 |
| **Codex / Agent** | 按 PaperForge Skill 读取 PDF 并填写结构化分析 | 不是 Zotero 数据库管理器 |
| **Obsidian** | 长期 Markdown 知识网络、双向链接、个人批注、复习 | 不是 PDF 事实的一手来源 |

## PaperForge 不做什么

PaperForge **不会**：

- 自动把 PDF、工作区、Obsidian 笔记或 Profile 上传到 GitHub
- 自动修改 Zotero `storage/` 或 `zotero.sqlite`
- 自动给 Zotero 条目写 tag
- 在 PDF 缺失时伪造全文分析
- 把深度分析结果包装成"绝对正确"的事实
- 替代专家同行评审
- 自动运行任何论文仓库的代码或下载的脚本
- 弱化来源定位要求、证据边界或 prompt-injection 防护

PaperForge 在设计上就是 **local-first、traceable、source-located、evidence-aware** — 这不是营销，是工程约束。

## 快速开始

```bash
git clone https://github.com/Lurek-st/PaperForge.git
cd PaperForge
python skills/paper-forge/scripts/paperforge.py doctor
python skills/paper-forge/scripts/paperforge.py init
python skills/paper-forge/scripts/paperforge.py ingest-zotero
python skills/paper-forge/scripts/paperforge.py deep zotero:EXAMPLE123
```

如果你暂时没有真实 Zotero 条目，也可以用本 README 中的匿名 ID `EXAMPLE123` 演练工作流。PaperForge 不会为你从未配置的 ID 静默编造内容。

## 安装

### 安装前准备

必需：

- Git，或能从 GitHub 下载 ZIP
- Python 3.9 或更高版本
- Zotero Desktop
- 你自己的 Zotero 文献库
- Obsidian
- 能运行 Codex / Agent 的环境（如 Codex CLI 或 Claude Code）

可选：

- GitHub Desktop
- VS Code
- 独立的 Python 虚拟环境

当前验证情况：

- **Windows**：已验证
- **macOS / Linux**：理论上可用，请按相同 Python 环境方式配置并自行验证

### 下载与安装

方式 A：使用 Git 克隆

```bash
git clone https://github.com/Lurek-st/PaperForge.git
cd PaperForge
```

方式 B：下载 ZIP

```text
GitHub 页面 -> Code -> Download ZIP -> 解压 -> 在终端进入 PaperForge 目录
```

### （可选）创建虚拟环境

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

PaperForge 没有第三方运行依赖，核心命令可直接执行。

### 安装后先做环境检查

```bash
python skills/paper-forge/scripts/paperforge.py doctor
```

你应看到类似：

- `PaperForge doctor`
- `Workspace root`
- `Obsidian vault`
- `Zotero Desktop Local API is reachable` 或明确的失败原因

## 配置

### 首次配置

```bash
python skills/paper-forge/scripts/paperforge.py init
```

这会在默认位置创建用户级配置与工作目录。默认情况下：

```text
PAPERFORGE_HOME 未设置时：
~/.paper-forge/
```

你也可以通过环境变量指定：

```text
PAPERFORGE_HOME=<your-paperforge-data-directory>
```

### 请确保以下目录分离

```text
<project-root>/PaperForge            <-- 本仓库
<your-paperforge-data-directory>     <-- 受控工作区
<your-zotero-data-directory>         <-- 由 Zotero 拥有
<your-obsidian-vault>                <-- 由你拥有
```

推荐结构：

```text
<project-root>/PaperForge
├── skills/
├── docs/
├── tests/
├── profile.example.md
├── paperforge-config.example.yaml
├── CHANGELOG.md
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

## Zotero 集成

PaperForge 通过 Zotero Local API 读取数据。该链路当前**只读**：

- 读取论文元数据
- 查找 PDF 附件
- 建立 PaperForge 工作包

它**不会**：

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

   成功后应看到：

   ```text
   Zotero Desktop Local API is reachable.
   ```

常见失败原因：

- Zotero Desktop 没有启动
- Local API 不可用
- 本地端口不可达
- 条目没有 PDF
- 配置中的 collection 名与实际不一致

## Obsidian 集成

Obsidian 是 PaperForge 的长期知识网络输出端。你需要在配置中提供自己的 Vault 路径：

```text
obsidian:
  vault_path: "<your-obsidian-vault>"
```

PaperForge 只会向这个位置导出。

保护策略：

- 已有笔记默认不覆盖
- 发现旧版 `00.md` 到 `05.md` 时默认跳过并提示
- 发现不同语言版本的现有标题文件时默认跳过，避免静默生成重复页面

## 个人 Research Profile

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

方式 1：直接复制模板

Windows：

```bash
copy profile.example.md %USERPROFILE%\.paper-forge\profile.md
```

macOS / Linux：

```bash
mkdir -p ~/.paper-forge
cp profile.example.md ~/.paper-forge/profile.md
```

方式 2：使用初始化脚本

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

`auto` 规则：

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

## `screen` / `deep` / `recall`

PaperForge 严格使用三种阅读模式：

- `screen` — 快速 triage，决定这篇论文是否值得 deep reading
- `deep` — 完整可追溯分析，结构校验、完整性检查、可选导出 Obsidian
- `recall` — 在同一个 Skill 内的 Feynman 风格主动回忆

`deep` **不会**自己完成论文语义分析。它会创建或复用工作区、运行结构校验、运行完整性检查，并在分析被填好的情况下导出 Obsidian。真正的语义深读仍由 Codex / Agent 按 PaperForge Skill 填写这些文件：

```text
analysis/01_triage.md
analysis/02_claim_ledger.md
analysis/03_contribution_map.md
analysis/04_mechanism.md
analysis/05_evidence_audit.md
analysis/06_transfer_analysis.md
analysis/07_final_brief.md
learning/08_recall_log.md
```

参考提示词：

```text
使用 PaperForge deep 工作流分析 zotero:EXAMPLE123。
读取 PDF，按 Profile 与选定语言填充 analysis/*.md。
所有关键结论必须附带可追溯证据位置。
区分论文事实、作者主张与 PaperForge 判断。
```

端到端参考示例见 [docs/DEMO_TRANSCRIPT.md](docs/DEMO_TRANSCRIPT.md)。

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

- **论文事实**：论文明确写了什么、实验展示了什么
- **作者主张**：作者如何解释自己的方法和结果
- **PaperForge 判断**：基于证据做出的可信度、迁移性和风险判断

## 证据与来源定位哲学

PaperForge 在三条边界上是强制的：

1. **主张不是证据。** `02_claim_ledger.md` 中每条主张必须带 `Source Locator` 与 `Direct Evidence`。若主张无法从现有来源材料验证，则标记为 `Unknown` 并说明缺失什么。
2. **来源定位必须诚实。** PaperForge 绝不伪造页码、图表号、表格号、实验 ID、源代码行或引用。当精确 PDF 页码不可得时，定位会写 `PDF page Unknown` 并给出可用的章节、图表、表格、附录、DOI、arXiv ID、URL 或 HTML 定位。
3. **Agent 的输出不是自动证据。** PaperForge 把 Agent 的草稿与论文同等对待：它是结构化阅读产物，不是事实裁决。用户需要自行核对重要主张。

这些规则存在的原因：PaperForge 是**阅读工具**，不是真值引擎。

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

完整安全模型见 [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md)。

## 测试

运行测试：

```bash
python -m unittest discover -s tests -p "test_*.py"
```

提交代码前建议至少确认：

- CLI 主要命令能运行
- `python -m unittest discover -s tests -p "test_*.py"` 通过
- 没有把 PDF、`.env`、Profile、Vault 输出或用户工作区加入 Git

## 项目结构

```text
PaperForge/
├── skills/
│   └── paper-forge/
├── docs/
├── tests/
├── assets/
│   ├── paperforge-hero.svg
│   ├── social-preview.svg
│   └── social-preview.png
├── profile.example.md
├── paperforge-config.example.yaml
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## 贡献与反馈

欢迎提交贡献、bug report、文档修正和可复现的测试用例。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

特别欢迎：

- 安装修复
- Zotero 兼容性报告
- Obsidian 导出问题
- 来源定位与证据可追溯性改进
- 跨平台验证
- 可复现的 bug 报告
- 测试
- 文档

请不要提交：

- 私人 PDF
- 真实 Zotero 数据
- 个人 Profile
- Obsidian Vault
- `.env`
- Token、API Key、凭据文件

相关文档：

- [CHANGELOG.md](CHANGELOG.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [docs/workflow.md](docs/workflow.md)
- [docs/obsidian-structure.md](docs/obsidian-structure.md)
- [docs/troubleshooting.md](docs/troubleshooting.md)
- [docs/LIMITATIONS.md](docs/LIMITATIONS.md)

## 常见问题与故障排查

**Q1：`doctor` 检查失败怎么办？**

- 先看 CLI 输出是路径、写权限还是 Zotero Local API 问题
- 若是 Zotero 问题，确认 Zotero Desktop 已启动
- 若是路径问题，检查 `config.yaml` 中 `workspace.root` 和 `obsidian.vault_path`

**Q2：Zotero 已启动，但读不到条目怎么办？**

- 确认 collection 名与配置一致
- 确认条目不是 attachment 子条目
- 重新运行 `doctor`

**Q3：条目存在但没有 PDF，为什么不能生成完整分析？**

- 因为 PaperForge 不会在 PDF 缺失时伪造全文结论
- 这类情况会降级为 `metadata_only`

**Q4：为什么输出是 `metadata_only`？**

- 常见原因是 PDF 缺失或不可访问
- 检查 Zotero 附件是否真实存在

**Q5：为什么 Obsidian 目录没有生成？**

- 看 `deep` 是否因为 `analysis_incomplete` 跳过导出
- 或 `obsidian.vault_path` 配置错误

**Q6：为什么已有笔记没有被覆盖？**

- 这是默认保护策略
- PaperForge 优先保护用户手写内容

**Q7：如何重新分析同一篇论文？**

- 重新运行 `deep`
- 只会补写缺失内容或在显式 `--force` 时备份后重写

**Q8：如何改成中文、英文或中英文对照？**

- 在 `profile.md` 中设置 `default_output_language` 与 `obsidian_note_language`
- 或在 CLI 中使用 `--language` / `--obsidian-language`

**Q9：如何修改自己的 Research Profile？**

- 直接编辑 `~/.paper-forge/profile.md`
- 修改后，新的 deep / export 会读取新的偏好

**Q10：为什么文件名是"编号 + 主题"？**

- 为了保证 Obsidian 左侧文件树可读，同时保留固定排序

**Q11：我可以直接编辑 Obsidian 文件吗？**

- 可以
- 但请理解之后重新导出时，PaperForge 会优先保护已有内容

**Q12：如何避免把论文、PDF 和笔记上传到 GitHub？**

- 不要把这些数据放在项目源码目录内
- 本仓库 `.gitignore` 已忽略常见用户数据目录、PDF、Profile 和 Vault 输出

**Q13：PaperForge 会不会自动修改我的 Zotero 标签？**

- 不会
- 当前 Zotero Local API 链路只读

**Q14：作者名乱码或非英文名字显示异常怎么办？**

- 当前实现会显式按 UTF-8 / Unicode 安全方式处理
- 仅在字符串明显像 mojibake 时才尝试保守恢复
- 若仍异常，请保留最小复现实例并提交 Issue

**Q15：Codex / Agent 没有正确填充 analysis 文件怎么办？**

- 检查提示词是否明确要求"附带 source locator"
- 检查 PDF 是否可访问
- 检查 `analysis/*.md` 是否仍是模板占位符

更多排查可见：

- [docs/troubleshooting.md](docs/troubleshooting.md)
- [docs/workflow.md](docs/workflow.md)
- [docs/obsidian-structure.md](docs/obsidian-structure.md)

## 许可证

PaperForge 使用 MIT License 开源。

详见 [LICENSE](LICENSE)。
