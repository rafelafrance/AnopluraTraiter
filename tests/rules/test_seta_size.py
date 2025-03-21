import unittest

from anoplura.rules.seta_size import SetaSize
from anoplura.rules.size import Dimension
from tests.setup import parse


class TestSetaCount(unittest.TestCase):
    def test_seta_size_01(self):
        self.assertEqual(
            parse("(DPTS) length, 0.123 mm;"),
            [
                SetaSize(
                    seta="dorsal principal thoracic setae",
                    dims=[
                        Dimension(
                            dim="length",
                            low=0.123,
                            units="mm",
                            start=7,
                            end=23,
                        ),
                    ],
                    start=0,
                    end=23,
                ),
            ],
        )
