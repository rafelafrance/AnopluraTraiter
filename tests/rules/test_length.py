# """Test length trait matcher."""
# # pylint: disable=missing-function-docstring, too-many-public-methods
# import unittest
#
# from tests.setup import parse
#
#
# class TestLength(unittest.TestCase):
#     """Test length trait matcher."""
#
#     def test_length_01(self):
#         self.assertEqual(
#             parse("Total body length: 0.99–1.16 mm; mean, 1.09 mm (n = 4)."),
#             [
#                 {
#                     "n": 4,
#                     "mean": 1.09,
#                     "mean_units": "mm",
#                     "body_part": "body",
#                     "low": 0.99,
#                     "high": 1.16,
#                     "length_units": "mm",
#                     "trait": "total_length",
#                     "start": 0,
#                     "end": 54,
#                 }
#             ],
#         )
#
#     def test_length_02(self):
#         self.assertEqual(
#             parse(
#                 """
#                 DPTS length 0.137 mm (n = 1) (only one unbroken DPTS present).
#                 """
#             ),
#             [
#                 {
#                     "n": 1,
#                     "low": 0.137,
#                     "length_units": "mm",
#                     "seta_abbrev": "dorsal principal thoracic seta",
#                     "trait": "length",
#                     "start": 0,
#                     "end": 28,
#                 },
#                 {
#                     "end": 52,
#                     "start": 48,
#                     "trait": "seta_abbrev",
#                     "seta_abbrev": "dorsal principal thoracic seta",
#                 },
#             ],
#         )
