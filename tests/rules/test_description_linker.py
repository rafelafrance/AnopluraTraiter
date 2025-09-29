import unittest

from anoplura.rules.description import Description
from anoplura.rules.part import Part
from anoplura.rules.seta import Seta
from tests.setup import parse


class TestDescriptionLinker(unittest.TestCase):
    def test_description_linker_01(self) -> None:
        self.assertEqual(
            parse("setae present except on legs."),
            [
                Seta(
                    start=0,
                    end=5,
                    links=[
                        Description(start=6, end=23, description="present except on"),
                        Part(start=24, end=28, part="leg"),
                    ],
                    seta="setae",
                ),
                Description(
                    start=6,
                    end=23,
                    links=[
                        Seta(_trait="seta", _text="setae", start=0, end=5, seta="setae")
                    ],
                    description="present except on",
                ),
                Part(
                    start=24,
                    end=28,
                    links=[Seta(start=0, end=5, seta="setae")],
                    part="leg",
                ),
            ],
        )
