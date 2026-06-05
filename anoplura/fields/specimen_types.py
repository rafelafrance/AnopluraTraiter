"""Build a pivot table of plate notations across species and sexes."""

import pandas as pd


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of specimen type notations.

    Parameters
    ----------
    records : list[dict]
        Pre-filtered list of specimen type record dicts.
    species_sexes: pd.MultiIndex
        The two level column headers for the new data frame.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each specimen type  notation.

    """
    row_index = ["holotype", "allotype", "paratype"]
    df = pd.DataFrame(index=row_index, columns=species_sexes)

    for rec in records:
        type_ = rec["type"].lower()
        if type_ in ("holotype", "allotype"):
            df.loc[type_, (rec["species"], rec["sex"])] = "Yes"
        else:  # Handle paratype
            value = f"{rec['count']} =" if rec["count"] else ""
            if rec["male_count"]:
                value += f" {rec['male_count']}♂"
            if rec["female_count"]:
                value += f" {rec['female_count']}♀"
            value = " ".join(value.removesuffix("=").split())
            df.loc["paratype", (rec["species"], "n/a")] = value

    df = df.fillna("")
    return df
