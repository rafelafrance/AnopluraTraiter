# import unittest
#
# from anoplura.rules.gonopod import Gonopod
# from anoplura.rules.group import Group
# from tests.setup import parse
#
#
# class TestText(unittest.TestCase):
#     def test_text_01(self):
#         self.assertEqual(
#             parse("""
#                 setae immediately anterior to gonopods IX on each side coning of 4
#                  (anterior row),"""),
#             [
#                 Gonopod(start=0, end=11, which=[9]),
#                 Group(group="on each side", start=12, end=24),
#             ],
#         )
