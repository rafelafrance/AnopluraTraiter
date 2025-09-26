# import unittest
#
# from anoplura.rules.count import Count
# from anoplura.rules.description import Description
# from anoplura.rules.seta import Seta
# from anoplura.rules.sex import Sex
# from anoplura.rules.sternite import Sternite
# from anoplura.rules.subpart import Subpart
# from anoplura.rules.tergite import Tergite
# from tests.setup import parse
#
#
# class TestCount(unittest.TestCase):
#     def test_count_01(self) -> None:
#         self.assertEqual(
#             parse("One small lobe"),
#             [
#                 Count(
#                     start=0,
#                     end=3,
#                     links=[Subpart(start=10, end=14, subpart="lobe")],
#                     count_low=1,
#                 ),
#                 Description(
#                     start=4,
#                     end=9,
#                     links=[Subpart(start=10, end=14, subpart="lobe")],
#                     description="small",
#                 ),
#                 Subpart(
#                     start=10,
#                     end=14,
#                     links=[
#                         Description(start=4, end=9, description="small"),
#                         Count(start=0, end=3, count_low=1),
#                     ],
#                     subpart="lobe",
#                 ),
#             ],
#         )
#
#     def test_count_02(self) -> None:
#         self.assertEqual(
#             parse("3 long, narrow sternites"),
#             [
#                 Count(
#                     start=0,
#                     end=1,
#                     links=[Sternite(start=15, end=24, part="sternite")],
#                     count_low=3,
#                 ),
#                 Description(
#                     start=2,
#                     end=14,
#                     links=[Sternite(start=15, end=24, part="sternite")],
#                     description="long, narrow",
#                 ),
#                 Sternite(
#                     start=15,
#                     end=24,
#                     links=[
#                         Description(start=2, end=14, description="long, narrow"),
#                         Count(start=0, end=1, count_low=3),
#                     ],
#                     part="sternite",
#                 ),
#             ],
#         )
#
#     def test_count_03(self) -> None:
#         self.assertEqual(
#             parse("4 DCAS,"),
#             [
#                 Count(
#                     start=0,
#                     end=1,
#                     links=[
#                         Seta(
#                             start=2,
#                             end=6,
#                             seta="dorsal central abdominal setae",
#                             seta_part="abdomen",
#                         )
#                     ],
#                     count_low=4,
#                 ),
#                 Seta(
#                     start=2,
#                     end=6,
#                     links=[Count(start=0, end=1, count_low=4)],
#                     seta="dorsal central abdominal setae",
#                     seta_part="abdomen",
#                 ),
#             ],
#         )
#
#     def test_count_04(self) -> None:
#         self.assertEqual(
#             parse("5 pairs of DCAS,"),
#             [
#                 Count(
#                     start=0,
#                     end=10,
#                     links=[
#                         Seta(
#                             start=11,
#                             end=15,
#                             seta="dorsal central abdominal setae",
#                             seta_part="abdomen",
#                         )
#                     ],
#                     count_low=5,
#                     count_group="pairs of",
#                 ),
#                 Seta(
#                     start=11,
#                     end=15,
#                    inks=[Count(start=0, end=10, count_low=5, count_group="pairs of")],
#                     seta="dorsal central abdominal setae",
#                     seta_part="abdomen",
#                 ),
#             ],
#         )
#
#     def test_count_05(self) -> None:
#         self.assertEqual(
#             parse("6-7 DCAS,"),
#             [
#                 Count(
#                     start=0,
#                     end=3,
#                     links=[
#                         Seta(
#                             start=4,
#                             end=8,
#                             seta="dorsal central abdominal setae",
#                             seta_part="abdomen",
#                         )
#                     ],
#                     count_low=6,
#                     count_high=7,
#                 ),
#                 Seta(
#                     start=4,
#                     end=8,
#                     links=[Count(start=0, end=3, count_low=6, count_high=7)],
#                     seta="dorsal central abdominal setae",
#                     seta_part="abdomen",
#                 ),
#             ],
#         )
#
#     def test_count_06(self) -> None:
#         self.assertEqual(
#             parse(
#                 """
#                 3 or 4 apical head setae, 1 dorsal preantennal head seta
#                 """
#             ),
#             [
#                 Count(
#                     start=0,
#                     end=6,
#                     links=[
#                         Seta(
#                            start=7, end=24, seta="apical head setae", seta_part="head"
#                         )
#                     ],
#                     count_low=3,
#                     count_high=4,
#                 ),
#                 Seta(
#                     start=7,
#                     end=24,
#                     links=[Count(start=0, end=6, count_low=3, count_high=4)],
#                     seta="apical head setae",
#                     seta_part="head",
#                 ),
#                 Count(
#                     start=26,
#                     end=27,
#                     links=[
#                         Seta(
#                             start=28,
#                             end=56,
#                             seta="dorsal preantennal head setae",
#                             seta_part="head",
#                         )
#                     ],
#                     count_low=1,
#                 ),
#                 Seta(
#                     start=28,
#                     end=56,
#                     links=[Count(start=26, end=27, count_low=1)],
#                     seta="dorsal preantennal head setae",
#                     seta_part="head",
#                 ),
#             ],
#         )
#
#     def test_count_07(self) -> None:
#         self.assertEqual(
#             parse("2 lateral StAS on each side"),
#             [
#                 Count(
#                     start=0,
#                     end=1,
#                     links=[
#                         Seta(
#                             start=10,
#                             end=14,
#                             seta="sternal abdominal setae",
#                             seta_part="abdomen",
#                         )
#                     ],
#                     count_low=2,
#                 ),
#                 Description(
#                     start=2,
#                     end=9,
#                     links=[
#                         Seta(
#                             start=10,
#                             end=14,
#                             seta="sternal abdominal setae",
#                             seta_part="abdomen",
#                         )
#                     ],
#                     description="lateral",
#                 ),
#                 Seta(
#                     start=10,
#                     end=14,
#                     links=[
#                         Description(start=2, end=9, description="lateral"),
#                         Description(start=15, end=27, description="on each side"),
#                         Count(start=0, end=1, count_low=2),
#                     ],
#                     seta="sternal abdominal setae",
#                     seta_part="abdomen",
#                 ),
#                 Description(
#                     start=15,
#                     end=27,
#                     links=[
#                         Seta(
#                             start=10,
#                             end=14,
#                             seta="sternal abdominal setae",
#                             seta_part="abdomen",
#                         )
#                     ],
#                     description="on each side",
#                 ),
#             ],
#         )
#
#     def test_count_08(self) -> None:
#         self.assertEqual(
#             parse("1 (posterior row) setae"),
#             [
#                 Count(
#                     start=0,
#                     end=1,
#                     links=[Seta(start=18, end=23, seta="setae")],
#                     count_low=1,
#                 ),
#                 Description(
#                     start=3,
#                     end=16,
#                     links=[Seta(start=18, end=23, seta="setae")],
#                     description="posterior row",
#                 ),
#                 Seta(
#                     start=18,
#                     end=23,
#                     links=[
#                         Description(start=3, end=16, description="posterior row"),
#                         Count(
#                             start=0,
#                             end=1,
#                             count_low=1,
#                         ),
#                     ],
#                     seta="setae",
#                 ),
#             ],
#         )
#
#     def test_count_09(self) -> None:
#         self.assertEqual(
#             parse("setae (2 on 1 side, 3 on the other); sternites 4-10"),
#             [
#                 Seta(
#                     start=0,
#                     end=5,
#                     links=[
#                         Count(start=7, end=18, count_low=2, count_group="on 1 side"),
#                         Count(
#                             start=20, end=34, count_low=3, count_group="on the other"
#                         ),
#                     ],
#                     seta="setae",
#                 ),
#                 Count(
#                     start=7,
#                     end=18,
#                     links=[Seta(start=0, end=5, seta="setae")],
#                     count_low=2,
#                     count_group="on 1 side",
#                 ),
#                 Count(
#                     start=20,
#                     end=34,
#                     links=[Seta(start=0, end=5, seta="setae")],
#                     count_low=3,
#                     count_group="on the other",
#                 ),
#                 Sternite(
#                     start=37,
#                     end=51,
#                     links=[],
#                     part="sternite",
#                     number=[4, 5, 6, 7, 8, 9, 10],
#                 ),
#             ],
#         )
#
#     def test_count_10(self) -> None:
#         self.assertEqual(
#             parse("(23♂, 28♀)"),
#             [
#                 Count(
#                     start=1,
#                     end=3,
#                     links=[Sex(start=3, end=4, sex="male")],
#                     count_low=23,
#                 ),
#                 Sex(
#                     start=3,
#                     end=4,
#                     links=[Count(start=1, end=3, count_low=23)],
#                     sex="male",
#                 ),
#                 Count(
#                     start=6,
#                     end=8,
#                     links=[Sex(start=8, end=9, sex="female")],
#                     count_low=28,
#                 ),
#                 Sex(
#                     start=8,
#                     end=9,
#                     links=[Count(start=6, end=8, count_low=28)],
#                     sex="female",
#                 ),
#             ],
#         )
