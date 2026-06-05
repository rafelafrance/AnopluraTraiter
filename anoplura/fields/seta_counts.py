"""Build a pivot table of seta count notations across species and sexes."""

import re
from collections import defaultdict

import pandas as pd

from anoplura.pylib import format_util


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of seta count notations.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of seta count record dicts.
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each seta count notation.

    """
    # Map record fields to row indexes
    regions = {"abdomen": "abdominal", "thorax": "thoracic"}
    row_map = defaultdict(set)
    for rec in records:
        region = rec["body_region"]
        region = regions.get(region, region)
        seg = rec["segment"]
        name = rec["seta_name"]
        name = name if name not in ("seta", "setae") else ""
        key = name, region, seg

        segment_list = [f"segment {n}" for n in format_util.expand_numbers(seg)]

        seta_counts = []

        if name and region and segment_list:
            seta_counts = [f"{name} counts on {region} {s}" for s in segment_list]
        elif name and segment_list:
            seta_counts = [f"{name} counts on {s}" for s in segment_list]
        elif name:
            seta_counts = [name]
        else:
            seta_count = " ".join([f for f in (region, seg) if f])
            seta_counts = [seta_count]

        if seta_counts:
            row_map[key] |= set(seta_counts)

    for key, value in row_map.items():
        print(key)
        print(value)
        print()

    # # Build row index
    row_index = set()
    for indexes in row_map.values():
        for idx in indexes:
            if not re.search(r"(seta_count\s+\d+|missing)", idx):
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
        key = rec["name"], rec["body_region"], rec["segment"]
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
