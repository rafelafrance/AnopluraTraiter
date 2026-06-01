"""Utilities for formatting extracted trait data into pivot tables."""

import pandas as pd


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
            df.loc[(rec["species"], rec["sex"]), row_label] = rec[field]

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
    col_tuples = {(r["species"], r["sex"]) for r in records}
    col_tuples = sorted(col_tuples)
    return pd.MultiIndex.from_tuples(col_tuples, names=["species", "sex"])
