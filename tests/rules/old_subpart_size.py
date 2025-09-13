import unittest

from anoplura.pylib.dimension import Dimension
from anoplura.rules.subpart import Subpart
from anoplura.rules.subpart_size import SubpartSize
from tests.setup import parse


class TestSubpartSize(unittest.TestCase):
    def test_subpart_size_01(self) -> None:
        self.assertEqual(
            parse("""posterior apex length, 0.123 mm;"""),
            [
                Subpart(
                    start=0,
                    end=14,
                    subpart="apex",
                    position="posterior",
                ),
                SubpartSize(
                    start=15,
                    end=31,
                    subpart="apex",
                    position="posterior",
                    dims=[
                        Dimension(
                            dim="length",
                            units="mm",
                            low=0.123,
                            start=15,
                            end=31,
                        )
                    ],
                ),
            ],
        )
