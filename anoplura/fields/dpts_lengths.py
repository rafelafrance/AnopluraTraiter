"""Build a pivot table of DPTS length traits across species and sexes."""

from typing import TYPE_CHECKING

from anoplura.pylib import format_util

if TYPE_CHECKING:
    import pandas as pd

FIELD_LABELS = {
    "length": "DPTS length",
    "mean_length": "mean DPTS length",
    "length_low": "low DPTS length",
    "length_high": "high DPTS length",
    "n": "DPTS length sample size (n)",
    "description": "DPTS length description",
}


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of DPTS length measurements.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of dpts_length trait record dicts.
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each DPTS length sub-trait.

    """
    return format_util.build_trait_table(records, species_sexes, FIELD_LABELS)
