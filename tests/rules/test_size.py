# import unittest
#
# from anoplura.rules.size import Dimension, Size
# from tests.setup import parse
#
#
# class TestSize(unittest.TestCase):
#     def test_size_01(self) -> None:
#         """It handles values larger than 1000."""
#         self.assertEqual(
#             parse("""Elevation: 0–3600 m"""),
#             [
#                 Size(
#                     dims=[
#                         Dimension(
#                             dim="length",
#                             low=0,
#                             high=3600,
#                             units="m",
#                             start=11,
#                             end=19,
#                         )
#                     ],
#                     start=11,
#                     end=19,
#                 ),
#             ],
#         )
#
#     def test_size_02(self) -> None:
#         """It handles two dimensions."""
#         self.assertEqual(
#             parse("""30–60 × 10-20 cm,"""),
#             [
#                 Size(
#                     dims=[
#                         Dimension(
#                             dim="length",
#                             low=30,
#                             high=60,
#                             units="cm",
#                             start=0,
#                             end=5,
#                         ),
#                         Dimension(
#                             dim="width",
#                             low=10,
#                             high=20,
#                             units="cm",
#                             start=8,
#                             end=16,
#                         ),
#                     ],
#                     start=0,
#                     end=16,
#                 ),
#             ],
#         )
#
#     def test_size_03(self) -> None:
#         """It handles an extra plus sign."""
#         self.assertEqual(
#             parse("""10–30+ cm,"""),
#             [
#                 Size(
#                     dims=[
#                         Dimension(
#                             dim="length",
#                             low=10,
#                             high=30,
#                             units="cm",
#                             start=0,
#                             end=9,
#                         )
#                     ],
#                     start=0,
#                     end=9,
#                 ),
#             ],
#         )
#
#     def test_size_04(self) -> None:
#         self.assertEqual(
#             parse("""length, 1.02 mm."""),
#             [
#                 Size(
#                     dims=[
#                         Dimension(
#                             dim="length",
#                             low=1.02,
#                             units="mm",
#                             start=0,
#                             end=16,
#                         )
#                     ],
#                     start=0,
#                     end=16,
#                 ),
#             ],
#         )
