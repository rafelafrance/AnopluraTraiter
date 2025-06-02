import unittest

from anoplura.rules.part import Part
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestSubpart(unittest.TestCase):
    def test_subpart_01(self):
        self.assertEqual(
            parse("dorsal head suture"),
            [Subpart(subpart="dorsal head suture", start=0, end=18)],
        )

    def test_subpart_02(self):
        self.assertEqual(
            parse("head with anterolateral lobe on each side"),
            [
                Part(start=0, end=4, part="head"),
                Subpart(
                    start=10,
                    end=41,
                    subpart="anterolateral lobe",
                    subpart_group="on each side",
                ),
            ],
        )
