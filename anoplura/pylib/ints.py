"""Utilities to help process integers."""

import re

INT_RE = re.compile(r"\d+(?!\.)")
INT_RANGE = re.compile(r" (\d+) \s* (?:[\–\—\-])+ \s* (\d+) ", flags=re.VERBOSE)


def has_ints(text: str) -> bool:
    """Check if a string has ints."""
    match = INT_RE.search(text)
    return bool(match)


def get_ints(text: str) -> list[str]:
    """Find all ints in a string."""
    return [f" {i}" if len(i) == 1 else i for i in INT_RE.findall(text)]


def get_range(text: str) -> list[str] | None:
    """
    Expand a range of ints from a string.

    Ranges are inclusive.
    For instance: given (3, 6) return [3, 4, 5, 6].
    """
    if not (match := INT_RANGE.search(text)):
        return None
    low = int(match.group(1))
    high = int(match.group(2))
    return [f"{i:2d}" for i in range(low, high + 1)]
