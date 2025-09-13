import unittest

from anoplura.rules.part_count import PartCount
from anoplura.rules.sternite import Sternite
from anoplura.rules.tergite import Tergite
from tests.setup import parse


class TestPartCount(unittest.TestCase):
    def test_part_count_01(self) -> None:
        self.assertEqual(
            parse("3 long, narrow sternites"),
            [
                PartCount(
                    start=0,
                    end=14,
                    part="sternite",
                    count_low=3,
                    description="long, narrow",
                ),
                Sternite(
                    start=15,
                    end=24,
                    part="sternite",
                ),
            ],
        )

    def test_part_count_02(self) -> None:
        self.assertEqual(
            parse("2 elongate sternites (nos. 2 and 3)"),
            [
                PartCount(
                    start=0,
                    end=10,
                    part="sternite",
                    which=[2, 3],
                    count_low=2,
                    description="elongate",
                ),
                Sternite(
                    start=11,
                    end=35,
                    part="sternite",
                    number=[2, 3],
                ),
            ],
        )

    def test_part_count_03(self) -> None:
        self.assertEqual(
            parse("2 relatively broad tergites (nos. 1 and 2)"),
            [
                PartCount(
                    start=0,
                    end=18,
                    part="tergite",
                    which=[1, 2],
                    count_low=2,
                    description="relatively broad",
                ),
                Tergite(
                    start=19,
                    end=42,
                    part="tergite",
                    number=[1, 2],
                ),
            ],
        )
