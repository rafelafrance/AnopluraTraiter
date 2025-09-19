import unittest

from anoplura.pylib.dimension import Dimension
from anoplura.rules.part import Part
from anoplura.rules.sex import Sex
from anoplura.rules.size import Size
from tests.setup import parse


class TestPhraseLinker(unittest.TestCase):
    def test_phrase_linker_01(self) -> None:
        self.maxDiff = None
        self.assertEqual(
            parse("Male: Total body length, 1.02 mm."),
            [
                Sex(start=0, end=4, sex="male"),
                Part(
                    start=6,
                    end=16,
                    links=[
                        Size(
                            start=17,
                            end=33,
                            dims=[
                                Dimension(
                                    dim="length",
                                    units="mm",
                                    low=1.02,
                                    start=17,
                                    end=33,
                                )
                            ],
                        )
                    ],
                    part="total body",
                ),
                Size(
                    start=17,
                    end=33,
                    links=[Part(start=6, end=16, part="total body")],
                    dims=[
                        Dimension(dim="length", units="mm", low=1.02, start=17, end=33)
                    ],
                ),
            ],
        )
