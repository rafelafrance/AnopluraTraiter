import unittest

from anoplura.pylib.dimension import Dimension
from anoplura.rules.seta import Seta
from anoplura.rules.seta_size import SetaSize
from tests.setup import parse


class TestSetaSize(unittest.TestCase):
    def test_seta_size_01(self) -> None:
        self.assertEqual(
            parse("""(DPTS) length, 0.123 mm;"""),
            [
                Seta(
                    start=1,
                    end=5,
                    seta="dorsal principal thoracic setae",
                    seta_part="thorax",
                ),
                SetaSize(
                    start=7,
                    end=23,
                    seta="dorsal principal thoracic setae",
                    seta_part="thorax",
                    dims=[
                        Dimension(dim="length", units="mm", low=0.123, start=7, end=23)
                    ],
                ),
            ],
        )
