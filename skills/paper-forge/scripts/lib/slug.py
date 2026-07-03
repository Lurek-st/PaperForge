import re
import unicodedata
from datetime import date
from typing import Optional


def safe_slug(value: str, fallback: str = "paper", max_length: int = 80) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text)
    ascii_text = re.sub(r"-{2,}", "-", ascii_text).strip("-")
    if not ascii_text:
        ascii_text = fallback
    return ascii_text[:max_length].strip("-") or fallback


def dated_slug(value: str, run_date: Optional[date] = None) -> str:
    current = run_date or date.today()
    return f"{current.isoformat()}_{safe_slug(value)}"
