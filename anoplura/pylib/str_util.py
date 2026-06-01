"""String manipulation and parsing utilities."""

import re


def compress(text: str) -> str:
    """Collapse all whitespace in a string."""
    return " ".join(text.split())


def clean_text(text: str) -> str:
    """Fix markup nonsense from the OCR engines."""
    text = re.sub(r"<br/?>", "\n", text)
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    text = text.strip()
    return text
