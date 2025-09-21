import unittest

from anoplura.rules.description import Description
from anoplura.rules.part import Part
from tests.setup import parse


class TestPart(unittest.TestCase):
    def test_part_01(self) -> None:
        self.assertEqual(
            parse("Legs progressively larger"),
            [
                Part(
                    start=0,
                    end=4,
                    links=[
                        Description(start=5, end=25, description="progressively larger")
                    ],
                    part="leg",
                ),
                Description(
                    start=5,
                    end=25,
                    links=[Part(start=0, end=4, part="leg")],
                    description="progressively larger",
                ),
            ],
        )

    def test_part_02(self) -> None:
        self.assertEqual(
            parse("Antennae 5-segmented"),
            [
                Part(
                    start=0,
                    end=8,
                    links=[Description(start=9, end=20, description="5-segmented")],
                    part="antenna",
                ),
                Description(
                    start=9,
                    end=20,
                    links=[Part(start=0, end=8, part="antenna")],
                    description="5-segmented",
                ),
            ],
        )

    def test_part_03(self) -> None:
        self.assertEqual(
            parse("head with anterolateral lobe on each side"),
            [
                Part(
                    start=0,
                    end=4,
                    links=[
                        Description(
                            start=5,
                            end=41,
                            description="with anterolateral lobe on each side",
                        )
                    ],
                    part="head",
                ),
                Description(
                    start=5,
                    end=41,
                    links=[Part(start=0, end=4, part="head")],
                    description="with anterolateral lobe on each side",
                ),
            ],
        )

    def test_part_04(self) -> None:
        self.assertEqual(
            parse("Mesothoracic spiracle"),
            [
                Part(start=0, end=21, part="mesothoracic spiracle"),
            ],
        )
