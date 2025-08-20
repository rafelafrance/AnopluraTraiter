import unittest

from anoplura.rules.part_morphology import PartMorphology
from anoplura.rules.plate import Plate
from anoplura.rules.seta import Seta
from anoplura.rules.seta_count import SetaCount
from anoplura.rules.sternite import Sternite
from anoplura.rules.subpart import Subpart
from anoplura.rules.subpart_morphology import SubpartMorphology
from tests.setup import parse


class TestLinkPart(unittest.TestCase):
    def test_link_part_01(self) -> None:
        self.assertEqual(
            parse(
                """
                Thoracic sternal plate club-shaped with rounded anterolateral margins,
                broadly acuminate anterior apex, and elongate posterior extension
                with squarish posterior apex.
                """
            ),
            [
                Plate(
                    start=0,
                    end=22,
                    part="plate",
                    position="thoracic sternal",
                ),
                PartMorphology(
                    start=23,
                    end=34,
                    part="plate",
                    morphology=["club-shaped"],
                ),
                SubpartMorphology(
                    start=40,
                    end=47,
                    subpart="margin",
                    part="plate",
                    position="anterolateral",
                    morphology=["rounded"],
                ),
                Subpart(
                    start=48,
                    end=69,
                    subpart="margin",
                    part="plate",
                    position="anterolateral",
                ),
                SubpartMorphology(
                    start=71,
                    end=88,
                    subpart="apex",
                    part="plate",
                    position="anterior",
                    morphology=["broadly acuminate"],
                ),
                Subpart(
                    start=89,
                    end=102,
                    subpart="apex",
                    part="plate",
                    position="anterior",
                ),
                SubpartMorphology(
                    start=108,
                    end=116,
                    subpart="extension",
                    part="plate",
                    position="posterior",
                    morphology=["elongate"],
                ),
                Subpart(
                    start=117,
                    end=136,
                    subpart="extension",
                    part="plate",
                    position="posterior",
                ),
                SubpartMorphology(
                    start=142,
                    end=150,
                    subpart="apex",
                    part="plate",
                    position="posterior",
                    morphology=["squarish"],
                ),
                Subpart(
                    start=151,
                    end=165,
                    subpart="apex",
                    part="plate",
                    position="posterior",
                ),
            ],
        )

    def test_link_part_02(self) -> None:
        self.assertEqual(
            parse("sternite 2 with 6 sternal abdominal setae"),
            [
                Sternite(
                    start=0,
                    end=10,
                    part="sternite",
                    which=[2],
                ),
                SetaCount(
                    start=16,
                    end=17,
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                    count_low=6,
                ),
                Seta(
                    start=18,
                    end=41,
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                    part="sternite",
                    which=[2],
                ),
            ],
        )

    def test_link_part_03(self) -> None:
        self.assertEqual(
            parse("Sternite 1 with 4 DLAS; Sternite 2 with 9 StAS"),
            [
                Sternite(
                    start=0,
                    end=10,
                    part="sternite",
                    which=[1],
                ),
                SetaCount(
                    start=16,
                    end=17,
                    seta="dorsal lateral abdominal setae",
                    seta_part="abdomen",
                    count_low=4,
                ),
                Seta(
                    start=18,
                    end=22,
                    seta="dorsal lateral abdominal setae",
                    seta_part="abdomen",
                    part="sternite",
                    which=[1],
                ),
                Sternite(
                    start=24,
                    end=34,
                    part="sternite",
                    which=[2],
                ),
                SetaCount(
                    start=40,
                    end=41,
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                    count_low=9,
                ),
                Seta(
                    start=42,
                    end=46,
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                    part="sternite",
                    which=[2],
                ),
            ],
        )
