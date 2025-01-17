# """Test body part trait matcher."""
# import unittest
#
# from tests.setup import test_traits
#
#
# class TestBodyPart(unittest.TestCase):
#     """Test body part trait matcher."""
#
#     # def test_body_part_01(self):
#     #     self.assertEqual(
#     #         test_traits("fourth segment"),
#     #         [
#     #             {
#     #                 "body_part": "fourth segment",
#     #                 "trait": "body_part",
#     #                 "start": 0,
#     #                 "end": 14,
#     #             }
#     #         ],
#     #     )
#
#     def test_body_part_02(self):
#         self.assertEqual(
#             test_traits("head, thorax, abdomen"),
#             [
#                 {
#                     "body_part": "head, thorax, abdomen",
#                     "trait": "body_part",
#                     "start": 0,
#                     "end": 21,
#                 }
#             ],
#         )
#
#     def test_body_part_03(self):
#         self.assertEqual(
#             test_traits("missing eyes"),
#             [
#                 {
#                     "body_part": "missing eye",
#                     "missing": True,
#                     "trait": "body_part",
#                     "start": 0,
#                     "end": 12,
#                 }
#             ],
#         )
