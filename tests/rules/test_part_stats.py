import unittest

from anoplura.pylib.dimension import Dimension
from anoplura.rules.part_stats import PartStats
from tests.setup import parse


class TestPartStats(unittest.TestCase):
    def test_part_stats_01(self):
        self.assertEqual(
            parse("""Maximum head width, 0.185–0.200 mm (mean, 0.194 mm, n = 3)."""),
            [
                PartStats(
                    start=0,
                    end=58,
                    measure="maximum head width",
                    mean=0.194,
                    mean_units="mm",
                    sample_size=3,
                    range=Dimension(
                        dim="width", units="mm", low=0.185, high=0.2, start=13, end=34
                    ),
                )
            ],
        )

    def test_part_stats_02(self):
        self.assertEqual(
            parse("""Thorax: Maximum width, 0.285–0.295 mm (n = 2)."""),
            [
                PartStats(
                    start=0,
                    end=45,
                    measure="maximum thorax width",
                    sample_size=2,
                    range=Dimension(
                        dim="width", units="mm", low=0.285, high=0.295, start=16, end=37
                    ),
                )
            ],
        )

    def test_part_stats_03(self):
        self.assertEqual(
            parse("""maximum width of head, 0.190 mm."""),
            [
                PartStats(
                    start=0,
                    end=32,
                    measure="maximum head width",
                    range=Dimension(
                        dim="width", units="mm", low=0.19, start=23, end=32
                    ),
                )
            ],
        )

    def test_part_stats_04(self):
        self.assertEqual(
            parse("""Total body length: 0.99–1.16 mm; mean, 1.09 mm (n = 4)."""),
            [
                PartStats(
                    start=0,
                    end=54,
                    measure="total body length",
                    mean=1.09,
                    mean_units="mm",
                    sample_size=4,
                    range=Dimension(
                        dim="length", units="mm", low=0.99, high=1.16, start=19, end=31
                    ),
                )
            ],
        )

    # def test_part_stats_05(self):
    #     self.assertEqual(
    #         parse("""Total body length of holotype, 1.35 mm, mean of
    #                 series 1.36 mm, range 1.31–1.43 mm (n ⫽ 3)."""),
    #         [
    #             PartStats(
    #                 start=0,
    #                 end=54,
    #                 measure="total body length",
    #                 mean=1.09,
    #                 mean_units="mm",
    #                 sample_size=4,
    #                 range=Dimension(
    #                    dim="length", units="mm", low=0.99, high=1.16, start=19, end=31
    #                 ),
    #             )
    #         ],
    #     )
