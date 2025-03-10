import unittest

from anoplura.rules.seta_count import SetaCount
from tests.setup import parse


class TestSetaCount(unittest.TestCase):
    def test_seta_count_01(self):
        self.assertEqual(
            parse("1 DMHS"),
            [
                SetaCount(seta="dorsal marginal head setae", low=1, start=0, end=6),
            ],
        )


#     def test_setae_count_02(self):
#         self.assertEqual(
#             parse("no Dorsal Mesothoracic Setae (DMsS);"),
#             [
#                 {
#                     "count": 0,
#                     "seta": "dorsal mesothoracic setae",
#                     "body_part": "seta",
#                     "trait": "seta_count",
#                     "start": 0,
#                     "end": 35,
#                 }
#             ],
#         )
#
#     def test_setae_count_03(self):
#         self.assertEqual(
#             parse("with pair of long setae"),
#             [
#                 {
#                     "body_part": "seta",
#                     "present": True,
#                     "seta": "setae",
#                     "group": "pair of",
#                     "trait": "seta_count",
#                     "start": 5,
#                     "end": 23,
#                 }
#             ],
#         )
#
#     def test_setae_count_04(self):
#         self.assertEqual(
#             parse("with 16–18 contiguous curved setae on each side;"),
#             [
#                 {
#                     "low": 16,
#                     "high": 18,
#                     "seta": "setae",
#                     "group": "each side",
#                     "body_part": "seta",
#                     "trait": "seta_count",
#                     "start": 5,
#                     "end": 47,
#                 }
#             ],
#         )
#
#     def test_setae_count_05(self):
#         self.assertEqual(
#             parse("One long and one tiny seta immediately posterior to"),
#             [
#                 {
#                     "seta": "seta",
#                     "count": 2,
#                     "body_part": "seta",
#                     "trait": "seta_count",
#                     "start": 0,
#                     "end": 26,
#                 }
#             ],
#         )
