"""Build a pivot table of head width traits across species and sexes."""

from typing import TYPE_CHECKING

from anoplura.pylib import format_util

if TYPE_CHECKING:
    import pandas as pd

FIELD_LABELS = {
    "width": "head width",
    "mean_width": "mean head width",
    "width_low": "low head width",
    "width_high": "high head width",
    "n": "head width sample size (n)",
}


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of head width measurements.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of head_width trait record dicts.
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each head width sub-trait.

    """
    return format_util.build_trait_table(records, species_sexes, FIELD_LABELS)
