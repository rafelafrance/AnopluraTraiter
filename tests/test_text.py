import unittest

from tests.setup import parse


class TestText(unittest.TestCase):
    def test_text_00(self) -> None:
        parse(
            """
            3 rows of setae immediately anterior to gonopods IX on each side
            """
        )
