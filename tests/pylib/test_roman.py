import unittest

from anoplura.pylib import roman


class TestFixValues(unittest.TestCase):
    # ---------------------------------------------------------------------
    def test_has_roman_01(self) -> None:
        assert roman.has_roman("IV")

    def test_has_roman_02(self) -> None:
        assert roman.has_roman("plate iv")

    def test_has_roman_03(self) -> None:
        assert roman.has_roman("plate IV")

    def test_has_roman_04(self) -> None:
        assert roman.has_roman("iv")
