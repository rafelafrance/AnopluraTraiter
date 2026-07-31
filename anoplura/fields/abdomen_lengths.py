"""Build a pivot table of abdomen length traits across species and sexes."""

from typing import TYPE_CHECKING

from anoplura.pylib import format_util

if TYPE_CHECKING:
    import pandas as pd

FIELD_LABELS = {
    "length": "abdomen length",
    "mean_length": "mean abdomen length",
    "length_low": "low abdomen length",
    "length_high": "high abdomen length",
    "uncertainty": "abdomen length uncertainty",
    "n": "abdomen length sample size (n)",
}


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of abdomen length measurements.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of abdomen_length trait record dicts.
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each abdomen length sub-trait.

    """
    return format_util.build_trait_table(records, species_sexes, FIELD_LABELS)
