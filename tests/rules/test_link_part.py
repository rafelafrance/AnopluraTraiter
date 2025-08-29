import unittest

from anoplura.rules.seta import Seta
from anoplura.rules.seta_count import SetaCount
from anoplura.rules.sternite import Sternite
from tests.setup import parse


class TestLinkPart(unittest.TestCase):
    def test_link_part_01(self) -> None:
        self.assertEqual(
            parse("sternite 2 with 6 sternal abdominal setae"),
            [
                Sternite(
                    start=0,
                    end=10,
                    part="sternite",
                    which=[2],
                ),
                SetaCount(
                    start=16,
                    end=17,
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                    count_low=6,
                ),
                Seta(
                    start=18,
                    end=41,
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                    part="sternite",
                    which=[2],
                ),
            ],
        )

    def test_link_part_02(self) -> None:
        self.assertEqual(
            parse("Sternite 1 with 4 DLAS; Sternite 2 with 9 StAS"),
            [
                Sternite(
                    start=0,
                    end=10,
                    part="sternite",
                    which=[1],
                ),
                SetaCount(
                    start=16,
                    end=17,
                    seta="dorsal lateral abdominal setae",
                    seta_part="abdomen",
                    count_low=4,
                ),
                Seta(
                    start=18,
                    end=22,
                    seta="dorsal lateral abdominal setae",
                    seta_part="abdomen",
                    part="sternite",
                    which=[1],
                ),
                Sternite(
                    start=24,
                    end=34,
                    part="sternite",
                    which=[2],
                ),
                SetaCount(
                    start=40,
                    end=41,
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                    count_low=9,
                ),
                Seta(
                    start=42,
                    end=46,
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                    part="sternite",
                    which=[2],
                ),
            ],
        )
