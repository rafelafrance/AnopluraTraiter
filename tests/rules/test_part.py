import unittest

from anoplura.rules.part import Part
from anoplura.rules.part_morphology import PartMorphology
from tests.setup import parse


class TestPart(unittest.TestCase):
    def test_part_01(self):
        self.assertEqual(
            parse("Legs progressively larger"),
            [
                Part(part="leg", start=0, end=4),
                PartMorphology(
                    start=5, end=25, part="leg", morphology=["progressively larger"]
                ),
            ],
        )
