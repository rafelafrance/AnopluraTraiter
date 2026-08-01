"""Utilities for formatting extracted trait data into pivot tables."""

import pandas as pd

from anoplura.pylib import ints, ordinals, roman

REGIONS = {"abdomen": "abdominal", "thorax": "thoracic"}


def build_trait_table(
    records: list[dict],
    species_sexes: pd.MultiIndex,
    field_labels: dict[str, str],
    body_region: str = "",
) -> pd.DataFrame:
    """Build a DataFrame of trait measurements pivoted by species and sex."""
    row_labels = [(body_region, value) for value in field_labels.values()]
    row_index = pd.MultiIndex.from_tuples(row_labels, names=["region", "label"])
    df = pd.DataFrame(index=row_index, columns=species_sexes)
    for rec in records:
        for field, row_label in field_labels.items():
            df.loc[(body_region, row_label), (rec["species"], rec["sex"])] = rec[field]

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
    for rec in records:
        sex = rec.get("sex", "n/a").lower()
        if sex == "♀" or sex.startswith("f"):
            sex = "female"
        elif sex == "♂" or sex.startswith("m"):
            sex = "male"
        else:
            sex = "n/a"
        rec["sex"] = sex

        species = rec["species"]
        species = species[0].upper() + species[1:].lower()
        rec["species"] = species

    col_tuples = {(r["species"], r["sex"]) for r in records}

    order = {"male": 0, "female": 1, "n/a": 2}
    col_tuples = sorted(col_tuples, key=lambda t: (t[0], order[t[1]]))

    return pd.MultiIndex.from_tuples(col_tuples, names=["species", "sex"])


def expand_numbers(text: str) -> list[str]:
    """Expand number ranges '1-3' or 'I-III', lists '1, 2, & 3' or 'I, II, & III'."""
    if not text:
        return []

    has_ints = ints.has_ints(text)
    has_roman = roman.has_roman(text)
    has_ordinals = ordinals.has_ordinal(text)

    if not has_ints and not has_roman and not has_ordinals:
        return []

    if not has_ints and has_ordinals:
        if nums := ordinals.get_range(text):
            return nums
        return ordinals.get_ordinals(text)

    if not has_ints and has_roman:
        if nums := roman.get_range(text):
            return nums
        return roman.get_romans(text)

    if nums := ints.get_range(text):
        return [str(n) for n in nums]

    return [str(n) for n in ints.get_ints(text)]


def expand_body_region(record: dict) -> str:
    region: str = record.get("body_region", "").lower()
    return REGIONS.get(region, region)
