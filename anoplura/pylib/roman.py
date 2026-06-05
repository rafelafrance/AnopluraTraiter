"""Roman numeral conversion utilities."""

import re

PATTERN = r"\b[mdclvi]+\b"

REGEX = re.compile(PATTERN, flags=re.IGNORECASE | re.VERBOSE)

PAREN = "(" + PATTERN + ")"
RANGE_REGEX = re.compile(
    PAREN + r" \s* (?:[\–\—\-])+ \s* " + PAREN, flags=re.IGNORECASE | re.VERBOSE
)

CONVERTER = (
    ("M", 1000),
    ("CM", 900),
    ("D", 500),
    ("CD", 400),
    ("C", 100),
    ("XC", 90),
    ("L", 50),
    ("XL", 40),
    ("X", 10),
    ("IX", 9),
    ("V", 5),
    ("IV", 4),
    ("I", 1),
)


def has_roman(text: str) -> bool:
    """Check if a string has a roman numeral in it."""
    match = REGEX.search(text)
    return bool(match)


def get_romans(text: str) -> list[str]:
    """Find all roman numerals in a string."""
    return REGEX.findall(text)


def get_range(text: str) -> list[str] | None:
    """Expand a range of roman numerals from a string."""
    if not (match := RANGE_REGEX.search(text)):
        return None
    low = match.group(1)
    high = match.group(2)
    return roman_range(low, high)


def roman_range(low: str, high: str) -> list[str]:
    """
    Expand a range of roman numerals.

    Ranges are inclusive.
    For instance: given ("III", "VI") return ["III", "IV", "V", "VI"].
    """
    i_low: int = from_roman(low)
    i_high: int = from_roman(high)
    numbers: list[str] = [to_roman(i) for i in range(i_low, i_high + 1)]
    return numbers


def to_roman(n: int) -> str:
    """Convert an integer to a uppercase Roman numeral string."""
    result = ""
    for roman, arabic in CONVERTER:
        while n >= arabic:
            result += roman
            n -= arabic
    return result


def from_roman(s: str) -> int:
    """Convert a Roman numeral string to an integer."""
    s = s.upper()
    result: int = 0
    i = 0
    for roman, arabic in CONVERTER:
        width = len(roman)
        while s[i : i + width] == roman:
            result += arabic
            i += width
    return result
