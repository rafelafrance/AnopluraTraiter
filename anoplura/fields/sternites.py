"""Build a pivot table of sternite notations across species and sexes."""

from dataclasses import dataclass
from itertools import product

import pandas as pd

from anoplura.pylib import format_util


@dataclass
class Sternite:
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
    sternites: list[Sternite] = []

    for rec in records:
        region = format_util.expand_body_region(rec)
        seg = rec["segment"]
        number = rec["number"]
        missing = rec["missing"]

        # Expand sternite numbers and segments into lists
        sternite_list = [f"sternite {n}" for n in format_util.expand_numbers(number)]
        segment_list = [f"segment {n}" for n in format_util.expand_numbers(seg)]

        # Build sternite records
        if missing:
            label = " ".join(
                [f for f in (region, seg, "sternites missing") if f]
            ).lower()
            labels = [label]
        elif sternite_list and segment_list:
            labels = [f"{p[0]} {p[1]}" for p in product(segment_list, sternite_list)]
            labels = [" ".join([f for f in (region, s) if f]) for s in labels]
        elif sternite_list:
            labels = sternite_list
        elif segment_list:
            labels = [f"sternites on {s}" for s in segment_list]
        else:
            label = " ".join(
                [f for f in (region, seg, number, "sternites") if f]
            ).lower()
            labels = [label]

        sternites += [
            Sternite(
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
    for sternite in sternites:
        row_index.add(sternite.count_row_loc)
        row_index.add(sternite.missing_row_loc)
        row_index.add(sternite.description_row_loc)
    row_index = sorted(row_index)
    row_index = pd.MultiIndex.from_tuples(row_index, names=["region", "label"])

    # Build the data frame
    df = pd.DataFrame(index=row_index, columns=species_sexes)
    for sternite in sternites:
        if sternite.count:
            df.loc[sternite.count_row_loc, sternite.col_loc] = sternite.count

        if sternite.missing:
            df.loc[sternite.missing_row_loc, sternite.col_loc] = "True"

        if sternite.description:
            df.loc[sternite.description_row_loc, sternite.col_loc] = (
                sternite.description
            )

    return df
