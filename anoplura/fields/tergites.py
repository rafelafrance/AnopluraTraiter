"""Build a pivot table of tergite notations across species and sexes."""

import re
from collections import defaultdict
from itertools import product

import pandas as pd

from anoplura.pylib import format_util


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of tergite notations.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of tergite record dicts.
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each tergite notation.

    """
    # Map record fields to row indexes
    row_map = defaultdict(set)
    for rec in records:
        region = rec["body_region"]
        seg = rec["segment"]
        number = rec["number"]
        missing = rec["missing"]
        key = region, seg, number

        tergite_list = [f"tergite {n}" for n in format_util.expand_numbers(number)]
        segment_list = [f"segment {n}" for n in format_util.expand_numbers(seg)]

        tergites = []

        if missing:
            tergite = " ".join(
                [f for f in (region, seg, "tergites missing") if f]
            ).lower()
            tergites = [tergite]
        elif tergite_list and segment_list:
            stern = [f"{p[0]} {p[1]}" for p in product(segment_list, tergite_list)]
            tergites = [" ".join([f for f in (region, s) if f]) for s in stern]
        elif tergite_list:
            tergites = tergite_list
        elif segment_list:
            tergites = [f"tergites on {s}" for s in segment_list]
        else:
            tergite = " ".join(
                [f for f in (region, seg, number, "tergites") if f]
            ).lower()
            tergites = [tergite]

        if tergites:
            row_map[key] |= set(tergites)

    # # Build row index
    row_index = set()
    for indexes in row_map.values():
        for idx in indexes:
            if not re.search(r"(tergite\s+\d+|missing)", idx):
                row_index.add(f"{idx} count")
            if re.search(r"missing", idx):
                row_index.add(idx)
            else:
                row_index.add(f"{idx} description")
    row_index = sorted(row_index)
    row_index = [" ".join(i.split()) for i in row_index]

    # Build the data frame
    df = pd.DataFrame(index=row_index, columns=species_sexes)
    for rec in records:
        key = rec["body_region"], rec["segment"], rec["number"]
        indexes = row_map[key]
        for idx in indexes:
            count = f"{idx} count"
            descr = f"{idx} description"
            if (df.index == count).any():
                df.loc[count, (rec["species"], rec["sex"])] = rec["count"]
            if (df.index == descr).any():
                df.loc[descr, (rec["species"], rec["sex"])] = rec["description"]
            if (df.index == idx).any():
                df.loc[idx, (rec["species"], "male")] = "True"
                df.loc[idx, (rec["species"], "female")] = "True"

    df = df.fillna("")
    return df
