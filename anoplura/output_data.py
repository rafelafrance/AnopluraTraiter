#!/usr/bin/env python3

"""Clean and aggregate parsed trait data from LLM output JSON files."""

import argparse
import json
import logging
import textwrap
from collections import defaultdict
from pathlib import Path

import pandas as pd

from anoplura.pylib import log

JSON_ERRORS = (json.JSONDecodeError, UnicodeDecodeError)


def clean(args: argparse.Namespace) -> None:
    """Read LLM output JSON files and aggregate trait data."""
    log.started(args.log_file, args=args)

    grid = defaultdict(list)

    with args.lm_jsonl.open() as fh:
        try:
            jsonl = [json.loads(ln) for ln in fh.readlines()]
        except JSON_ERRORS:
            logging.exception("JSON Error")
            raise

    for ln in jsonl:
        sex = (ln["sex"] or "n/a").lower()
        col = ln["species"], sex

        match ln["record"]:
            case "specimen_type":
                row = specimen_type(ln)
                grid[col].append(("00|" + ln["record"], row))

            case "seta_count":
                row = seta_count(ln)
                grid[col].append(("10|" + ln["record"], row))

            case "antennae_segment":
                row = antennae_segments(ln)
                grid[col].append(("20|" + ln["record"], row))

            case "body_length":
                rows = body_length(ln)
                grid[col] += [("30|" + ln["record"], r) for r in rows]

            case "head_width":
                rows = head_width(ln)
                grid[col] += [("40|" + ln["record"], r) for r in rows]

            case "thorax_width":
                rows = thorax_width(ln)
                grid[col] += [("50|" + ln["record"], r) for r in rows]

            case "sternite_count":
                row = sternite_count(ln)
                grid[col].append(("60|" + ln["record"], row))

            case "tergite_count":
                row = tergite_count(ln)
                grid[col].append(("70|" + ln["record"], row))

            case "plate_count":
                row = plate_count(ln)
                grid[col].append(("80|" + ln["record"], row))

            case "dpts_length":
                rows = dpts_length(ln)
                grid[col] += [("90|" + ln["record"], r) for r in rows]

            case "spiracle_diameter":
                rows = spiracle_diameter(ln)
                grid[col] += [("a0|" + ln["record"], r) for r in rows]

            case "except":
                row = excepts(ln)
                grid[col].append(("b0|" + ln["record"], row))

            case _:
                print(ln["record"])
                raise ValueError

    # Get row names
    order = set()
    for rows in grid.values():
        for row in rows:
            order.add((row[0], row[1][0]))
    order = sorted(order)
    # print(order)

    arrays = [k[0] for k in grid], [k[1] for k in grid]
    headers = pd.MultiIndex.from_arrays(arrays, names=("species", "sex"))
    df = pd.DataFrame(index=[o[1] for o in order], columns=headers)

    for key, rows in grid.items():
        for row in rows:
            df.loc[row[1][0], key] = row[1][1]

    df.to_csv(args.csv_out)

    log.finished()


def excepts(ln: dict) -> tuple[str, str]:
    """Extract exception notations the data."""
    return "except phrase", ln["phrase"]


def spiracle_diameter(ln: dict) -> list[tuple[str, str]]:
    """Extract the various spiracle diameter measurements."""
    lens = []

    units = f" {ln['units']}" if ln["units"] else ""

    if ln["diameter"] is not None:
        label = "spiracle diameter"
        value = f"{ln['diameter']}{units}"
        lens.append((label, value))

    if ln["mean_diameter"] is not None:
        label = "mean spiracle diameter"
        value = f"{ln['mean_diameter']}{units}"
        lens.append((label, value))

    if ln["diameter_low"] is not None and ln["diameter_high"] is not None:
        label = "spiracle diameter range"
        value = f"{ln['diameter_low']}-{ln['diameter_high']}{units}"
        lens.append((label, value))

    if ln["n"] is not None:
        label = "spiracle diameter sample size"
        value = f"{ln['n']}"
        lens.append((label, value))

    return lens


def dpts_length(ln: dict) -> list[tuple[str, str]]:
    """Extract the various DPTS length measurements."""
    lens = []

    units = f" {ln['units']}" if ln["units"] else ""

    if ln["length"] is not None:
        label = "DPTS length"
        value = f"{ln['length']}{units}"
        lens.append((label, value))

    if ln["mean_length"] is not None:
        label = "mean DPTS length"
        value = f"{ln['mean_length']}{units}"
        lens.append((label, value))

    if ln["length_low"] is not None and ln["length_high"] is not None:
        label = "DPTS length range"
        value = f"{ln['length_low']}-{ln['length_high']}{units}"
        lens.append((label, value))

    if ln["n"] is not None:
        label = "DPTS length sample size"
        value = f"{ln['n']}"
        lens.append((label, value))

    return lens


def plate_count(ln: dict) -> tuple[str, str]:
    """Extract plate counts and format the data."""
    label = []
    if ln["body_region"] is not None:
        label.append(ln["body_region"])
    if ln["plate_name"] is not None:
        label.append(ln["plate_name"])
    label.append("plate count")

    value = []
    if ln["count_low"] is not None and ln["count_high"] is not None:
        value.append(f"{ln['count_low']}-{ln['count_high']}")
    elif ln["count"] is not None:
        value.append(str(ln["count"]))

    return " ".join(label).lower(), " ".join(value).lower()


def tergite_count(ln: dict) -> tuple[str, str]:
    """Extract tergite counts and format the data."""
    label = []
    if ln["body_region"] is not None:
        label.append(ln["body_region"])
    if ln["segment"] is not None:
        label.append(f"segment {ln['segment']}")
    if ln["tergite_name"] is not None:
        label.append(ln["tergite_name"])
    label.append("tergite count")

    value = []
    if ln["count_low"] is not None and ln["count_high"] is not None:
        value.append(f"{ln['count_low']}-{ln['count_high']}")
    elif ln["count"] is not None:
        value.append(str(ln["count"]))

    return " ".join(label).lower(), " ".join(value).lower()


def sternite_count(ln: dict) -> tuple[str, str]:
    """Extract sternite counts and format the data."""
    label = []
    if ln["body_region"] is not None:
        label.append(ln["body_region"])
    if ln["segment"] is not None:
        label.append(f"segment {ln['segment']}")
    if ln["sternite_name"] is not None:
        label.append(ln["sternite_name"])
    label.append("sternite count")

    value = []
    if ln["count_low"] is not None and ln["count_high"] is not None:
        value.append(f"{ln['count_low']}-{ln['count_high']}")
    elif ln["count"] is not None:
        value.append(str(ln["count"]))

    return " ".join(label).lower(), " ".join(value).lower()


def thorax_width(ln: dict) -> list[tuple[str, str]]:
    """Extract the various thorax width measurements."""
    lens = []

    units = f" {ln['units']}" if ln["units"] else ""

    if ln["width"] is not None:
        label = "thorax width"
        value = f"{ln['width']}{units}"
        lens.append((label, value))

    if ln["mean_width"] is not None:
        label = "mean thorax width"
        value = f"{ln['mean_width']}{units}"
        lens.append((label, value))

    if ln["width_low"] is not None and ln["width_high"] is not None:
        label = "thorax width range"
        value = f"{ln['width_low']}-{ln['width_high']}{units}"
        lens.append((label, value))

    if ln["n"] is not None:
        label = "thorax width sample size"
        value = f"{ln['n']}"
        lens.append((label, value))

    return lens


def head_width(ln: dict) -> list[tuple[str, str]]:
    """Extract the various head width measurements."""
    lens = []

    units = f" {ln['units']}" if ln["units"] else ""

    if ln["width"] is not None:
        label = "head width"
        value = f"{ln['width']}{units}"
        lens.append((label, value))

    if ln["mean_width"] is not None:
        label = "mean head width"
        value = f"{ln['mean_width']}{units}"
        lens.append((label, value))

    if ln["width_low"] is not None and ln["width_high"] is not None:
        label = "head width range"
        value = f"{ln['width_low']}-{ln['width_high']}{units}"
        lens.append((label, value))

    if ln["n"] is not None:
        label = "head width sample size"
        value = f"{ln['n']}"
        lens.append((label, value))

    return lens


def body_length(ln: dict) -> list[tuple[str, str]]:
    """Extract the various body length measurements."""
    lens = []

    units = f" {ln['units']}" if ln["units"] else ""

    if ln["length"] is not None:
        label = "body length"
        value = f"{ln['length']}{units}"
        lens.append((label, value))

    if ln["mean_length"] is not None:
        label = "mean body length"
        value = f"{ln['mean_length']}{units}"
        lens.append((label, value))

    if ln["length_low"] is not None and ln["length_high"] is not None:
        label = "body length range"
        value = f"{ln['length_low']}-{ln['length_high']}{units}"
        lens.append((label, value))

    if ln["n"] is not None:
        label = "body length sample size"
        value = f"{ln['n']}"
        lens.append((label, value))

    return lens


def antennae_segments(ln: dict) -> tuple[str, str]:
    """Extract the number of antennae segments and format the data."""
    return "number of antennal segments", str(ln["segment_count"])


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


def specimen_type(ln: dict) -> tuple[str, str]:
    """Extract specimen type and sex information from a data ln."""
    label = ln["type"].lower()

    if label in ("holotype", "allotype"):
        return label, ln["sex"]

    value = f"count {ln['count']}," if ln["count"] else ""
    value += f" ♂ {ln['male_count']}," if ln["male_count"] else ""
    value += f" ♀ {ln['female_count']}" if ln["female_count"] else ""
    value = value.removesuffix(",")

    return label, value


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
