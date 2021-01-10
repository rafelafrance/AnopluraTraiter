"""Test antenna trait matcher."""

import unittest

from tests.setup import test_traits


class TestAntenna(unittest.TestCase):
    """Test antenna trait matcher."""

    def test_antenna_01(self):
        self.assertEqual(
            test_traits('Head suboval; antennae unmodified in males;.'),
            [{'body_part': 'head', 'trait': 'body_part', 'start': 0, 'end': 4},
             {'description': 'suboval', 'body_part': 'head',
              'trait': 'description', 'start': 5, 'end': 12},
             {'body_part': 'antenna', 'trait': 'body_part',
              'start': 14, 'end': 22},
             {'description': 'unmodified in males', 'body_part': 'antenna',
              'trait': 'description', 'start': 23, 'end': 42}]
        )

    def test_antenna_02(self):
        self.assertEqual(
            test_traits("""
                Antennae five-segmented with basal segment wider than long and
                much larger than second segment; fourth segment slightly
                extended posterolaterally.
                """),
            [{'body_part': 'antenna', 'trait': 'body_part', 'start': 0, 'end': 8},
             {'description': 'five-segmented', 'body_part': 'antenna',
              'trait': 'description', 'start': 9, 'end': 23},
             {'body_part': 'basal segment',
              'trait': 'body_part', 'start': 29, 'end': 42},
             {'body_part': 'second segment',
              'trait': 'body_part', 'start': 80, 'end': 94},
             {'body_part': 'fourth segment',
              'trait': 'body_part', 'start': 96, 'end': 110},
             {'description': 'slightly extended posterolaterally',
              'body_part': 'fourth segment',
              'trait': 'description', 'start': 111, 'end': 145}]
        )

    def test_antenna_03(self):
        self.assertEqual(
            test_traits("""
                Head lacking eyes, with 5-segmented antennae which are often
                sexually dimorphic.
                """),
            [{'body_part': 'head', 'trait': 'body_part', 'start': 0, 'end': 4},
             {'body_part': 'lacking eyes', 'missing': True,
              'trait': 'body_part', 'start': 5, 'end': 17},
             {'description': '5-segmented', 'body_part': 'antenna',
              'trait': 'description', 'start': 24, 'end': 35},
             {'body_part': 'antenna', 'trait': 'body_part', 'start': 36, 'end': 44},
             {'description': 'which are often sexually dimorphic',
              'body_part': 'antenna', 'trait': 'description', 'start': 45, 'end': 79}]
        )

    def test_antenna_04(self):
        self.assertEqual(
            test_traits("""
                third antennal segment modified with anterodorsal projection.
                """),
            [{'body_part': 'third antennal segment',
              'trait': 'body_part', 'start': 0, 'end': 22},
             {'description': 'modified with anterodorsal projection',
              'body_part': 'third antennal segment',
              'trait': 'description', 'start': 23, 'end': 60}]
        )

    def test_antenna_05(self):
        self.assertEqual(
            test_traits('Antennal segments 3-5 not fused;'),
            [{'body_part': 'antennal segments 3-5',
              'trait': 'body_part', 'start': 0, 'end': 21},
             {'description': 'not fused',
              'body_part': 'antennal segments 3-5',
              'trait': 'description', 'start': 22, 'end': 31}]
        )
