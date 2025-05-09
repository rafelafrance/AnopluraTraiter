import unittest

from anoplura.pylib.dimension import Dimension
from anoplura.rules.part_size import PartSize
from tests.setup import parse


class TestPartSize(unittest.TestCase):
    def test_part_size_01(self):
        self.assertEqual(
            parse("Total body length, 1.02 mm."),
            [
                PartSize(
                    part="body",
                    part_dims=[
                        Dimension(
                            dim="length",
                            units="mm",
                            low=1.02,
                            start=11,
                            end=27,
                        )
                    ],
                    start=0,
                    end=27,
                )
            ],
        )

    def test_part_size_02(self):
        self.assertEqual(
            parse("Total body length of allotype 1.75 mm,"),
            [
                PartSize(
                    part="body",
                    specimen_type="allotype",
                    part_dims=[
                        Dimension(dim="length", units="mm", low=1.75, start=30, end=37)
                    ],
                    start=0,
                    end=37,
                )
            ],
        )

    def test_part_size_03(self):
        self.assertEqual(
            parse("Total body length of holotype, 1.35 mm,"),
            [
                PartSize(
                    part="body",
                    specimen_type="holotype",
                    part_dims=[
                        Dimension(dim="length", units="mm", low=1.35, start=31, end=38)
                    ],
                    start=0,
                    end=38,
                )
            ],
        )
