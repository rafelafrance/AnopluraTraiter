import unittest

from anoplura.pylib.dimension import Dimension
from anoplura.rules.mean import Mean
from tests.setup import parse


class TestMean(unittest.TestCase):
    def test_mean_01(self) -> None:
        self.assertEqual(
            parse("""mean, 0.194 mm"""),
            [
                Mean(
                    start=0,
                    end=14,
                    mean=[
                        Dimension(dim="length", units="mm", low=0.194, start=6, end=14)
                    ],
                )
            ],
        )
