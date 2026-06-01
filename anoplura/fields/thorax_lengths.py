"""Build a pivot table of thorax length traits across species and sexes."""

from typing import TYPE_CHECKING

from anoplura.pylib import format_util

if TYPE_CHECKING:
    import pandas as pd

FIELD_LABELS = {
    "length": "thorax length",
    "mean_length": "mean thorax length",
    "length_low": "low thorax length",
    "length_high": "high thorax length",
    "n": "thorax length sample size (n)",
}


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of thorax length measurements.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of thorax_length trait record dicts.
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each thorax length sub-trait.

    """
    return format_util.build_trait_table(records, species_sexes, FIELD_LABELS)
