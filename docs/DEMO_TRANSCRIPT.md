# 演示记录 / Demo Transcript

## 中文

以下论文是虚构示例，不是真实论文：

```text
Title: Latency-Aware Visual Servoing For Modular Factory Robots
Authors: Fictional Example Team
Year: 2026
```

用户：请安装 Paper Forge。

Agent：我会只安装单一 `paper-forge` Skill，不安装 Plugin、MCP、Hook 或系统服务。安装后我会检查 `~/.paper-forge/profile.md`。

Agent：Paper Forge 已安装。未发现 Profile。建议先创建长期研究 Profile，它位于 `~/.paper-forge/profile.md`，用于相关性和迁移判断。你可以现在对话式设置、手动编辑模板，或暂时跳过。

用户：我的方向是工业具身智能、智能制造自动化、机器人和机器视觉。我关心实时性、安全可靠、Sim2Real、PLC / MES / SCADA 集成和维护成本。默认中文输出。

Agent：我整理了拟写入的 Profile，并展示完整内容和路径 `~/.paper-forge/profile.md`。请确认是否写入。

用户：确认。

Agent：已写入 Profile。

用户：`$paper-forge screen ./fictional-servoing.pdf`

Agent：我创建工作区，记录来源清单，并生成 `analysis/01_triage.md`。初步建议是 `deep`，但标记了真实工厂验证和长期稳定性为 Unknown。

用户：`$paper-forge deep ./fictional-servoing.pdf`

Agent：我完成主张账本、贡献图谱、机制 Mermaid、证据审计、迁移分析和最终简报。结论：该虚构论文的机制对工业视觉伺服有潜在价值，但真实产线延迟、传感器噪声和安全恢复证据不足。建议进入 Recall。

用户：`$paper-forge recall`

Agent：问题 1：请用自己的话解释：这篇论文为什么认为旧视觉伺服方法不够？

用户：因为旧方法精度不够，新方法用了更好的模型。

Agent：你的回答缺少两个关键环节：旧方法不足不只是精度，还包括通信延迟下的控制稳定性；“更好的模型”需要说明如何改变信息流或控制目标。请补充因果链。

用户：我不会，告诉我答案。

Agent：完整解释是：该虚构论文声称旧方法在模块化工厂中没有显式建模相机到控制器的延迟变化，导致视觉误差被过时状态驱动；作者引入延迟感知状态估计和控制更新，使控制器使用更接近执行时刻的状态。但真实工厂长周期验证仍是 Unknown。

## English

The following paper is fictional and is not a real paper:

```text
Title: Latency-Aware Visual Servoing For Modular Factory Robots
Authors: Fictional Example Team
Year: 2026
```

User: Install Paper Forge.

Agent: I will install only the single `paper-forge` Skill, with no Plugin, MCP server, Hook, or system service. After installation, I will check `~/.paper-forge/profile.md`.

Agent: Paper Forge is installed. No Profile was found. I recommend creating a persistent research Profile first. It lives at `~/.paper-forge/profile.md` and supports relevance and transfer judgment. You can set it up conversationally, edit the template manually, or skip for now.

User: My directions are industrial embodied intelligence, intelligent manufacturing automation, robotics, and machine vision. I care about real-time constraints, safety and reliability, Sim2Real, PLC / MES / SCADA integration, and maintenance cost. Default to Chinese output.

Agent: I drafted the proposed Profile and showed the full content and path `~/.paper-forge/profile.md`. Please confirm whether to write it.

User: Confirm.

Agent: Profile written.

User: `$paper-forge screen ./fictional-servoing.pdf`

Agent: I created the workspace, recorded the source manifest, and generated `analysis/01_triage.md`. The preliminary recommendation is `deep`, but real-factory validation and long-run stability are marked Unknown.

User: `$paper-forge deep ./fictional-servoing.pdf`

Agent: I completed the claim ledger, contribution map, Mermaid mechanism, evidence audit, transfer analysis, and final brief. Conclusion: this fictional paper's mechanism may be relevant to industrial visual servoing, but evidence for real production latency, sensor noise, and safety recovery is insufficient. Recall is recommended next.

User: `$paper-forge recall`

Agent: Question 1: In your own words, explain why this paper says prior visual servoing methods were insufficient.

User: Because old methods were not accurate enough, and the new method uses a better model.

Agent: Your answer misses two key links: the prior limitation is not only accuracy but control stability under communication latency; "better model" needs to explain how information flow or control objective changes. Please complete the causal chain.

User: I do not know. Tell me the answer.

Agent: The full explanation is: the fictional paper claims prior methods did not explicitly model camera-to-controller latency variation in modular factories, so visual error could be driven by stale state. The authors introduce latency-aware state estimation and control updates so the controller uses a state closer to execution time. However, long-run real-factory validation remains Unknown.
