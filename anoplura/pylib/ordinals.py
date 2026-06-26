"""Ordinal number conversion utilities."""

import re

CONVERTER = {
    # Numbers as words
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    # Ordinals
    "1st": 1,
    "2nd": 2,
    "3rd": 3,
    "4th": 4,
    "5th": 5,
    "6th": 6,
    "7th": 7,
    "8th": 8,
    "9th": 9,
    "10th": 10,
    "11th": 11,
    "12th": 12,
    "13th": 13,
    "14th": 14,
    "15th": 15,
    "16th": 16,
    "17th": 17,
    "18th": 18,
    "19th": 19,
    "20th": 20,
    # Ordinals as words
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
    "eleventh": 11,
    "twelfth": 12,
    "thirteenth": 13,
    "fourteenth": 14,
    "fifteenth": 15,
    "sixteenth": 16,
    "seventeenth": 17,
    "eighteenth": 18,
    "nineteenth": 19,
    "twentieth": 20,
}

PATTERN = rf"\b({'|'.join(c for c in CONVERTER)})\b"

REGEX = re.compile(PATTERN, flags=re.IGNORECASE | re.VERBOSE)

PAREN = "(" + PATTERN + ")"
RANGE_REGEX = re.compile(
    PAREN + r" \s* (?:[\–\—\-])+ \s* " + PAREN, flags=re.IGNORECASE | re.VERBOSE
)


def has_ordinal(text: str) -> bool:
    """Check if a string has an ordinal numeral in it."""
    match = REGEX.search(text)
    return bool(match)


def get_ordinals(text: str) -> list[str]:
    """Find all ordinal numbers in a string."""
    numbers = REGEX.findall(text)
    return [f"{CONVERTER[i]:2d}" for i in numbers]


def get_range(text: str) -> list[str] | None:
    """Expand a range of ordinal numbers from a string."""
    if not (match := RANGE_REGEX.search(text)):
        return None
    low = CONVERTER[match.group(1)]
    high = CONVERTER[match.group(2)]
    return [f"{i:2d}" for i in range(low, high + 1)]
