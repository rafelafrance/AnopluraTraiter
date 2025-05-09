import unittest

from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestSubpart(unittest.TestCase):
    def test_subpart_01(self):
        self.assertEqual(
            parse("dorsal head suture"),
            [Subpart(subpart="dorsal head suture", start=0, end=18)],
        )
