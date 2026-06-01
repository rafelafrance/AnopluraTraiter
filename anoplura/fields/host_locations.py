"""Build a pivot table of host location notations across species and sexes."""

from typing import TYPE_CHECKING

from anoplura.pylib import format_util

if TYPE_CHECKING:
    import pandas as pd

FIELD_LABELS = {
    "host_species": "host species",
    "host_location": "host location",
    "context": "host context",
}


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of host location notations.

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
        labels describing each host location notation.

    """
    return format_util.build_trait_table(records, species_sexes, FIELD_LABELS)
