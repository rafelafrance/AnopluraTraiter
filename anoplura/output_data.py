#!/usr/bin/env python3

"""Clean and aggregate parsed trait data from LLM output JSON files."""

import argparse
import json
import logging
import textwrap
from pathlib import Path

from anoplura.fields import plates
from anoplura.pylib import format_util, log

JSON_ERRORS = (json.JSONDecodeError, UnicodeDecodeError)

SETA_CSV = Path("anoplura/terms") / "seta_patterns.csv"


def output(args: argparse.Namespace) -> None:
    """Read LLM output JSON files and aggregate trait data."""
    log.started(args.log_file, args=args)

    with args.lm_jsonl.open() as fh:
        try:
            records = [json.loads(ln) for ln in fh.readlines()]
        except JSON_ERRORS:
            logging.exception("JSON Error")
            raise

    species_sexes = format_util.get_column_index(records)

    plate_recs = [r for r in records if r["record"] == "plate"]
    plates.build_table(plate_recs, species_sexes)

    log.finished()


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
    output(ARGS)
