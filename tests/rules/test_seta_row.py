# import unittest
#
# from anoplura.rules.seta_row import SetaRow
# from tests.setup import parse
#
#
# class TestSetaRow(unittest.TestCase):
#     def test_seta_row_01(self):
#         self.assertEqual(
#             parse("row 1 with 4 DCAS,"),
#             [
#                 SetaRow(
#                     rows=[1],
#                     seta="dorsal central abdominal setae",
#                     start=0,
#                     end=17,
#                 ),
#             ],
#         )
#
#     def test_seta_row_02(self):
#         self.assertEqual(
#             parse("rows 2 and 3 each with 5 DCAS,"),
#             [
#                 SetaRow(
#                     rows=[2, 3],
#                     seta="dorsal central abdominal setae",
#                     start=0,
#                     end=29,
#                 ),
#             ],
#         )
#
#     def test_seta_row_03(self):
#         self.assertEqual(
#             parse("rows 4-7 each with 6-7 DCAS,"),
#             [
#                 SetaRow(
#                     seta="dorsal central abdominal setae",
#                     rows=[4, 5, 6, 7],
#                     start=0,
#                     end=27,
#                 ),
#             ],
#         )
