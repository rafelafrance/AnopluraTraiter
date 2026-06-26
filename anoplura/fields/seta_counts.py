"""Build a pivot table of seta count notations across species and sexes."""

import re
from collections import defaultdict
from pathlib import Path

import pandas as pd

from anoplura.pylib import format_util

SETA_CSV = Path("anoplura/terms") / "seta_patterns.csv"


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
    # Get seta patterns
    seta_df = pd.read_csv(SETA_CSV)
    seta_patterns = {s["pattern"]: s["replace"] for s in seta_df.to_dict("records")}

    # Map record fields to row indexes
    regions = {"abdomen": "abdominal", "thorax": "thoracic"}
    row_map = defaultdict(set)
    for rec in records:
        original = rec["seta_name"]
        rec_name = re.sub(r"(hairs?|spines?)", "setae", original)
        rec_name = re.sub(r"\s*\(\w+\)", "", rec_name)  # Remove like (VPHS)
        name_list = re.split(r"[,]\s*(?:and\s*)?|\s+and\s*", rec_name.lower())

        region = rec["body_region"]
        region = regions.get(region, region)

        seg = rec["segment"]
        segment_list = [f"segment {n}" for n in format_util.expand_numbers(seg)]

        key = original, region, seg

        seta_counts = []

        for name in name_list:
            name = seta_patterns.get(name.lower(), name)

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

    # Build row index
    row_index = set()
    for indexes in row_map.values():
        for idx in indexes:
            if not re.search(r"(seta_count\s+\d+|missing)", idx):
                row_index.add(f"{idx} count")
            if re.search(r"missing", idx):
                row_index.add(idx)
            else:
                row_index.add(f"{idx} description")
            row_index.add(f"{idx} rows")
            row_index.add(f"{idx} side")
    row_index = sorted(row_index)
    row_index = [" ".join(i.split()) for i in row_index]

    # Build the data frame
    df = pd.DataFrame(index=row_index, columns=species_sexes)
    for rec in records:
        key = rec["seta_name"], rec["body_region"], rec["segment"]
        indexes = row_map[key]
        for idx in indexes:
            count = f"{idx} count"
            descr = f"{idx} description"
            rows = f"{idx} rows"
            side = f"{idx} sides"
            if (df.index == count).any():
                df.loc[count, (rec["species"], rec["sex"])] = rec["count"] or None
            if (df.index == descr).any():
                df.loc[descr, (rec["species"], rec["sex"])] = rec["description"] or None
            if (df.index == rows).any():
                df.loc[rows, (rec["species"], rec["sex"])] = rec["rows"] or None
            if (df.index == side).any():
                df.loc[side, (rec["species"], rec["sex"])] = rec["side"] or None
            if (df.index == idx).any():
                df.loc[idx, (rec["species"], "male")] = "True"
                df.loc[idx, (rec["species"], "female")] = "True"

    return df
