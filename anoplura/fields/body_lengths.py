"""Build a pivot table of body length traits across species and sexes."""

from typing import TYPE_CHECKING

from anoplura.pylib import format_util

if TYPE_CHECKING:
    import pandas as pd

FIELD_LABELS = {
    "length": "body length",
    "mean_length": "mean body length",
    "length_low": "low body length",
    "length_high": "high body length",
    "n": "body length sample size (n)",
}


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of body length measurements.

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
        labels describing each body length sub-trait.

    """
    return format_util.build_trait_table(records, species_sexes, FIELD_LABELS)
