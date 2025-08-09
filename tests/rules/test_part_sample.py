import unittest

from anoplura.rules.part_sample import PartSample
from tests.setup import parse


class TestPartSample(unittest.TestCase):
    def test_part_sample_01(self):
        self.assertEqual(
            parse("""n = 3)."""), [PartSample(start=0, end=5, sample_size=3)]
        )
