import unittest

from anoplura.pylib.dimension import Dimension
from anoplura.rules.part_stats import PartStats
from tests.setup import parse


class TestPartStats(unittest.TestCase):
    def test_part_stats_01(self):
        self.assertEqual(
            parse(
                """Total body length of holotype, 1.35 mm, mean of series 1.36 mm,
                range 1.31-1.43 mm (n = 3)"""
            ),
            [
                PartStats(
                    start=0,
                    end=90,
                    _trait="part_stats",
                    _text="Total body length of holotype, 1.35 mm, mean of series 1.36 "
                    "mm, range 1.31-1.43 mm (n = 3)",
                    _paragraph=None,
                    part="body",
                    part_dims=[
                        Dimension(
                            dim="length",
                            units="mm",
                            low=1.35,
                            start=31,
                            end=38,
                        )
                    ],
                    specimen_type="holotype",
                    specimen_sex=None,
                    specimen_type_other=None,
                    part_mean=[
                        Dimension(
                            dim="length",
                            units="mm",
                            low=1.36,
                            start=55,
                            end=62,
                        )
                    ],
                    part_range=[
                        Dimension(
                            dim="length",
                            units="mm",
                            low=1.31,
                            high=1.43,
                            start=70,
                            end=82,
                        )
                    ],
                    part_sample_size=3,
                )
            ],
        )
