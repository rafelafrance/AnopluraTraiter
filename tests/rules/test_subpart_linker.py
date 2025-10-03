import unittest

from anoplura.rules.base import Link
from anoplura.rules.count import Count
from anoplura.rules.seta import Seta
from anoplura.rules.shape import Shape
from anoplura.rules.tergite import Tergite
from tests.setup import parse


class TestSubpartLinker(unittest.TestCase):
    def test_subpart_linker_01(self) -> None:
        self.assertEqual(
            parse("Tergites 1, 2, and 17 each with 4 long TeAS;"),
            [
                Tergite(
                    start=0,
                    end=21,
                    links=[
                        Link(trait="count", start=22, end=33),
                        Link(trait="seta", start=39, end=43),
                    ],
                    part="tergite",
                    number=[1, 2, 17],
                ),
                Count(start=22, end=33, count_low=4, count_group="each with"),
                Shape(start=34, end=38, shape="long"),
                Seta(
                    start=39,
                    end=43,
                    links=[Link(trait="shape", start=34, end=38)],
                    seta="tergal abdominal setae",
                    seta_part="abdomen",
                ),
            ],
        )
