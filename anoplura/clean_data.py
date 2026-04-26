#!/usr/bin/env python3

import argparse
import json
import logging
import textwrap
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pandas as pd

from anoplura.pylib import log, str_util

JSON_ERRORS = (json.JSONDecodeError, UnicodeDecodeError)


def clean(args: argparse.Namespace) -> None:
    log.started(args.log_file, args=args)

    args.cleaned_lm_dir.mkdir(parents=True, exist_ok=True)

    paths = sorted(args.raw_lm_dir.glob("*.json"))

    for in_path in paths:
        with in_path.open() as fh:
            data = json.load(fh)

        out = {}
        for parsed in data:
            for key, value in parsed.items():
                raw = str_util.compress(value)  # ################################

                try:
                    obj = json.loads(raw)
                except JSON_ERRORS:
                    logging.exception("JSON Error")
                    break

                out |= CLEANERS[key](obj)

        out = json.dumps(out, indent=4)
        print(out)

    log.finished()


def echo(obj: dict) -> dict[str, Any]:
    return obj


def setae_counts(obj: dict) -> dict[str, Any]:
    new = pd.json_normalize(obj).to_dict(orient="records")
    new = new[0]
    return {"setae_counts": new[0]}


CLEANERS: dict[str, Callable] = {
    "text": echo,
    "species": echo,
    "setae_counts": setae_counts,
    # "antennae_segments": antennae_segments,
    # "body_measurements": body_measurements,
    # "head_measurements": head_measurements,
    # "holotype_measurements": holotype_measurements,
    # "allotype_measurements": allotype_measurements,
    # "thorax_measurements": thorax_measurements,
    # "sternite_counts": sternite_counts,
    # "tergite_counts": tergite_counts,
    # "paratergal_plate_counts": paratergal_plate_counts,
    # "dpts_measurements": dpts_measurements,
    # "mesothracic_spiracle": mesothracic_spiracle,
    # "denticles": denticles,
}


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Clean parsed data from LLM output."""),
    )
    arg_parser.add_argument(
        "--raw-data-dir",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the results to this directory.""",
    )
    arg_parser.add_argument(
        "--cleaned-data-dir",
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
