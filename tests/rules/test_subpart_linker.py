import unittest

from anoplura.rules.count import Count
from anoplura.rules.description import Description
from anoplura.rules.seta import Seta
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
                        Count(start=22, end=33, count_low=4, count_group="each with"),
                        Seta(
                            start=39,
                            end=43,
                            seta="tergal abdominal setae",
                            seta_part="abdomen",
                        ),
                    ],
                    part="tergite",
                    number=[1, 2, 17],
                ),
                Count(
                    start=22,
                    end=33,
                    links=[Tergite(start=0, end=21, part="tergite", number=[1, 2, 17])],
                    count_low=4,
                    count_group="each with",
                ),
                Description(
                    start=34,
                    end=38,
                    links=[
                        Seta(
                            start=39,
                            end=43,
                            seta="tergal abdominal setae",
                            seta_part="abdomen",
                        )
                    ],
                    description="long",
                ),
                Seta(
                    start=39,
                    end=43,
                    links=[
                        Description(start=34, end=38, description="long"),
                        Tergite(start=0, end=21, part="tergite", number=[1, 2, 17]),
                    ],
                    seta="tergal abdominal setae",
                    seta_part="abdomen",
                ),
            ],
        )
