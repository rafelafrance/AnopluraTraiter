import unittest

from anoplura.pylib.dimension import Dimension
from anoplura.rules.part import Part
from anoplura.rules.part_size import PartSize
from tests.setup import parse


class TestPartSize(unittest.TestCase):
    def test_part_size_01(self) -> None:
        self.assertEqual(
            parse("""spiracle diameter, 0.023 mm."""),
            [
                Part(start=0, end=8, part="spiracle"),
                PartSize(
                    start=9,
                    end=28,
                    part="spiracle",
                    dims=[
                        Dimension(
                            dim="diameter", units="mm", low=0.023, start=9, end=28
                        )
                    ],
                ),
            ],
        )
