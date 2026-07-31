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
REGIONS = {"abdomen": "abdominal", "thorax": "thoracic"}


@dataclass
class SetaCount:
    body_region: str = ""
    species: str = ""
    sex: str = ""
    seta_name: str = ""
    segment: str = ""
    count: str = ""
    side: str = ""
    rows: str = ""
    description: str = ""


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
        seta_name = re.sub(r"(hairs?|spines?)", "setae", rec["seta_name"])
        seta_name = re.sub(r"\s*\(\w+\)", "", seta_name)  # Remove like (VPHS)
        seta_name = seta_name.lower()
        seta_name = SETA_PATTERNS.get(seta_name, seta_name)

        region = rec.get("body_region", "").lower()
        region = REGIONS.get(region, region)

        seg = rec["segment"]
        segment_list = [f"segment {n}" for n in format_util.expand_numbers(seg)]

        names = []
        if seta_name and region and segment_list:
            names = [f"{seta_name} counts on {region} {s}" for s in segment_list]
        elif seta_name and segment_list:
            names = [f"{seta_name} counts on {s}" for s in segment_list]
        elif seta_name:
            names = [seta_name]
            segment_list = [""]
        else:
            name = " ".join([f for f in (region, seg) if f])
            names = [name]
            segment_list = [""]

        seta_counts += [
            SetaCount(
                body_region=region,
                species=rec["species"],
                sex=rec["sex"],
                seta_name=name,
                segment=seg,
                count=rec["count"],
                side=rec["side"],
                rows=rec["rows"],
                description=rec["description"],
            )
            for name, seg in zip(names, segment_list, strict=True)
        ]

    # Build row index
    row_index = set()
    for count in seta_counts:
        name = get_seta_name(count)
        row_index.add((count.body_region, name))
        row_index.add((count.body_region, f"{name} rows"))
        row_index.add((count.body_region, f"{name} side"))
        row_index.add((count.body_region, f"{name} description"))
    row_index = sorted(row_index)
    row_index = pd.MultiIndex.from_tuples(row_index, names=["region", "label"])

    # Build the data frame
    df = pd.DataFrame(index=row_index, columns=species_sexes)
    for count in seta_counts:
        name = get_seta_name(count)
        desc = f"{name} description"
        rows = f"{name} rows"
        side = f"{name} side"

        df.loc[(count.body_region, name)] = count.count
        if count.description:
            df.loc[(count.body_region, desc)] = count.description
        if count.rows:
            df.loc[(count.body_region, rows)] = count.rows
        if count.side:
            df.loc[(count.body_region, side)] = count.side

    return df


def get_seta_name(count: SetaCount) -> str:
    name = count.seta_name
    if name.find("count") == -1:
        name += " seta count" if not name.endswith("seta") else " count"
    return name
