import unittest

from tests.setup import parse


class TestText(unittest.TestCase):
    def test_text_00(self) -> None:
        parse(
            """
            hind femora with relatively broad spur-like ridge posteriorly
            """
        )
