# 阅读输出 / Reading Outputs

## 中文

Paper Forge 的输出不是网页界面，而是一个 Markdown 阅读包。每篇论文工作区都会生成 `README_FOR_READING.md`，它是阅读入口。

你通常只需要优先打开这些带编号的 Markdown 文件：

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

推荐打开方式：

- VS Code
- Codex 文件视图
- Obsidian
- Typora
- 任意 Markdown 阅读器

非编号文件的用途：

- `source/source_manifest.md`：记录来源材料、可访问性和限制。
- `analysis/profile_snapshot.md`：记录本次分析使用的 Profile 片段。
- `run_state.json`：记录脚本状态，主要供结构验证使用。

定位信息：

- 编号文件中的强结论、关键证据、机制判断和迁移判断应包含 `Source locator` 或 `Source basis`。
- 优先使用 PDF 页码、章节、图号、表号、实验编号、附录、DOI、arXiv ID 或 URL。
- 如果无法可靠定位页码，必须写 `PDF page Unknown` 或 `Source locator: Unknown`，不得编造。

## English

Paper Forge outputs are not a web UI. They are a Markdown reading package. Each paper workspace includes `README_FOR_READING.md` as the reading entry point.

You normally only need to open these numbered Markdown files first:

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

Recommended ways to open them:

- VS Code
- Codex file view
- Obsidian
- Typora
- Any Markdown reader

Non-numbered files:

- `source/source_manifest.md`: records source material, availability, and limitations.
- `analysis/profile_snapshot.md`: records the Profile content used for this run.
- `run_state.json`: records script state, mainly for structural validation.

Locator information:

- Strong conclusions, key evidence, mechanism judgments, and transfer judgments in numbered files should include `Source locator` or `Source basis`.
- Prefer PDF page, section, figure ID, table ID, experiment ID, appendix, DOI, arXiv ID, or URL.
- If exact pages are unavailable, write `PDF page Unknown` or `Source locator: Unknown`; never fabricate locators.
