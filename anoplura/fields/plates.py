"""Build a pivot table of plate notations across species and sexes."""

from typing import TYPE_CHECKING

from anoplura.pylib import format_util

if TYPE_CHECKING:
    import pandas as pd

FIELD_LABELS = {
    "plate_type": "plate type",
    "description": "plate description",
    "count": "plate count",
}


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
    # Expand plate numbers or use other descriptions
    for rec in records:
        print(rec)

    return format_util.build_trait_table(records, species_sexes, FIELD_LABELS)
