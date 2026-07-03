# 手动安装 / Manual Installation

## 中文

手动安装只复制单一 Skill 目录，不安装 Plugin、MCP、Hook、浏览器扩展或系统服务。

步骤：

1. 找到当前 Codex 用户级 Skill 目录。通常是 `$CODEX_HOME/skills`；如果未设置 `CODEX_HOME`，通常是 `~/.codex/skills`。
2. 将本仓库的 `skills/paper-forge/` 复制到该目录。
3. 确认目标路径类似 `~/.codex/skills/paper-forge/SKILL.md`。
4. 重新加载或重启 Codex，使 Skill 可被发现。
5. 运行 Profile 初始化脚本可创建模板：

```bash
python skills/paper-forge/scripts/init_profile.py
```

不要把真实 Profile 放进仓库。真实 Profile 应位于 `~/.paper-forge/profile.md`。

## English

Manual installation copies only the single Skill directory. It does not install a Plugin, MCP server, Hook, browser extension, or system service.

Steps:

1. Find the current Codex user-level Skill directory. It is usually `$CODEX_HOME/skills`; when `CODEX_HOME` is not set, it is usually `~/.codex/skills`.
2. Copy this repository's `skills/paper-forge/` directory into that location.
3. Confirm that the destination resembles `~/.codex/skills/paper-forge/SKILL.md`.
4. Reload or restart Codex so the Skill can be discovered.
5. Run the Profile initialization script to create the template:

```bash
python skills/paper-forge/scripts/init_profile.py
```

Do not put the real Profile in the repository. The real Profile belongs at `~/.paper-forge/profile.md`.
