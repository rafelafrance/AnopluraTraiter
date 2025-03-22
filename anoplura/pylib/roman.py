STRICT_PATTERN = r"^m{0,4}(cm|cd|d?c{0,3})?(xc|xl|l?x{0,3})?(ix|iv|v?i{0,3})?$"
LENIENT_PATTERN = r"^m{0,4}(cm|cd|d?c{0,4})?(xc|xl|l?x{0,4})?(ix|iv|v?i{0,4})?$"

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


def to_roman(n: int) -> str:
    result = ""
    for roman, arabic in CONVERTER:
        while n >= arabic:
            result += roman
            n -= arabic
    return result


def from_roman(s: str) -> int:
    s = s.lower()
    result: int = 0
    i = 0
    for roman, arabic in CONVERTER:
        width = len(roman)
        while s[i : i + width] == roman:
            result += arabic
            i += width
    return result
