import unittest

from anoplura.rules.part import Part
from anoplura.rules.part_description import PartDescription
from tests.setup import parse


class TestPart(unittest.TestCase):
    def test_part_01(self):
        self.assertEqual(
            parse("Legs progressively larger"),
            [
                Part(part="leg", start=0, end=4),
                PartDescription(
                    start=5, end=25, part="leg", shape=["progressively larger"]
                ),
            ],
        )
