#!/usr/bin/env python3

"""Clean and aggregate parsed trait data from LLM output JSON files."""

import argparse
import json
import logging
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import Any

from anoplura.pylib import log

JSON_ERRORS = (json.JSONDecodeError, UnicodeDecodeError)


def clean(args: argparse.Namespace) -> None:
    """Read LLM output JSON files and aggregate trait data."""
    log.started(args.log_file, args=args)

    paths = sorted(args.llm_data_dir.glob("*.json"))

    grid = defaultdict(list)

    for in_path in paths:
        logging.info(in_path)
        with in_path.open() as fh:
            try:
                data = json.load(fh)
            except JSON_ERRORS:
                logging.exception("JSON Error")
                continue

        for annotation, rows in [(k, v) for k, v in data.items() if k != "files"]:
            for row in rows:
                col = rows["species"], rows["sex"]
                # key = annotation.removesuffix("s").replace("_", " ")

                match annotation:
                    case "specimen_types":
                        grid[col].append(specimen_types(row))
                    case "seta_counts":
                        pass
                    case "antennae_segments":
                        pass
                    case "body_lengths":
                        pass
                    case "head_widths":
                        pass
                    case "thorax_widths":
                        pass
                    case "sternite_counts":
                        pass
                    case "tergite_counts":
                        pass
                    case "plate_counts":
                        pass
                    case "dpts_lengths":
                        pass
                    case "specimen_types":
                        pass
                    case "spiracle_diameters":
                        pass
                    case _:
                        raise ValueError

    for col, values in grid.items():
        print(col)
        print(values)

    log.finished()


def specimen_types(row: dict) -> tuple[str, Any]:
    """Extract specimen type and sex information from a data row."""
    type_ = row["type"].lower()

    if type_ in ("holotype", "allotype"):
        return type_, row["sex"]

    value = str(row["count"]) if row["count"] else ""
    value += f" ♂ {row['male_count']}" if row["male_count"] else ""
    value += f" ♀ {row['female_count']}" if row["female_count"] else ""

    return type_, value


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the cleaning script."""
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Clean parsed data from LLM output."""),
    )
    arg_parser.add_argument(
        "--llm-data-dir",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the results to this directory.""",
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
