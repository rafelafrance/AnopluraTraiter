import unittest

from anoplura.rules.subpart_count import SubpartCount
from tests.setup import parse


class TestSubpartCount(unittest.TestCase):
    def test_subpart_count_01(self):
        self.assertEqual(
            parse("Antennae 5-segmented"),
            [
                SubpartCount(
                    part="antenna",
                    subpart="segment",
                    count=5,
                    start=0,
                    end=20,
                )
            ],
        )
