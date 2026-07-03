# 先设置 Profile / Profile First

## 中文

Profile 是 Paper Forge 判断“这篇论文是否与你有关”和“哪些部分可能迁移到你的研究方向”的本地依据。它不会让系统全知，也不会替代论文证据；它只改变相关性、迁移价值、术语解释和默认输出语言的判断背景。

Profile 存储在：

```text
~/.paper-forge/profile.md
```

它位于 Skill 包外部，因此更新或重新安装 Skill 时仍然保留。它不是模型记忆，也不会从过去对话中自动恢复。

你可以通过两种方式设置：

- 对话式设置：告诉 Codex 研究背景、方向、应用场景、判断论文时最重视的约束和语言偏好。Codex 必须先展示完整内容和路径，等待你确认后再写入。
- 手动编辑：复制 `skills/paper-forge/assets/profile-template.md` 到 `~/.paper-forge/profile.md` 后自行编辑。

不要写入密码、账号凭据、私钥、住址、身份证件或与论文分析无关的敏感个人信息。

工业具身智能示例见：

```text
skills/paper-forge/assets/profile-industrial-embodied-ai-example.md
```

## English

The Profile is Paper Forge's local basis for judging whether a paper is relevant to you and which parts may transfer to your research direction. It does not make the system omniscient and does not replace paper evidence; it changes the context for relevance, transfer value, terminology, and default output language.

Profile location:

```text
~/.paper-forge/profile.md
```

It lives outside the Skill package, so it survives Skill updates or reinstallation. It is not model memory and is not automatically recovered from previous conversations.

You can set it up in two ways:

- Conversational setup: tell Codex your research background, directions, applications, paper-judgment constraints, and language preference. Codex must show the complete proposed content and path, then wait for your confirmation before writing.
- Manual editing: copy `skills/paper-forge/assets/profile-template.md` to `~/.paper-forge/profile.md` and edit it yourself.

Do not put passwords, account credentials, private keys, addresses, identity documents, or unrelated sensitive personal information into the Profile.

Industrial embodied intelligence example:

```text
skills/paper-forge/assets/profile-industrial-embodied-ai-example.md
```
