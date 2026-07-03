# 使用 Codex 安装 / Install With Codex

## 中文

将下面提示词复制给 Codex，并把 `<REPOSITORY_URL>` 替换成真实仓库地址：

```text
请从这个 GitHub 仓库安装 Paper Forge Skill：

<REPOSITORY_URL>

在进行任何修改前：
1. 检查 README.md、Skill 目录、SKILL.md 和所有脚本。
2. 说明将安装哪些文件以及安装到哪里。
3. 只安装单一 Paper Forge Skill。
4. 不要安装任何 Plugin、MCP server、Hook、浏览器扩展、系统服务或无关依赖。
5. 不要运行来自仓库或外部来源的任意脚本。
6. 不要修改系统级配置。
7. 在本地或官方文档中确认当前 Codex 用户级 Skill 位置后再使用。
8. 验证安装后该 Skill 可以被发现。
9. 安装后检查我的长期 Paper Forge Profile 是否存在于 ~/.paper-forge/profile.md。
10. 如果不存在，解释 Profile 为什么重要，并询问是否现在设置。
11. 不要编造个人 Profile 信息。向我询问信息，或让我选择手动设置。
12. 在写入 Profile 前，展示完整拟写入内容和目标路径，然后等待我确认。
```

安装后，Codex 不应只说“完成”。它应报告 Skill 安装目录、版本或 Git commit、如何调用 Paper Forge、Profile 是否存在、Profile 作用和如何配置。

## English

Copy this prompt into Codex and replace `<REPOSITORY_URL>` with the real repository URL:

```text
Install the Paper Forge Skill from this GitHub repository:

<REPOSITORY_URL>

Before making changes:
1. Inspect README.md, the skill directory, SKILL.md, and all scripts.
2. Explain which files will be installed and where.
3. Install only the single Paper Forge Skill.
4. Do not install any Plugin, MCP server, Hook, browser extension, system service, or unrelated dependency.
5. Do not run arbitrary scripts from the repository or from external sources.
6. Do not modify system-wide configuration.
7. Use the current official Codex user-level Skill location after verifying it locally or from official documentation.
8. Verify that the Skill becomes discoverable after installation.
9. After installation, check whether my persistent Paper Forge Profile exists at ~/.paper-forge/profile.md.
10. If it does not exist, explain why the Profile matters and offer to set it up now.
11. Do not invent personal profile information. Ask me for the information or let me choose manual setup.
12. Before writing my Profile, show the exact content and destination path, then wait for my confirmation.
```

After installation, Codex should not merely say "done". It should report the installed Skill directory, version or Git commit, how to invoke Paper Forge, whether the Profile exists, what the Profile is for, and how to configure it.
