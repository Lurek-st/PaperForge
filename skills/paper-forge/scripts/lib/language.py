from __future__ import annotations

from typing import Any

from .profile import load_profile_preferences


VALID_LANGUAGE_MODES = {"auto", "zh", "en", "bilingual"}


NOTE_TITLE_CATALOG = {
    "en": {
        "00": "Source, Metadata, Profile Snapshot",
        "01": "Problem, Prior Limitation, Actual Contribution",
        "02": "Mechanism, Method, Causal Chain",
        "03": "Claims, Evidence, Limitations, Unproven Parts",
        "04": "Transfer Analysis, User Research Relevance, Project Ideas",
        "05": "Feynman Recall, Self-Explanation, Open Questions",
    },
    "zh": {
        "00": "来源、元数据与 Profile 快照",
        "01": "论文定位、原有局限与真实贡献",
        "02": "方法机制、输入输出与因果链",
        "03": "主张证据、局限与未证部分",
        "04": "迁移分析、研究关联与项目想法",
        "05": "费曼回忆、自我解释与开放问题",
    },
    "bilingual": {
        "00": "来源、元数据与 Profile 快照 · Source, Metadata, Profile Snapshot",
        "01": "论文定位、原有局限与真实贡献 · Problem, Prior Limitation, Actual Contribution",
        "02": "方法机制、输入输出与因果链 · Mechanism, Method, Causal Chain",
        "03": "主张证据、局限与未证部分 · Claims, Evidence, Limitations, Unproven Parts",
        "04": "迁移分析、研究关联与项目想法 · Transfer Analysis, User Research Relevance, Project Ideas",
        "05": "费曼回忆、自我解释与开放问题 · Feynman Recall, Self-Explanation, Open Questions",
    },
}


UI_TEXT = {
    "en": {
        "navigation": "Navigation",
        "home": "Home",
        "previous": "Previous",
        "next": "Next",
        "recommended_reading_order": "Recommended Reading Order",
        "quick_entry": "Quick Entry",
        "source_and_zotero": "Source and Zotero",
        "problem_entry": "Problem, prior limitation, actual contribution",
        "mechanism_entry": "Mechanism, method, causal chain",
        "claims_entry": "Claims, evidence, limitations",
        "transfer_entry": "Transfer to user projects",
        "recall_entry": "Active recall and self-explanation",
        "zotero_source_item": "Zotero Source Item",
        "reading_purpose": "Reading Purpose",
        "source_boundary": "Boundary",
        "source_links": "Source Links",
        "core_workspace": "Core Workspace",
        "metadata_warnings": "Metadata Warnings",
    },
    "zh": {
        "navigation": "导航",
        "home": "主页",
        "previous": "上一篇",
        "next": "下一篇",
        "recommended_reading_order": "推荐阅读顺序",
        "quick_entry": "快速入口",
        "source_and_zotero": "来源与 Zotero",
        "problem_entry": "论文定位、原有局限与真实贡献",
        "mechanism_entry": "方法机制、输入输出与因果链",
        "claims_entry": "主张证据、局限与未证部分",
        "transfer_entry": "迁移分析、研究关联与项目想法",
        "recall_entry": "费曼回忆与自我解释",
        "zotero_source_item": "Zotero 来源条目",
        "reading_purpose": "阅读目的",
        "source_boundary": "边界说明",
        "source_links": "来源链接",
        "core_workspace": "核心工作区",
        "metadata_warnings": "元数据警告",
    },
    "bilingual": {
        "navigation": "导航 | Navigation",
        "home": "主页 | Home",
        "previous": "上一篇 | Previous",
        "next": "下一篇 | Next",
        "recommended_reading_order": "推荐阅读顺序 | Recommended Reading Order",
        "quick_entry": "快速入口 | Quick Entry",
        "source_and_zotero": "来源与 Zotero | Source and Zotero",
        "problem_entry": "论文定位、原有局限与真实贡献 | Problem, Prior Limitation, Actual Contribution",
        "mechanism_entry": "方法机制、输入输出与因果链 | Mechanism, Method, Causal Chain",
        "claims_entry": "主张证据、局限与未证部分 | Claims, Evidence, Limitations",
        "transfer_entry": "迁移分析、研究关联与项目想法 | Transfer Analysis, Project Ideas",
        "recall_entry": "费曼回忆与自我解释 | Active Recall",
        "zotero_source_item": "Zotero 来源条目 | Zotero Source Item",
        "reading_purpose": "阅读目的 | Reading Purpose",
        "source_boundary": "边界说明 | Boundary",
        "source_links": "来源链接 | Source Links",
        "core_workspace": "核心工作区 | Core Workspace",
        "metadata_warnings": "元数据警告 | Metadata Warnings",
    },
}


def normalize_language_mode(value: object, *, fallback: str = "auto") -> str:
    text = str(value or "").strip().lower()
    aliases = {
        "": fallback,
        "auto": "auto",
        "automatic": "auto",
        "zh": "zh",
        "cn": "zh",
        "chinese": "zh",
        "中文": "zh",
        "en": "en",
        "english": "en",
        "英文": "en",
        "bilingual": "bilingual",
        "zh-en": "bilingual",
        "en-zh": "bilingual",
        "中英": "bilingual",
        "中英对照": "bilingual",
    }
    normalized = aliases.get(text, fallback)
    return normalized if normalized in VALID_LANGUAGE_MODES else fallback


def resolve_language_settings(
    config: dict[str, Any],
    *,
    explicit_language: str | None = None,
    explicit_obsidian_language: str | None = None,
) -> dict[str, str]:
    profile_preferences = load_profile_preferences()
    language_config = config.get("language", {})

    requested_analysis = normalize_language_mode(
        explicit_language
        or profile_preferences.get("default_output_language")
        or language_config.get("default_output_language"),
        fallback="auto",
    )
    fallback_analysis = normalize_language_mode(language_config.get("fallback_output_language"), fallback="en")
    resolved_analysis = fallback_analysis if requested_analysis == "auto" else requested_analysis

    requested_obsidian = normalize_language_mode(
        explicit_obsidian_language
        or explicit_language
        or profile_preferences.get("obsidian_note_language")
        or language_config.get("obsidian_note_language")
        or requested_analysis,
        fallback="auto",
    )
    if requested_obsidian == "auto":
        resolved_obsidian = resolved_analysis if resolved_analysis in {"zh", "en", "bilingual"} else "en"
    else:
        resolved_obsidian = requested_obsidian

    return {
        "analysis_language_requested": requested_analysis,
        "analysis_language": resolved_analysis,
        "obsidian_note_language_requested": requested_obsidian,
        "obsidian_note_language": resolved_obsidian,
    }
