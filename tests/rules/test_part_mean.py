import unittest

from anoplura.rules.part_mean import PartMean
from tests.setup import parse


class TestPartMean(unittest.TestCase):
    def test_part_mean_01(self):
        self.assertEqual(
            parse("""mean, 0.194 mm"""),
            [PartMean(start=0, end=14, mean=0.194, units="mm")],
        )
