"""Build a pivot table of tergite notations across species and sexes."""

from dataclasses import dataclass
from itertools import product

import pandas as pd

from anoplura.pylib import format_util


@dataclass
class Tergite:
    body_region: str = ""
    label: str = ""
    species: str = ""
    sex: str = ""
    count: str = ""
    missing: str = ""
    description: str = ""

    @property
    def count_row_loc(self) -> tuple:
        return self.body_region, f"{self.label} count"

    @property
    def missing_row_loc(self) -> tuple:
        return self.body_region, self.label

    @property
    def description_row_loc(self) -> tuple:
        return self.body_region, f"{self.label} description"

    @property
    def col_loc(self) -> tuple:
        return self.species, self.sex


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
    tergites: list[Tergite] = []

    for rec in records:
        region = format_util.expand_body_region(rec)
        seg = rec["segment"]
        number = rec["number"]
        missing = rec["missing"]

        # Expand tergite numbers and segments into lists
        tergite_list = [f"tergite {n}" for n in format_util.expand_numbers(number)]
        segment_list = [f"segment {n}" for n in format_util.expand_numbers(seg)]

        if missing:
            label = " ".join(
                [f for f in (region, seg, "tergites missing") if f]
            ).lower()
            labels = [label]
        elif tergite_list and segment_list:
            labels = [f"{p[0]} {p[1]}" for p in product(segment_list, tergite_list)]
            labels = [" ".join([f for f in (region, s) if f]) for s in labels]
        elif tergite_list:
            labels = tergite_list
        elif segment_list:
            labels = [f"tergites on {s}" for s in segment_list]
        else:
            label = " ".join(
                [f for f in (region, seg, number, "tergites") if f]
            ).lower()
            labels = [label]

        tergites += [
            Tergite(
                body_region=region,
                label=lb,
                species=rec["species"],
                sex=rec["sex"],
                count=rec["count"],
                missing=rec["missing"],
                description=rec["description"],
            )
            for lb in labels
        ]

    # Build row index
    row_index = set()
    for tergite in tergites:
        row_index.add(tergite.count_row_loc)
        row_index.add(tergite.missing_row_loc)
        row_index.add(tergite.description_row_loc)
    row_index = sorted(row_index)
    row_index = pd.MultiIndex.from_tuples(row_index, names=["region", "label"])

    # Build the data frame
    df = pd.DataFrame(index=row_index, columns=species_sexes)
    for tergite in tergites:
        if tergite.count:
            df.loc[tergite.count_row_loc, tergite.col_loc] = tergite.count

        if tergite.missing:
            df.loc[tergite.missing_row_loc, tergite.col_loc] = "True"

        if tergite.description:
            df.loc[tergite.description_row_loc, tergite.col_loc] = tergite.description

    return df
