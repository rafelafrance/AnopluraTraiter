"""Build a pivot table of geographic location notations across species and sexes."""

from typing import TYPE_CHECKING

from anoplura.pylib import format_util

if TYPE_CHECKING:
    import pandas as pd

FIELD_LABELS = {
    "geographic_location": "geographic location",
}


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of geographic location notations.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of geographic location trait record dicts.
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each geographic location notation.

    """
    return format_util.build_trait_table(records, species_sexes, FIELD_LABELS)
