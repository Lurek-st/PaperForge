# 使用 Claude Code 安装 / Install With Claude Code

## 中文

如果你的 Claude Code 环境支持本地 Skill 目录，可以采用与手动安装相同的保守原则：只复制 `skills/paper-forge/`，不要安装 Plugin、MCP、Hook、浏览器扩展、系统服务或无关依赖。

建议提示词：

```text
请检查这个仓库中的 Paper Forge Skill。只安装 skills/paper-forge/ 这一项。安装前说明将复制哪些文件和目标路径。不要运行任意脚本，不要安装额外依赖，不要修改系统级配置。安装后检查 ~/.paper-forge/profile.md 是否存在；如果不存在，只解释 Profile 作用并询问我是否要设置，不要编造个人信息。
```

如果目标环境没有可发现的 Skill 机制，则仍可把本仓库作为规范和脚本集合使用，但不应把它包装成 Plugin 或多 Agent 系统。

## English

If your Claude Code environment supports a local Skill directory, use the same conservative principle as manual installation: copy only `skills/paper-forge/`, and do not install any Plugin, MCP server, Hook, browser extension, system service, or unrelated dependency.

Suggested prompt:

```text
Inspect the Paper Forge Skill in this repository. Install only skills/paper-forge/. Before installing, explain which files will be copied and where. Do not run arbitrary scripts, install extra dependencies, or modify system-wide configuration. After installation, check whether ~/.paper-forge/profile.md exists; if it does not, explain what the Profile is for and ask whether I want to set it up. Do not invent personal information.
```

If the target environment has no discoverable Skill mechanism, the repository can still be used as a specification and script set, but it should not be packaged as a Plugin or multi-agent system.
