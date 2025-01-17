# """Test setae count trait matcher."""
# import unittest
#
# from tests.setup import test_traits
#
#
# class TestSetaeCount(unittest.TestCase):
#     """Test setae count trait matcher."""
#
#     def test_setae_count_01(self):
#         self.assertEqual(
#             test_traits("One long Dorsal Principal Head Seta (DPHS)"),
#             [
#                 {
#                     "count": 1,
#                     "body_part": "seta",
#                     "seta": "dorsal principal head seta",
#                     "trait": "seta_count",
#                     "start": 0,
#                     "end": 42,
#                 }
#             ],
#         )
#
#     def test_setae_count_02(self):
#         self.assertEqual(
#             test_traits("no Dorsal Mesothoracic Setae (DMsS);"),
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
#             test_traits("with pair of long setae"),
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
#             test_traits("with 16–18 contiguous curved setae on each side;"),
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
#             test_traits("One long and one tiny seta immediately posterior to"),
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
