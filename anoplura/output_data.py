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
            case "seta_count":
                row = seta_count(ln)
                grid[col].append(("10|" + ln["record"], row))

            case "sternite_count":
                row = count(ln, "sternite")
                grid[col].append(("60|" + ln["record"], row))

            case "tergite_count":
                row = count(ln, "tergite")
                grid[col].append(("70|" + ln["record"], row))

            case "plate_count":
                row = count(ln, "plate")
                grid[col].append(("80|" + ln["record"], row))

            case "body_length":
                rows = measurement(ln, "body", "length")
                grid[col] += [("30|" + ln["record"], r) for r in rows]

            case "head_length":
                rows = measurement(ln, "head", "length")
                grid[col] += [("40|" + ln["record"], r) for r in rows]

            case "head_width":
                rows = measurement(ln, "head", "width")
                grid[col] += [("40|" + ln["record"], r) for r in rows]

            case "thorax_length":
                rows = measurement(ln, "thorax", "length")
                grid[col] += [("50|" + ln["record"], r) for r in rows]

            case "thorax_width":
                rows = measurement(ln, "thorax", "width")
                grid[col] += [("50|" + ln["record"], r) for r in rows]

            case "abdomen_length":
                rows = measurement(ln, "abdomen", "length")
                grid[col] += [("50|" + ln["record"], r) for r in rows]

            case "dpts_length":
                rows = measurement(ln, "DPTS", "length")
                grid[col] += [("90|" + ln["record"], r) for r in rows]

            case "spiracle_diameter":
                rows = measurement(ln, "spiracle", "diameter")
                grid[col] += [("a0|" + ln["record"], r) for r in rows]

            case "specimen_type":
                row = specimen_type(ln)
                grid[col].append(("00|" + ln["record"], row))

            case "antennae_segment":
                row = antennae_segments(ln)
                grid[col].append(("20|" + ln["record"], row))

            case "except":
                row = excepts(ln)
                grid[col].append(("b0|" + ln["record"], row))

            case _:
                logging.error(f"Unknown record type: {ln['record']}")
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


def count(ln: dict, part: str, label: list[str] | None = None) -> tuple[str, str]:
    """Extract part counts and format the data."""
    label = label or []

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


def antennae_segments(ln: dict) -> tuple[str, str]:
    """Extract the number of antennae segments and format the data."""
    return "number of antennal segments", str(ln["segment_count"])


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
