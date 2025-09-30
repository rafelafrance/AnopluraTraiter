import unittest

from anoplura.rules.base import Link
from anoplura.rules.elevation import Elevation
from anoplura.rules.part import Part
from anoplura.rules.seta import Seta
from anoplura.rules.size import Dimension, Size
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestSize(unittest.TestCase):
    def test_size_01(self) -> None:
        """It handles values larger than 1000."""
        self.assertEqual(
            parse("""Elevation: 0–3600 m"""),
            [
                Elevation(
                    start=0, end=19, elevation=0.0, elevation_high=3600.0, units="m"
                )
            ],
        )

    def test_size_02(self) -> None:
        """It handles two dimensions."""
        self.assertEqual(
            parse("""total body length 30–60 × 10-20 cm,"""),
            [
                Part(
                    start=0,
                    end=10,
                    links=[Link(trait="size", start=11, end=34)],
                    part="total body",
                ),
                Size(
                    start=11,
                    end=34,
                    dims=[
                        Dimension(
                            dim="length",
                            units="cm",
                            low=30.0,
                            high=60.0,
                            start=11,
                            end=23,
                        ),
                        Dimension(
                            dim="width",
                            units="cm",
                            low=10.0,
                            high=20.0,
                            start=26,
                            end=34,
                        ),
                    ],
                ),
            ],
        )

    def test_size_03(self) -> None:
        """It handles an extra plus sign."""
        self.assertEqual(
            parse("""leg length 10–30+ cm,"""),
            [
                Part(
                    start=0,
                    end=3,
                    links=[Link(trait="size", start=4, end=20)],
                    part="leg",
                ),
                Size(
                    start=4,
                    end=20,
                    dims=[
                        Dimension(
                            dim="length",
                            units="cm",
                            low=10.0,
                            high=30.0,
                            start=4,
                            end=20,
                        )
                    ],
                ),
            ],
        )

    def test_size_04(self) -> None:
        self.assertEqual(
            parse("""head width, 1.02 mm."""),
            [
                Part(
                    start=0,
                    end=4,
                    links=[Link(trait="size", start=5, end=20)],
                    part="head",
                ),
                Size(
                    start=5,
                    end=20,
                    dims=[
                        Dimension(
                            dim="width",
                            units="mm",
                            low=1.02,
                            start=5,
                            end=20,
                        )
                    ],
                ),
            ],
        )

    def test_size_05(self) -> None:
        self.assertEqual(
            parse("""(DPTS) length, 0.123 mm;"""),
            [
                Seta(
                    start=1,
                    end=5,
                    links=[Link(trait="size", start=7, end=23)],
                    seta="dorsal principal thoracic setae",
                    seta_part="thorax",
                ),
                Size(
                    start=7,
                    end=23,
                    dims=[
                        Dimension(
                            dim="length",
                            units="mm",
                            low=0.123,
                            start=7,
                            end=23,
                        )
                    ],
                ),
            ],
        )

    def test_size_06(self) -> None:
        self.assertEqual(
            parse("""posterior apex length, 0.123 mm;"""),
            [
                Subpart(
                    start=0,
                    end=14,
                    links=[Link(trait="size", start=15, end=31)],
                    subpart="posterior apex",
                ),
                Size(
                    start=15,
                    end=31,
                    dims=[
                        Dimension(dim="length", units="mm", low=0.123, start=15, end=31)
                    ],
                ),
            ],
        )
