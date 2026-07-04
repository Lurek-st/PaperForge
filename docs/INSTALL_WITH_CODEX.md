# Install With Codex / 使用 Codex 安装

## 中文

将下面的提示词复制给 Codex，并把 `<REPOSITORY_URL>` 替换成真实仓库地址：

```text
请从这个 GitHub 仓库安装 PaperForge Skill：

<REPOSITORY_URL>

安装前：
1. 先阅读 README.md、AGENTS.md、skills/paper-forge/SKILL.md、脚本和文档。
2. 只安装 canonical Skill：skills/paper-forge/。
3. 不要创建 Plugin、MCP server、Hook、浏览器自动化、云服务或多 Agent 工作流。
4. 不要修改 Zotero 的 storage/ 或 zotero.sqlite。
5. 不要把用户 Profile 写入仓库；Profile 属于 ~/.paper-forge/profile.md。
6. 展示将安装哪些文件和目标位置。
7. 安装后验证 Skill 可被发现。
8. 检查 ~/.paper-forge/profile.md 是否存在；如不存在，说明作用，并询问是否现在设置。
9. 在写入 Profile 前展示完整内容和目标路径，等待我确认。
```

安装完成后，Codex 不应只说“完成”。它应说明：

- Skill 安装目录。
- 当前版本或 Git commit。
- 如何运行 `paperforge.py init`、`doctor`、`ingest-zotero`、`analyze`。
- `~/.paper-forge/profile.md` 是否存在。
- Zotero Desktop、Zotero Connector、Obsidian 和 PaperForge 的分工。
- Zotero 是原始 PDF 与标准元数据的事实源。
- PaperForge 不会修改 Zotero `storage/` 或 `zotero.sqlite`。
- 不要把 Zotero 数据目录放入云同步盘。
- 优先在 Obsidian 内移动或重命名 PaperForge 生成的笔记。

## English

Copy this prompt into Codex and replace `<REPOSITORY_URL>` with the real repository URL:

```text
Install the PaperForge Skill from this GitHub repository:

<REPOSITORY_URL>

Before installation:
1. Read README.md, AGENTS.md, skills/paper-forge/SKILL.md, scripts, and docs.
2. Install only the canonical Skill: skills/paper-forge/.
3. Do not create Plugins, MCP servers, Hooks, browser automation, cloud services, or multi-agent workflows.
4. Do not modify Zotero storage/ or zotero.sqlite.
5. Do not store the user Profile in the repository; it belongs at ~/.paper-forge/profile.md.
6. Show which files will be installed and where.
7. Verify that the Skill is discoverable after installation.
8. Check whether ~/.paper-forge/profile.md exists; if it does not, explain why it matters and ask whether to set it up.
9. Before writing the Profile, show the full content and target path, then wait for confirmation.
```

After installation, Codex should report the Skill directory, version or Git commit, invocation commands, Profile status, and the Zotero/PaperForge/Obsidian boundaries.
