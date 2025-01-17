# import unittest
#
# from tests.setup import parse
#
#
# class TestSciName(unittest.TestCase):
#     def test_taxon_01(self):
#         self.assertEqual(
#             parse("females of L. CLAYTONI sp. nov., ."),
#             [
#                 {"sex": "female", "trait": "sex", "start": 0, "end": 7},
#                 {
#                     "taxon": "L. claytoni",
#                     "group": "anoplura",
#                     "trait": "taxon",
#                     "rank": "species",
#                     "start": 11,
#                     "end": 22,
#                 },
#             ],
#         )
#
#     def test_taxon_02(self):
#         self.assertEqual(
#             parse("four known species of Abrocomaphthirus"),
#             [
#                 {
#                     "taxon": "Abrocomaphthirus",
#                     "group": "anoplura",
#                     "trait": "taxon",
#                     "rank": "genus",
#                     "start": 22,
#                     "end": 38,
#                 }
#             ],
#         )
