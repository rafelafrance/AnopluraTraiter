import unittest

from anoplura.rules.save.sternite_seta import SterniteSeta
from tests.setup import parse


class TestSterniteSeta(unittest.TestCase):
    def test_sternite_seta_01(self):
        self.assertEqual(
            parse("sternites 4-10 each with 6-8 StAS"),
            [
                SterniteSeta(
                    sternites=[4, 5, 6, 7, 8, 9, 10],
                    seta_count_low=6,
                    seta_count_high=8,
                    seta_count_group="each with",
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

    def test_sternite_seta_03(self):
        self.assertEqual(
            parse(" (VLAS) lateral to sternite 10 on each side."),
            [
                SterniteSeta(
                    sternites=[10],
                    seta="ventral lateral abdominal setae",
                    seta_count_group="on each side",
                    start=0,
                    end=42,
                )
            ],
        )
