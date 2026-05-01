import re


def compress(text: str) -> str:
    """Collapse all whitespace in a string."""
    return " ".join(text.split())


def dedent(text: str) -> str:
    """Remove leading and trailing spaces from each line."""
    lines = [ln.strip() for ln in text.splitlines() if ln]
    return "\n".join(lines)


def strip_json_fences(text: str) -> str:
    """
    Remove markdown code fences wrapping JSON content.

    Handles any language tag (json, python, text, etc.), extra whitespace,
    and varying numbers of backticks. Strips the outermost matching fence
    pair if present, otherwise returns the text unchanged.
    """
    stripped = text.strip()
    fence_re = re.compile(r"^(`{3,})(\w*)?\n(.*?)\n\s*\1\s*$", re.DOTALL)
    match = fence_re.match(stripped)
    if match:
        return match.group(3).strip()
    return stripped


def to_positive_float(value: str | float) -> float | None:
    """Convert a string to a float stripping bad characters from the string first."""
    if isinstance(value, str):
        value = re.sub(r"[^\d./]", "", value) or ""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def to_positive_int(value: str | float) -> int | None:
    """Convert a string to an int stripping bad characters from the string first."""
    if isinstance(value, str):
        value = re.sub(r"[^\d./]", "", value) if value else ""
        value = re.sub(r"\.$", "", value)
    try:
        return int(value)
    except (ValueError, TypeError):
        return None
