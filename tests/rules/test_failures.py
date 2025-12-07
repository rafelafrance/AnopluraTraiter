import unittest

from anoplura.rules.count import Count
from anoplura.rules.group import Group
from anoplura.rules.position import Position
from anoplura.rules.relative_size import RelativeSize
from anoplura.rules.rule import Link
from anoplura.rules.seta import Seta
from anoplura.rules.size_description import SizeDescription
from tests.setup import parse


class TestFailure(unittest.TestCase):
    def test_failure_01(self) -> None:
        self.assertEqual(
            parse("""
                1 fairly long ventral principal head seta (VPHS) ventrally on each side.
                """),
            [
                Count(start=0, end=1, count_low=1),
                SizeDescription(start=2, end=13, size_description="fairly long"),
                Seta(
                    start=14,
                    end=48,
                    links=[
                        Link(trait="size_description", start=2, end=13),
                        Link(trait="position", start=49, end=58),
                        Link(trait="count", start=0, end=1),
                        Link(trait="group", start=59, end=71),
                    ],
                    seta="ventral principal head setae",
                    seta_part="head",
                ),
                Position(start=49, end=58, position="ventrally"),
                Group(start=59, end=71, group="on each side"),
            ],
        )

    # def test_failure_02(self) -> None:
    #     self.assertEqual(
    #         parse("""sternite 1 lacking setae;"""),
    #         [
    #             Sternite(
    #                 start=0,
    #                 end=10,
    #                 links=[Link(trait="seta", start=19, end=24)],
    #                 part="sternite",
    #                 number=[1],
    #             ),
    #             Count(start=11, end=18, count_low=0),
    #             Seta(
    #                 start=19,
    #                 end=24,
    #                 links=[Link(trait="count", start=11, end=18)],
    #                 seta="setae",
    #             ),
    #         ],
    #     )

    def test_failure_03(self) -> None:
        self.assertEqual(
            parse("""some central StAS distinctly shorter than lateral StAS."""),
            [
                Position(start=5, end=12, position="central"),
                Seta(
                    start=13,
                    end=17,
                    links=[Link(trait="position", start=5, end=12)],
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                ),
                RelativeSize(start=18, end=41, relative_size="distinctly shorter than"),
                Position(start=42, end=49, position="lateral"),
                Seta(
                    start=50,
                    end=54,
                    links=[
                        Link(trait="relative_size", start=18, end=41),
                        Link(trait="position", start=42, end=49),
                    ],
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                ),
            ],
        )
