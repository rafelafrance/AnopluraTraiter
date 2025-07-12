import unittest

from anoplura.rules.seta import Seta
from anoplura.rules.seta_count import SetaCount
from tests.setup import parse


class TestSetaCount(unittest.TestCase):
    def test_seta_row_01(self):
        self.assertEqual(
            parse("4 DCAS,"),
            [
                SetaCount(
                    seta="dorsal central abdominal setae",
                    count_low=4,
                    start=0,
                    end=1,
                ),
                Seta(start=2, end=6, seta="dorsal central abdominal setae"),
            ],
        )

    def test_seta_row_02(self):
        self.assertEqual(
            parse("5 pairs of DCAS,"),
            [
                SetaCount(
                    seta="dorsal central abdominal setae",
                    count_low=5,
                    count_group="pairs of",
                    start=0,
                    end=10,
                ),
                Seta(start=11, end=15, seta="dorsal central abdominal setae"),
            ],
        )

    def test_seta_row_03(self):
        self.assertEqual(
            parse("6-7 DCAS,"),
            [
                SetaCount(
                    seta="dorsal central abdominal setae",
                    count_low=6,
                    count_high=7,
                    start=0,
                    end=3,
                ),
                Seta(start=4, end=8, seta="dorsal central abdominal setae"),
            ],
        )
