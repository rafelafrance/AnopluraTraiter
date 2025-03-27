import unittest

from anoplura.rules.sternite_seta import SterniteSeta
from tests.setup import parse


class TestSternite(unittest.TestCase):
    def test_sternite_seta_01(self):
        self.assertEqual(
            parse("sternites 4-10 each with 6-8 StAS"),
            [
                SterniteSeta(
                    sternites=[4, 5, 6, 7, 8, 9, 10],
                    seta_count_low=6,
                    seta_count_high=8,
                    seta="sternal abdominal setae",
                    start=0,
                    end=33,
                )
            ],
        )

    def test_sternite_seta_02(self):
        self.assertEqual(
            parse("sternite 1 lacking setae;"),
            [
                SterniteSeta(
                    sternites=[1], seta_count_low=0, seta="missing", start=0, end=24
                )
            ],
        )
