# import unittest
#
# from anoplura.rules.count import Count
# from tests.setup import parse
#
#
# class TestCount(unittest.TestCase):
#     def test_count_01(self):
#         self.assertEqual(
#             parse("6"),
#             [
#                 Count(start=0, end=1, count_low=6),
#             ],
#         )
#
#     def test_count_02(self):
#         self.assertEqual(
#             parse("2 pairs of"),
#             [
#                 Count(start=0, end=10, count_low=2, count_group="pairs of"),
#             ],
#         )
#
#     def test_count_03(self):
#         self.assertEqual(
#             parse("2-3 pairs of"),
#             [
#                 Count(
#                     start=0, end=12, count_low=2, count_high=3, count_group="pairs of"
#                 ),
#             ],
#         )
