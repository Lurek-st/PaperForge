from __future__ import annotations

import unicodedata


_SUSPICIOUS_SUBSTRINGS = (
    "Ã",
    "Â",
    "â€",
    "â€™",
    "â€œ",
    "â€\x9d",
    "Ð",
    "Ñ",
    "Ø",
    "ç\x8e",
    "å°",
    "æ\x98",
)


def normalize_unicode_text(value: object) -> str:
    text = unicodedata.normalize("NFC", str(value or ""))
    return text.replace("\ufeff", "")


def _suspicious_score(text: str) -> int:
    score = 0
    for char in text:
        codepoint = ord(char)
        if 0x80 <= codepoint <= 0x9F:
            score += 3
        elif char == "\ufffd":
            score += 3
    for marker in _SUSPICIOUS_SUBSTRINGS:
        score += text.count(marker) * 2
    return score


def _looks_like_mojibake(text: str) -> bool:
    return _suspicious_score(text) > 0


def _decode_roundtrip(text: str, encoding: str) -> str | None:
    try:
        return text.encode(encoding).decode("utf-8")
    except UnicodeError:
        return None


def repair_mojibake(text: object) -> str:
    original = normalize_unicode_text(text)
    if not original or not _looks_like_mojibake(original):
        return original

    original_score = _suspicious_score(original)
    best = original
    best_score = original_score

    for encoding in ("latin-1", "cp1252"):
        candidate = _decode_roundtrip(original, encoding)
        if not candidate:
            continue
        candidate = normalize_unicode_text(candidate)
        candidate_score = _suspicious_score(candidate)
        if candidate_score < best_score:
            best = candidate
            best_score = candidate_score

    return best


def safe_unicode_text(value: object) -> str:
    return repair_mojibake(value)


def safe_unicode_text_with_warning(value: object, *, label: str) -> tuple[str, str | None]:
    normalized = normalize_unicode_text(value)
    repaired = repair_mojibake(normalized)
    if _looks_like_mojibake(normalized) and repaired == normalized:
        return repaired, f"Could not safely repair suspected mojibake in {label}: {normalized!r}"
    return repaired, None
