import unittest

from anoplura.rules.base import Link
from anoplura.rules.mean import Mean
from anoplura.rules.measure import Measure
from anoplura.rules.part import Part
from anoplura.rules.sample_size import SampleSize
from anoplura.rules.size import Dimension, Size
from tests.setup import parse


class TestStatsLinker(unittest.TestCase):
    def test_stats_linker_01(self) -> None:
        self.assertEqual(
            parse("""Maximum head width, 0.185–0.200 mm (mean, 0.194 mm, n = 3)."""),
            [
                Measure(start=0, end=7, measure="maximum"),
                Part(
                    start=8,
                    end=12,
                    links=[
                        Link(trait="measure", start=0, end=7),
                        Link(trait="size", start=13, end=34),
                        Link(trait="mean", start=36, end=50),
                        Link(trait="sample_size", start=52, end=57),
                    ],
                    part="head",
                ),
                Size(
                    start=13,
                    end=34,
                    dims=[
                        Dimension(
                            dim="width",
                            units="mm",
                            low=0.185,
                            high=0.2,
                            start=13,
                            end=34,
                        )
                    ],
                ),
                Mean(
                    start=36,
                    end=50,
                    mean=[
                        Dimension(dim="width", units="mm", low=0.194, start=42, end=50)
                    ],
                ),
                SampleSize(start=52, end=57, sample_size=3),
            ],
        )

    def test_stats_linker_02(self) -> None:
        self.assertEqual(
            parse("""Thorax: Maximum width, 0.285–0.295 mm (n = 2)."""),
            [
                Part(
                    start=0,
                    end=6,
                    links=[
                        Link(trait="measure", start=8, end=15),
                        Link(trait="size", start=16, end=37),
                        Link(trait="sample_size", start=39, end=44),
                    ],
                    part="thorax",
                ),
                Measure(start=8, end=15, measure="maximum"),
                Size(
                    start=16,
                    end=37,
                    dims=[
                        Dimension(
                            dim="width",
                            units="mm",
                            low=0.285,
                            high=0.295,
                            start=16,
                            end=37,
                        )
                    ],
                ),
                SampleSize(start=39, end=44, sample_size=2),
            ],
        )

    def test_stats_linker_03(self) -> None:
        self.assertEqual(
            parse("""maximum width of head, 0.190 mm."""),
            [
                Measure(start=0, end=13, measure="maximum"),
                Part(
                    start=17,
                    end=21,
                    links=[
                        Link(trait="measure", start=0, end=7),
                        Link(trait="dimension", start=8, end=13),
                        Link(trait="size", start=23, end=32),
                    ],
                    part="head",
                ),
                Size(
                    start=23,
                    end=32,
                    dims=[
                        Dimension(dim="width", units="mm", low=0.19, start=23, end=32)
                    ],
                ),
            ],
        )

    def test_stats_linker_04(self) -> None:
        self.assertEqual(
            parse("""Total body length: 0.99–1.16 mm; mean, 1.09 mm (n = 4)."""),
            [
                Part(
                    start=0,
                    end=10,
                    links=[
                        Link(trait="size", start=11, end=31),
                        Link(trait="mean", start=33, end=46),
                        Link(trait="sample_size", start=48, end=53),
                    ],
                    part="total body",
                ),
                Size(
                    start=11,
                    end=31,
                    dims=[
                        Dimension(
                            dim="length",
                            units="mm",
                            low=0.99,
                            high=1.16,
                            start=11,
                            end=31,
                        )
                    ],
                ),
                Mean(
                    start=33,
                    end=46,
                    mean=[
                        Dimension(dim="length", units="mm", low=1.09, start=39, end=46)
                    ],
                ),
                SampleSize(start=48, end=53, sample_size=4),
            ],
        )

    def test_stats_linker_05(self) -> None:
        self.assertEqual(
            parse(
                "Total body length of holotype, 1.35 mm, mean of "
                "series 1.36 mm, range 1.31–1.43 mm (n = 3)."
            ),
            [],
        )
