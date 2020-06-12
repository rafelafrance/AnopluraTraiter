"""Shared patterns."""

import re
from traiter.util import to_positive_int, to_positive_float


CLOSE = [')', ']']
COMMA = [',']
CROSS = ['x', '×']
DASH = ['–', '-', '––', '--']
EQ = ['=', '¼']
INT = r'^\d+$'
MM = ['millimeters', 'mm']
NUMBER = r'^\d+(\.\d*)?$'
OPEN = ['(', '[']
PLUS = ['+']
QUOTE = ['"', "'"]
SLASH = ['/']


def int_group(span):
    """Convert the span into a single integer."""
    if values := [t.text for t in span if re.match(INT, t.text)]:
        if (value := to_positive_int(values[0])) is not None:
            return dict(
                start=span.start_char,
                end=span.end_char,
                value=value)
    return {}


def float_group(span):
    """Convert the span into a single float."""
    if values := [t.text for t in span if re.match(NUMBER, t.text)]:
        if (value := to_positive_float(values[0])) is not None:
            return dict(
                start=span.start_char,
                end=span.end_char,
                value=value)
    return {}
