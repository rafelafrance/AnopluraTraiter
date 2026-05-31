"""Build a pivot table of abdomen width traits across species and sexes."""

import json
from pathlib import Path

import pandas as pd

DEFAULT_JSONL = Path("tests/info/extracts.jsonl")

ROW_LABELS = [
    "abdomen width",
    "mean abdomen width",
    "low abdomen width",
    "high abdomen width",
    "abdomen width sample size (n)",
]

TRAIT_FIELDS = ["width", "mean_width", "width_low", "width_high", "n"]


def build_table(jsonl_path: Path | str = DEFAULT_JSONL) -> pd.DataFrame:
    """
    Build a DataFrame of abdomen width measurements.

    Parameters
    ----------
    jsonl_path : Path or str
        Path to the JSONL file containing extracted trait records.

    Returns
    -------
    pd.DataFrame
        DataFrame with a MultiIndex column of (species, sex) and row
        labels describing each abdomen width sub-trait.

    """
    jsonl_path = Path(jsonl_path)

    records = []
    with jsonl_path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    abdomen_records = [r for r in records if r["record"] == "abdomen_width"]

    # Collect unique (species, sex) column pairs in order of appearance
    col_tuples: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for r in abdomen_records:
        key = (r["species"], r["sex"])
        if key not in seen:
            seen.add(key)
            col_tuples.append(key)

    col_index = pd.MultiIndex.from_tuples(col_tuples, names=["species", "sex"])

    # Build data rows
    data_rows: list[dict] = []
    for f in TRAIT_FIELDS:
        row_vals: dict = {}
        for col in col_tuples:
            matching = [
                r
                for r in abdomen_records
                if r["species"] == col[0] and r["sex"] == col[1]
            ]
            val = matching[0].get(f) if matching else None
            # Keep n as string to avoid float conversion in pandas
            if f == "n" and val is not None:
                val = str(val)
            row_vals[col] = val
        data_rows.append(row_vals)

    df = pd.DataFrame(data_rows, index=ROW_LABELS, columns=col_index)
    df = df.fillna("")

    return df


if __name__ == "__main__":
    df = build_table()
    print(df.to_string())
    print(f"\nShape: {df.shape}")
