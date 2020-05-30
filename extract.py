#!/usr/bin/env python3

"""Extract lice traits from scientific literature (PDFs to text)."""

# from lice.pylib.util import DATA_DIR
from lice.matchers.matcher import Matcher


def main():
    """Extract data from the files."""
    matcher = Matcher()

    text = """
        Hoplopleura sciuricola Ferris, 1921 Specimens examined:
        ARIZONA: Coconino County, Kaibab Plateau, ~1/2 km down FR487,
        2,338 m elev., 8 October 1993; 5♂♂, 1♀, 5N ex Sciurus aberti.
        UTAH: Cache County, Bear River Range, vic. Willow Spring, 2,341
        m elev., 15 August 1992; 4♂♂, 7♀♀ ex Tamiasciurus hudsonicus.
        Summit County, Uinta Mountains, W portal of Duchesne Tunnel on UT150,
        2,475 m elev., 14 October 1990; 1♂, 1♀ ex T. hudsonicus.
        WYOMING: Teton County, Gros Ventre Range, vic. Granite Creek
        campground, 2,097 m elev., 22 September 1994; 4♂♂, 5♀♀, 2N
        ex T. hudsonicus.
        """

    matcher.parse(text)

    # for path in DATA_DIR.glob('*.txt'):
    #     pass


if __name__ == '__main__':
    main()
