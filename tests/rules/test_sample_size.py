import unittest

from anoplura.rules.sample_size import SampleSize
from tests.setup import parse


class TestSampleSize(unittest.TestCase):
    def test_sample_size_01(self) -> None:
        self.assertEqual(
            parse("""(n = 3)."""), [SampleSize(start=1, end=6, sample_size=3)]
        )
