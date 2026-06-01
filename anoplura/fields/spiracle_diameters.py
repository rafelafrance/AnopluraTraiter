"""Build a pivot table of spiracle diameters across species, sexes, & locations."""

import pandas as pd

from anoplura.pylib import format_util

FIELD_LABELS = {
    "diameter": "spiracle diameter ({location})",
    "mean_diameter": "mean spiracle diameter ({location})",
    "diameter_low": "low spiracle diameter ({location})",
    "diameter_high": "high spiracle diameter ({location})",
    "n": "spiracle diameter sample size ({location})",
}


def build_table(records: list[dict], species_sexes: pd.MultiIndex) -> pd.DataFrame:
    """
    Build a DataFrame of spiracle diameter measurements.

    Row labels incorporate the spiracle location (e.g. mesothorax,
    5th abdominal segment).

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
        labels describing each spiracle diameter sub-trait per location.

    """
    # Get all spiracle locations
    locations = sorted({r["location"] for r in records})

    rows = []
    for loc in locations:
        recs = [r for r in records if r["location"] == loc]
        field_labels = {
            k: v.format(loc) if loc else v.removesuffix(" ({location})")
            for k, v in FIELD_LABELS.items()
        }
        rows.append(format_util.build_trait_table(recs, species_sexes, field_labels))

    df = pd.concat(rows)
    return df
