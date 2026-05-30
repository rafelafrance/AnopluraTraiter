"""Utilities to help process integers."""

import re

INT_RE = re.compile(r"\d+(?!\.)")
INT_RANGE = re.compile(r" (\d+) \s* (?:[\–\—\-])+ \s* (\d+) ", flags=re.VERBOSE)


def has_ints(text: str) -> bool:
    """Check if a string has ints."""
    match = INT_RE.search(text)
    return bool(match)


def get_ints(text: str) -> list[int]:
    """Find all ints in a string."""
    return [int(i) for i in INT_RE.findall(text)]


def get_range(text: str) -> list[int] | None:
    """
    Expand a range of ints from a string.

    Ranges are inclusive.
    For instance: given (3, 6) return [3, 4, 5, 6].
    """
    if not (match := INT_RANGE.search(text)):
        return None
    low = int(match.group(1))
    high = int(match.group(2))
    return list(range(low, high + 1))
