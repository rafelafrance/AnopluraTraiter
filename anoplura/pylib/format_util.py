"""Utilities for formatting extracted trait data into pivot tables."""

import pandas as pd

from anoplura.pylib import ints, roman


def build_trait_table(
    records: list[dict],
    species_sexes: pd.MultiIndex,
    field_labels: dict[str, str],
) -> pd.DataFrame:
    """
    Build a DataFrame of trait measurements pivoted by species and sex.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of trait record dicts (e.g. all rows where
        ``"record" == "abdomen_length"``).
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.
    field_labels : dict[str, str]
        Mapping from JSON field name to human-readable row label
        (e.g. ``{"length": "abdomen length", "n": "abdomen length sample size (n)"}``).

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each sub-trait.  Missing values are blank strings.

    """
    df = pd.DataFrame(index=list(field_labels.values()), columns=species_sexes)
    for rec in records:
        for field, row_label in field_labels.items():
            df.loc[row_label, (rec["species"], rec["sex"])] = rec[field]

    df = df.fillna("")
    return df


def get_column_index(records: list[dict]) -> pd.MultiIndex:
    """
    Build the column index for the entire output data frame.

    Parameters
    ----------
    records : list[dict]
        Unfiltered list of trait record dicts (i.e. all rows).

    Returns
    -------
    pd.MultiIndex
        The two level column headers for the new output data frame.

    """
    col_tuples = {(r["species"], r.get("sex", "")) for r in records}
    col_tuples = sorted(col_tuples)
    return pd.MultiIndex.from_tuples(col_tuples, names=["species", "sex"])


def expand_numbers(text: str) -> list[str]:
    """Expand number ranges '1-3' or 'I-III', lists '1, 2, & 3' or 'I, II, & III'."""
    if not text:
        return []

    has_ints = ints.has_ints(text)
    has_roman = roman.has_roman(text)

    if not has_ints and not has_roman:
        return []

    if not has_ints and has_roman:
        if nums := roman.get_range(text):
            return nums
        return roman.get_romans(text)

    if nums := ints.get_range(text):
        return [str(n) for n in nums]

    return [str(n) for n in ints.get_ints(text)]
