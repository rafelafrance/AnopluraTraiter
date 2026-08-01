"""Build a pivot table of seta count notations across species and sexes."""

import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from anoplura.pylib import format_util

SETA_CSV = Path("anoplura/terms") / "seta_patterns.csv"
#
# Get seta patterns
SETA_DF = pd.read_csv(SETA_CSV)
SETA_PATTERNS = {s["pattern"]: s["replace"] for s in SETA_DF.to_dict("records")}


@dataclass
class SetaCount:
    body_region: str = ""
    label: str = ""
    species: str = ""
    sex: str = ""
    seta_name: str = ""
    segment: str = ""
    count: str = ""
    side: str = ""
    rows: str = ""
    description: str = ""

    @property
    def count_row_loc(self) -> tuple:
        return self.body_region, self.label

    @property
    def rows_row_loc(self) -> tuple:
        return self.body_region, f"{self.label} rows"

    @property
    def side_row_loc(self) -> tuple:
        return self.body_region, f"{self.label} side"

    @property
    def description_row_loc(self) -> tuple:
        return self.body_region, f"{self.label.removesuffix(' count')} description"

    @property
    def col_loc(self) -> tuple:
        return self.species, self.sex

    def finish_label(self) -> None:
        name = self.seta_name
        if name.find("count") == -1:
            name += " seta count" if name.find("seta") == -1 else " count"
        self.label = name


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
    seta_counts = []

    # Expand records
    for rec in records:
        region = format_util.expand_body_region(rec)

        seta_name = re.sub(r"(hairs?|spines?)", "setae", rec["seta_name"])
        seta_name = re.sub(r"\s*\(\w+\)", "", seta_name)  # Remove like (VPHS)
        seta_name = seta_name.lower()
        seta_name = SETA_PATTERNS.get(seta_name, seta_name)

        seg = rec["segment"]
        segment_list = [f"segment {n}" for n in format_util.expand_numbers(seg)]

        if seta_name and region and segment_list:
            labels = [f"{seta_name} counts on {region} {s}" for s in segment_list]
        elif seta_name and segment_list:
            labels = [f"{seta_name} counts on {s}" for s in segment_list]
        elif seta_name:
            labels = [seta_name]
            segment_list = [""]
        else:
            label = " ".join([f for f in (region, seg) if f])
            labels = [f"{label} seta"]
            segment_list = [""]

        seta_counts += [
            SetaCount(
                body_region=region,
                label=lb,
                species=rec["species"],
                sex=rec["sex"],
                seta_name=seta_name,
                segment=seg,
                count=rec["count"],
                side=rec["side"],
                rows=rec["rows"],
                description=rec["description"],
            )
            for lb, seg in zip(labels, segment_list, strict=True)
        ]

    # Build row index
    row_index = set()
    for seta in seta_counts:
        seta.finish_label()
        row_index.add(seta.count_row_loc)
        row_index.add(seta.rows_row_loc)
        row_index.add(seta.side_row_loc)
        row_index.add(seta.description_row_loc)
    row_index = sorted(row_index)
    row_index = pd.MultiIndex.from_tuples(row_index, names=["region", "label"])

    # Build the data frame
    df = pd.DataFrame(index=row_index, columns=species_sexes)
    for seta in seta_counts:
        if seta.count:
            df.loc[seta.count_row_loc, seta.col_loc] = seta.count

        if seta.description:
            df.loc[seta.description_row_loc, seta.col_loc] = seta.description

        if seta.rows:
            df.loc[seta.rows_row_loc, seta.col_loc] = seta.rows

        if seta.side:
            df.loc[seta.side_row_loc, seta.col_loc] = seta.side

    return df
