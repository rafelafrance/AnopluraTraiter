import unittest

from anoplura.rules.save.seta_row import SetaRow
from tests.setup import parse


class TestSetaRow(unittest.TestCase):
    def test_seta_row_01(self):
        self.assertEqual(
            parse("row 1 with 4 DCAS,"),
            [
                SetaRow(
                    seta_rows=[1],
                    seta="dorsal central abdominal setae",
                    seta_count_low=4,
                    start=0,
                    end=17,
                ),
            ],
        )

    def test_seta_row_02(self):
        self.assertEqual(
            parse("rows 2 and 3 each with 5 DCAS,"),
            [
                SetaRow(
                    seta_rows=[2, 3],
                    seta="dorsal central abdominal setae",
                    seta_count_group="each with",
                    seta_count_low=5,
                    start=0,
                    end=29,
                ),
            ],
        )

    def test_seta_row_03(self):
        self.assertEqual(
            parse("rows 4-7 each with 6-7 DCAS,"),
            [
                SetaRow(
                    seta="dorsal central abdominal setae",
                    seta_rows=[4, 5, 6, 7],
                    seta_count_low=6,
                    seta_count_high=7,
                    seta_count_group="each with",
                    start=0,
                    end=27,
                ),
            ],
        )
