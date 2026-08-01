"""Build a pivot table of plate notations across species and sexes."""

from dataclasses import dataclass

import pandas as pd

from anoplura.pylib import format_util


@dataclass
class Plate:
    body_region: str = ""
    label: str = ""
    species: str = ""
    sex: str = ""
    count: str = ""
    description: str = ""

    @property
    def count_row_loc(self) -> tuple:
        return self.body_region, f"{self.label} count"

    @property
    def description_row_loc(self) -> tuple:
        return self.body_region, f"{self.label} description"

    @property
    def col_loc(self) -> tuple:
        return self.species, self.sex


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of plate notations.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of plate record dicts.
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each plate notation.

    """
    # Map record fields to row indexes
    plates: list[Plate] = []

    for rec in records:
        region = format_util.expand_body_region(rec)
        type_ = rec["plate_type"]
        number = rec["number"]

        numbers = format_util.expand_numbers(number)

        prefix = type_ or f"{region} plate" if region else "plate"
        prefix = prefix.replace("plates", "plate").replace("thorax", "thoracic")
        labels = [f"{prefix} {n}" for n in numbers] if numbers else [prefix]

        plates += [
            Plate(
                body_region=region,
                label=lb,
                species=rec["species"],
                sex=rec["sex"],
                count=rec["count"],
                description=rec["description"],
            )
            for lb in labels
        ]

    # Build row index
    row_index = set()
    for plate in plates:
        row_index.add(plate.count_row_loc)
        row_index.add(plate.description_row_loc)
    row_index = sorted(row_index)
    row_index = pd.MultiIndex.from_tuples(row_index, names=["region", "label"])

    # Build the data frame
    df = pd.DataFrame(index=row_index, columns=species_sexes)
    for plate in plates:
        if plate.count:
            df.loc[plate.count_row_loc, plate.col_loc] = plate.count

        if plate.description:
            df.loc[plate.description_row_loc, plate.col_loc] = plate.description

    return df
