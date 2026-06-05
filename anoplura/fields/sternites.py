"""Build a pivot table of sternite notations across species and sexes."""

import re
from collections import defaultdict
from itertools import product

import pandas as pd

from anoplura.pylib import format_util


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of sternite notations.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of sternite record dicts.
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each sternite notation.

    """
    # Map record fields to row indexes
    row_map = defaultdict(set)
    for rec in records:
        region = rec["body_region"]
        seg = rec["segment"]
        number = rec["number"]
        missing = rec["missing"]
        key = region, seg, number

        sternite_list = [f"sternite {n}" for n in format_util.expand_numbers(number)]
        segment_list = [f"segment {n}" for n in format_util.expand_numbers(seg)]

        sternites = []

        if missing:
            sternite = " ".join(
                [f for f in (region, seg, "sternites missing") if f]
            ).lower()
            sternites = [sternite]
        elif sternite_list and segment_list:
            stern = [f"{p[0]} {p[1]}" for p in product(segment_list, sternite_list)]
            sternites = [" ".join([f for f in (region, s) if f]) for s in stern]
        elif sternite_list:
            sternites = sternite_list
        elif segment_list:
            sternites = [f"sternites on {s}" for s in segment_list]
        else:
            sternite = " ".join(
                [f for f in (region, seg, number, "sternites") if f]
            ).lower()
            sternites = [sternite]

        if sternites:
            row_map[key] |= set(sternites)

    # # Build row index
    row_index = set()
    for indexes in row_map.values():
        for idx in indexes:
            if not re.search(r"(sternite\s+\d+|missing)", idx):
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
