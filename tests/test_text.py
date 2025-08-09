import unittest

from tests.setup import parse


class TestText(unittest.TestCase):
    def test_text_00(self):
        parse(
            """
            subtriangular coxae
            proximally and acuminate claws terminally
            """
        )
