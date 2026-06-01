"""Build a pivot table of plate notations across species and sexes."""

from collections import defaultdict

import pandas as pd

from anoplura.pylib import format_util


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of plate notations.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of body_length trait record dicts.
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each platehost location  notation.

    """
    # Map record fields to row indexes
    row_map = defaultdict(set)
    for rec in records:
        region = rec["body_region"]
        type_ = rec["plate_type"]
        number = rec["number"]
        key = region, type_, number

        nums = format_util.expand_numbers(number)

        prefix = type_ or f"{region} plate" or "plate"
        prefix = prefix.replace("plates", "plate").replace("thorax", "thoracic")
        if nums:
            row_map[key] |= {f"{prefix} {n}" for n in nums}
        else:
            row_map[key].add(prefix)

    # Build row index
    row_index = set()
    for indexes in row_map.values():
        for idx in indexes:
            row_index.add(f"{idx} count")
            row_index.add(f"{idx} description")
    row_index = sorted(row_index)

    # Build the data frame
    df = pd.DataFrame(index=row_index, columns=species_sexes)
    for rec in records:
        key = rec["body_region"], rec["plate_type"], rec["number"]
        indexes = row_map[key]
        for idx in indexes:
            count = f"{idx} count"
            descr = f"{idx} description"
            df.loc[count, (rec["species"], rec["sex"])] = rec["count"]
            df.loc[descr, (rec["species"], rec["sex"])] = rec["description"]

    df = df.fillna("")
    return df
