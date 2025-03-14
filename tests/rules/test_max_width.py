# """Test max body width trait matcher."""
# # pylint: disable=missing-function-docstring, too-many-public-methods
# import unittest
#
# from tests.setup import parse
#
#
# class TestMaxWidth(unittest.TestCase):
#     """Test louse size trait matcher."""
#
#     def test_max_width_01(self):
#         self.assertEqual(
#             parse("Maximum head width, 0.150–0.163 mm (mean, 0.17 mm, n = 4)."),
#             [
#                 {
#                     "n": 4,
#                     "mean": 0.17,
#                     "mean_units": "mm",
#                     "low": 0.150,
#                     "high": 0.163,
#                     "length_units": "mm",
#                     "body_part": "head",
#                     "trait": "max_width",
#                     "start": 0,
#                     "end": 57,
#                 }
#             ],
#         )
#
#     def test_length_02(self):
#         self.assertEqual(
#             parse("Maximum thorax width, 0.193–0.228 mm (mean, 0.210, n = 4)."),
#             [
#                 {
#                     "body_part": "thorax",
#                     "n": 4,
#                     "mean": 0.21,
#                     "low": 0.193,
#                     "high": 0.228,
#                     "length_units": "mm",
#                     "trait": "max_width",
#                     "start": 0,
#                     "end": 57,
#                 }
#             ],
#         )
