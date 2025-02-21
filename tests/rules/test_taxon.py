import unittest

from traiter.pylib.rules.number import Number

from anoplura.pylib.rules.taxon import Taxon
from tests.setup import parse


class TestSciName(unittest.TestCase):
    def test_taxon_01(self):
        self.assertEqual(
            parse("females of L. CLAYTONI sp. nov., ."),
            [
                # {"sex": "female", "trait": "sex", "start": 0, "end": 7},
                Taxon(
                    taxon="Lemurpediculus claytoni",
                    rank="species",
                    group="anoplura",
                    start=11,
                    end=22,
                ),
            ],
        )

    def test_taxon_02(self):
        self.assertEqual(
            parse("four known species of Abrocomaphthirus"),
            [
                Number(start=0, end=4, number=4, is_fraction=None, is_word=True),
                Taxon(
                    taxon="Abrocomaphthirus",
                    rank="genus",
                    group="anoplura",
                    start=22,
                    end=38,
                ),
            ],
        )
