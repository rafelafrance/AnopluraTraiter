"""Roman numeral conversion utilities."""

import re

LENIENT_PATTERN = (
    r" \b m{0,4} (?:cm|cd|d?c{0,4})? (?:xc|xl|l?x{0,4})? (?:ix|iv|v?i{0,4})? \b "
)
STRICT_PATTERN = (
    r" \b m{0,4} (?:cm|cd|d?c{0,3})? (?:xc|xl|l?x{0,3})? (?:ix|iv|v?i{0,3})? \b "
)

STRICT_RE = re.compile(STRICT_PATTERN, flags=re.IGNORECASE | re.VERBOSE)

STRICT_PAREN = "(" + STRICT_PATTERN + ")"
ROMAN_RANGE = re.compile(
    STRICT_PAREN + r" \s* (?:[\–\—\-])+ \s* " + STRICT_PAREN,
    flags=re.IGNORECASE | re.VERBOSE,
)

CONVERTER = (
    ("m", 1000),
    ("cm", 900),
    ("d", 500),
    ("cd", 400),
    ("c", 100),
    ("xc", 90),
    ("l", 50),
    ("xl", 40),
    ("x", 10),
    ("ix", 9),
    ("v", 5),
    ("iv", 4),
    ("i", 1),
)


def has_roman(text: str) -> bool:
    """Check if a string has a roman numeral in it."""
    match = STRICT_RE.search(text)
    return bool(match) and len(match.group(0)) > 0


def get_romans(text: str) -> list[str]:
    """Find all roman numerals in a string."""
    return STRICT_RE.findall(text)


def get_range(text: str) -> list[str] | None:
    """Expand a range of roman numerals from a string."""
    if not (match := ROMAN_RANGE.search(text)):
        return None
    low = match.group(1)
    high = match.group(2)
    return roman_range(low, high)


def roman_range(low: str, high: str) -> list[str]:
    """
    Expand a range of roman numerals.

    Ranges are inclusive.
    For instance: given ("iii", "vi") return ["iii", "iv", "v", "vi"].
    """
    i_low: int = from_roman(low)
    i_high: int = from_roman(high)
    numbers: list[str] = [to_roman(i) for i in range(i_low, i_high + 1)]
    return numbers


def to_roman(n: int) -> str:
    """Convert an integer to a lowercase Roman numeral string."""
    result = ""
    for roman, arabic in CONVERTER:
        while n >= arabic:
            result += roman
            n -= arabic
    return result


def from_roman(s: str) -> int:
    """Convert a Roman numeral string to an integer."""
    s = s.lower()
    result: int = 0
    i = 0
    for roman, arabic in CONVERTER:
        width = len(roman)
        while s[i : i + width] == roman:
            result += arabic
            i += width
    return result
