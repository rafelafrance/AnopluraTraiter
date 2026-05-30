#!/usr/bin/env python3

"""Clean and aggregate parsed trait data from LLM output JSON files."""

import argparse
import csv
import json
import logging
import re
import textwrap
from collections import defaultdict
from pathlib import Path

import pandas as pd

from anoplura.pylib import ints, log, roman

JSON_ERRORS = (json.JSONDecodeError, UnicodeDecodeError)

SETA_CSV = Path("anoplura/terms") / "seta_patterns.csv"

SIZES = [
    ("body", "length"),
    ("head", "length"),
    ("head", "width"),
    ("abdomen", "length"),
    ("abdomen", "width"),
    ("thorax", "length"),
    ("thorax", "width"),
    ("DPTS", "length"),
    ("spiracle", "diameter"),
]


def clean(args: argparse.Namespace) -> None:
    """Read LLM output JSON files and aggregate trait data."""
    log.started(args.log_file, args=args)

    with SETA_CSV.open() as f:
        reader = csv.DictReader(f)
        setae = list(reader)

    with args.lm_jsonl.open() as fh:
        try:
            lines = [json.loads(ln) for ln in fh.readlines()]
        except JSON_ERRORS:
            logging.exception("JSON Error")
            raise

    row_index = get_row_index(lines, setae)
    for r in row_index:
        print(r)
    return
    arrays = get_col_index(lines)
    headers = pd.MultiIndex.from_arrays(arrays, names=("species", "sex"))
    df = pd.DataFrame(index=row_index, columns=headers)

    for ln in lines:
        match ln["record"]:
            # case "seta_count":
            #     seta_count(ln)

            case "sternite_count":
                count(ln, "sternite")

            # case "tergite_count":
            #     count(ln, "tergite")
            #
            # case "plate_count":
            #     count(ln, "plate")
            #
            # case "body_length":
            #     measurement(ln, "body", "length")
            #
            # case "head_length":
            #     measurement(ln, "head", "length")
            #
            # case "head_width":
            #     measurement(ln, "head", "width")
            #
            # case "thorax_length":
            #     measurement(ln, "thorax", "length")
            #
            # case "thorax_width":
            #     measurement(ln, "thorax", "width")
            #
            # case "abdomen_length":
            #     measurement(ln, "abdomen", "length")
            #
            # case "dpts_length":
            #     measurement(ln, "DPTS", "length")
            #
            # case "spiracle_diameter":
            #     measurement(ln, "spiracle", "diameter")

            case "specimen_type":
                specimen_type(df, ln)

            # case "antennae_segment":
            #     antennae_segments(ln)
            #
            # case "except":
            #     excepts(ln)
            #
            # case _:
            #     logging.error(f"Unknown record type: {ln['record']}")
            #     raise ValueError

    df = df.fillna("")
    # print(df.head())

    df.to_csv(args.csv_out)

    log.finished()


def get_col_index(rows: list[dict]) -> tuple[list[str], list[str]]:
    """Assign column index names."""
    species, sexes = [], []
    specs = {r["species"] for r in rows}
    specs = sorted(species)
    for spec in specs:
        species += [spec * 3]
        sexes += ["male", "female", "N/A"]
    return species, sexes


def get_row_index(lines: list[dict], seta_list: list[dict]) -> list[str]:
    """Assign row index names to each column."""
    keys = ["holotype", "allotype", "paratype"]

    sternites: list[str] = []
    tergites: list[str] = []
    plates: list[str] = []
    excepts = defaultdict(int)

    setae: dict[str, dict] = {s["pattern"]: s for s in seta_list}
    row_seta = set()

    for ln in lines:
        match ln["record"]:
            case "seta_count":
                _process_seta_count(ln, setae, row_seta)

            case "sternite_count":
                sternites += _process_sternite_count(ln)

            case "tergite_count":
                tergites += _process_tergite_count(ln)

            # case "plate_count":
            #     plate = ln.get("plate_name", ln.get("body_region")).lower()
            #     plate = plate.replace("plates", plate)
            #     plates.add(plate)

            case "except":
                species = ln["species"]
                sex = ln["sex"] or "n/a"
                excepts[species, sex] += 1

    keys += [s[1] for s in sorted(row_seta)]

    keys += sorted(set(sternites))
    keys += sorted(set(tergites))
    keys += sorted(set(plates))

    for part, dim in SIZES:
        keys.append(f"{part} {dim}")
        keys.append(f"{part} {dim} mean")
        keys.append(f"{part} {dim} low")
        keys.append(f"{part} {dim} high")
        keys.append(f"{part} {dim} sample size")
        keys.append(f"{part} {dim} units")

    keys += [
        "antennae segment count",
        "antennae segment count low",
        "antennae segment count high",
        "host species",
        "geographic location",
        "host location",
    ]

    max_excepts = max(v for v in excepts.values())
    keys += [f"except {i}" for i in range(1, max_excepts + 1)]

    return keys


def _process_seta_count(ln: dict, setae: dict, row_seta: set) -> None:
    """Process a seta_count record and add row labels to row_seta."""
    name = (ln["seta_name"] or "").lower()
    name = name.replace("setae", "seta")
    match = re.search(r"\((\w+)\)", name)
    abbrev = match.group(1) if match else ""
    abbrev = name if not abbrev and len(name.split()) == 1 else abbrev
    seta = setae.get(abbrev, setae.get(name))

    if seta:
        row_seta.add((seta["part"], seta["replace"] + " count"))

    else:
        parts = []

        body = (ln["body_region"] or "").lower()
        if body:
            parts.append(body)

        seg = (ln["segment"] or "").lower()
        if seg and seg not in parts:
            # segs = _parse_segments(seg)
            parts.append(f"segment {seg}")

        if name and name not in parts:
            parts.append(name)

        seta = " ".join(parts)
        if seta and body:
            seta += " seta" if not seta.endswith("seta") else ""
            seta += " count"
            row_seta.add((body, seta))


def _process_sternite_count(ln: dict) -> list[str]:
    """Process a sternite_count record and add the label to sternites."""
    if ln["segment"] is None and ln["missing"]:
        return ["sternites missing"]
    if ln["segment"]:
        return [
            f"sternite count for segment {s}" for s in _expand_numbers(ln["segment"])
        ]
    if ln["body_region"]:
        return [f"sternite count for {ln['body_region'].lower()}"]
    raise ValueError(ln)


def _process_tergite_count(ln: dict) -> list[str]:
    """Process a tergite_count record and add the label to tergites."""
    if ln["segment"] is None and ln["missing"]:
        return ["tergites missing"]
    if ln["segment"]:
        return [
            f"tergite count for segment {s}" for s in _expand_numbers(ln["segment"])
        ]
    if ln["body_region"]:
        return [f"tergite count for {ln['body_region'].lower()}"]
    raise ValueError(ln)


def _expand_numbers(text: str) -> list[str]:
    """Expand number ranges '1-3' and lists '1, 2, & 3'."""
    if not text:
        return []

    has_ints = ints.has_ints(text)
    has_roman = roman.has_roman(text)

    if not has_ints and not has_roman:
        return [f"{text}"]

    if not has_ints and has_roman:
        if nums := roman.get_range(text):
            return nums
        return roman.get_romans(text)

    if nums := ints.get_range(text):
        return [str(n) for n in nums]
    return [str(n) for n in ints.get_ints(text)]


def specimen_type(df: pd.DataFrame, ln: dict) -> None:
    """Extract specimen type and sex information from a json line."""
    species = ln["species"]
    sex = ln["sex"] or "n/a"
    match ln["type"]:
        case "holotype":
            df.loc["holotype", (species, sex)] = "Yes"
        case "allotype":
            df.loc["allotype", (species, sex)] = "Yes"
        case "paratypes":
            value = f"count {ln['count']}," if ln["count"] else ""
            value += f" ♂ {ln['male_count']}," if ln["male_count"] else ""
            value += f" ♀ {ln['female_count']}" if ln["female_count"] else ""
            value = value.removesuffix(",")
            df.loc["paratype", (species, sex)] = value
        case None:
            pass
        case _:
            logging.error(f"Unknown specimen type: {ln['type']} {species} {sex}")
            raise ValueError


def count(df: pd.DataFrame, ln: dict, part: str) -> tuple[str, str]:
    """Extract part counts and format the data."""
    species = ln["species"]
    sex = ln["sex"] or "n/a"

    df.loc[f"{part} count", (species, sex)] = ln[""]

    label = ""

    region = ln.get("body region")
    if region is not None:
        label.append(region)

    segment = ln.get("segment")
    if segment is not None:
        label.append(f"segment {segment}")

    name = ln.get(f"{part}_name")
    if name is not None:
        label.append(name)
    label.append(f"{part} count")

    value = []
    if ln.get("count_low") is not None and ln.get("count_high") is not None:
        value.append(f"{ln['count_low']}-{ln['count_high']}")
    elif ln.get("count") is not None:
        value.append(str(ln["count"]))

    return " ".join(label).lower(), " ".join(value).lower()


def excepts(ln: dict) -> tuple[str, str]:
    """Extract exception notations the data."""
    return "except phrase", ln["phrase"]


def measurement(ln: dict, part: str, dimension: str) -> list[tuple[str, str]]:
    """Extract the various measurements."""
    values = []

    units = f" {ln['units']}" if ln["units"] else ""

    mean = ln.get(f"mean_{dimension}")
    low = ln.get(f"{dimension}_low")
    high = ln.get(f"{dimension}_high")
    n = ln.get("n")

    if ln[dimension] is not None:
        label = f"{part} {dimension}"
        value = f"{ln[dimension]}{units}"
        values.append((label, value))

    if mean is not None:
        label = f"mean {part} {dimension}"
        value = f"{mean}{units}"
        values.append((label, value))

    if low is not None and high is not None:
        label = f"{part} {dimension} range"
        value = f"{low}-{high}{units}"
        values.append((label, value))

    if n is not None:
        label = f"{part} {dimension} sample size"
        value = str(n)
        values.append((label, value))

    return values


def seta_count(ln: dict) -> tuple[str, str]:
    """Extract setae counts and format the data."""
    label = [ln[f] for f in ("body_region", "seta_name") if f is not None]
    if label[-1].endswith("setae"):
        pass
    elif label[-1].endswith("seta"):
        label[-1] = "setae"
    else:
        label.append("setae")
    label.append("count")

    value = []
    if ln["count_low"] is not None and ln["count_high"] is not None:
        value.append(f"{ln['count_low']}-{ln['count_high']}")
    elif ln["count"] is not None:
        value.append(str(ln["count"]))

    value += [str(ln[f]) for f in ("rows", "side") if ln[f] is not None]

    return " ".join(label).lower(), " ".join(value).lower()


def antennae_segments(ln: dict) -> tuple[str, str]:
    """Extract the number of antennae segments and format the data."""
    return "number of antennal segments", str(ln["segment_count"])


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the cleaning script."""
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Clean parsed data from LLM output."""),
    )
    arg_parser.add_argument(
        "--lm-jsonl",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Read LM results from this JSON lines file.""",
    )
    arg_parser.add_argument(
        "--csv-out",
        type=Path,
        required=True,
        metavar="PATH",
        help="""The directory containing the cleaned language model output.""",
    )
    arg_parser.add_argument(
        "--log-file",
        type=Path,
        help="""Append logging notices to this file. It also logs the script arguments
            so you may use this to keep track of what you did.""",
    )
    arg_parser.add_argument(
        "--notes",
        help="""Notes for logging.""",
    )
    ns: argparse.Namespace = arg_parser.parse_args(args)
    return ns


if __name__ == "__main__":
    ARGS = parse_args()
    clean(ARGS)
