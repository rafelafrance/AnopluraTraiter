"""Build a pivot table of abdomen width traits across species and sexes."""

from typing import TYPE_CHECKING

from anoplura.pylib import format_util

if TYPE_CHECKING:
    import pandas as pd

FIELD_LABELS = {
    "width": "abdomen width",
    "mean_width": "mean abdomen width",
    "width_low": "low abdomen width",
    "width_high": "high abdomen width",
    "n": "abdomen width sample size (n)",
}


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of abdomen width measurements.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of abdomen_width trait record dicts.
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each abdomen width sub-trait.

    """
    return format_util.build_trait_table(records, species_sexes, FIELD_LABELS)
