"""Build a pivot table of trait exceptions across species and sexes."""

from typing import TYPE_CHECKING

from anoplura.pylib import format_util

if TYPE_CHECKING:
    import pandas as pd

FIELD_LABELS = {
    "phrase": "exception phrase",
    "general_trait": "baseline trait excepted",
    "exception": "exception difference",
    "body_region": "exception body region",
}


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of except notations.

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
        labels describing each exception field.

    """
    return format_util.build_trait_table(records, species_sexes, FIELD_LABELS)
