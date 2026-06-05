#!/usr/bin/env python3

"""Clean and aggregate parsed trait data from LLM output JSON files."""

import argparse
import json
import logging
import textwrap
from pathlib import Path

import pandas as pd

from anoplura.fields import (
    abdomen_lengths,
    abdomen_widths,
    antenna_segments,
    body_lengths,
    dpts_lengths,
    excepts,
    geographic_locations,
    head_lengths,
    head_widths,
    host_locations,
    plates,
    specimen_types,
    spiracle_diameters,
    sternites,
    tergites,
    thorax_lengths,
    thorax_widths,
)
from anoplura.pylib import format_util, log

JSON_ERRORS = (json.JSONDecodeError, UnicodeDecodeError)

SETA_CSV = Path("anoplura/terms") / "seta_patterns.csv"


def output(args: argparse.Namespace) -> None:
    """Read LLM output JSON files and aggregate trait data."""
    log.started(args.log_file, args=args)

    with args.lm_jsonl.open() as fh:
        try:
            lines = [json.loads(ln) for ln in fh.readlines()]
            records = [{k: v or "" for k, v in r.items()} for r in lines]
        except JSON_ERRORS:
            logging.exception("JSON Error")
            raise

    species_sexes = format_util.get_column_index(records)

    df = pd.DataFrame(columns=species_sexes)

    recs = [r for r in records if r["record"] == "specimen_type"]
    df = pd.concat([df, specimen_types.build_table(recs, species_sexes)])

    # recs = [r for r in records if r["record"] == "seta_count"]
    # df = pd.concat([df, seta_counts.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "sternite"]
    df = pd.concat([df, sternites.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "tergite"]
    df = pd.concat([df, tergites.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "plate"]
    df = pd.concat([df, plates.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "antenna_segment"]
    df = pd.concat([df, antenna_segments.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "body_length"]
    df = pd.concat([df, body_lengths.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "head_length"]
    df = pd.concat([df, head_lengths.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "head_width"]
    df = pd.concat([df, head_widths.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "thorax_length"]
    df = pd.concat([df, thorax_lengths.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "thorax_width"]
    df = pd.concat([df, thorax_widths.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "abdomen_length"]
    df = pd.concat([df, abdomen_lengths.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "abdomen_width"]
    df = pd.concat([df, abdomen_widths.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "dpts_length"]
    df = pd.concat([df, dpts_lengths.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "spiracle_diameter"]
    df = pd.concat([df, spiracle_diameters.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "geographic_location"]
    df = pd.concat([df, geographic_locations.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "host_location"]
    df = pd.concat([df, host_locations.build_table(recs, species_sexes)])

    recs = [r for r in records if r["record"] == "except"]
    df = pd.concat([df, excepts.build_table(recs, species_sexes)])

    # print(df.index)
    # print(df.columns)
    # print(df.head(10))

    df.to_csv(args.csv_out)

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
