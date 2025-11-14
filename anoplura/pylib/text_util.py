import ftfy
import regex as re


def shorten(text: str) -> str:
    """Collapse all whitespace in a string."""
    return " ".join(text.split())


def compress(text: str) -> str:
    """Collapse whitespace in a string but keep lines."""
    lines = [" ".join(ln.split()) for ln in text.splitlines()]
    string = "\n".join(ln for ln in lines if ln)
    return string


def to_positive_float(value: str | float) -> float | None:
    """Convert a string to a float stripping bad characters from the string first."""
    if isinstance(value, str):
        value = re.sub(r"[^\d./]", "", value) if value else ""
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


def clean_text(
    text: str,
    trans: dict[int, str] | None = None,
    replace: dict[str, str] | None = None,
    *,
    eol_hyphens: bool = False,
) -> str:
    """Clean text before trait extraction."""
    text = text if text else ""

    # Handle uncommon mojibake
    if trans:
        text = text.translate(trans)

    if replace:
        for old, new in replace.items():
            text = text.replace(old, new)

    text = compress(text)  # Space normalize

    text = re.sub(r"\N{SHY}\s*", "", text)  # Remove soft-hyphens

    # Latex symbols
    text = re.sub(r" \\text\{ ([^}]+) \}", r"\1", text, flags=re.VERBOSE)  # Characters
    text = re.sub(r"\^\{\\circ\}", r"°", text)  # Degree symbol
    text = re.sub(r"\\pm", r"±", text)  # Plus/minus symbol
    text = re.sub(r"''", r'"', text)  # Minutes symbol

    # Remove HTML tags
    text = re.sub(r"< [^>]+ >", "", text, flags=re.VERBOSE)

    # Remove figure notations
    text = re.sub(
        r" \s* \( [^)]* fig [^)]+ \) ", "", text, flags=re.IGNORECASE | re.VERBOSE
    )
    text = re.sub(r" figs?\.? \s* \d+(-\d+)? ", "", text, flags=re.I | re.X)

    # Join hyphenated words when they are at the end of a line
    if eol_hyphens:
        text = re.sub(r"([a-z])-\s+([a-z])", r"\1\2", text, flags=re.IGNORECASE)

    text = ftfy.fix_text(text)  # Handle common mojibake

    # Remove control characters
    text = re.sub(r"\p{Cc}+", " ", text)

    return text
