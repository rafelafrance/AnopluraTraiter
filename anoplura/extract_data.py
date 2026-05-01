#!/usr/bin/env python3

import argparse
import json
import logging
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any

from openai import OpenAI

from anoplura.pylib import log
from anoplura.pylib.str_util import compress, strip_json_fences

JSON_ERRORS = (json.JSONDecodeError, UnicodeDecodeError)

SYSTEM_ROLE = compress("""
    You are a biologist studying lice.
    You are gathering anatomical information of lice species in order to compare them
    for evolutionary trends.

    We will ask you to find specific traits of interest in a document.

    Only get annotations from the document itself.
    If you cannot find the data do not include it.
    Return the results in JSON format.
    """)

PROMPTS: dict[str, Any] = {
    "seta_counts": compress("""
        Find all of the setae counts on all body parts.
        For each seta list:
            The species of the louse,
            The sex of the louse,
            The body region of the seta,
            The name of the seta,
            What is the seta count,
            Which side are the seta on,
            What rows the seta are in.
        Use null for any missing data.
        """),
    "antennae_segments": compress("""
        How many antennae segments are there?
        Find all of the antennae segment counts.
        For each antennae segments count get:
            The species of the louse,
            The sex of the louse,
            The antennal segment count.
        Use null for any missing data.
        """),
    "body_length": compress("""
        For each body length get:
            The species of the louse,
            The sex of the louse,
            Is this a holotype or allotype,
            The total body length,
            The maximum body length,
            The mean body length,
            The the range of body lengths,
        What was the sample size for body lengths (n=?).
        Use null for any missing data.
        """),
    "head_width": compress("""
        For each head width get:
            The species of the louse,
            The sex of the louse,
            The head width,
            The maximum head width,
            The mean head width,
            The the range of head widths,
            What was the sample size for the head widths (n=?).
        Use null for any missing data.
        """),
    "thorax_width": compress("""
        For each throax width get:
            The species of the louse,
            The sex of the louse,
            The thorax width,
            The maximum thorax width,
            The mean thorax width,
            The the range of thorax widths,
            What was the sample size for the thorax widths (n=?).
        Use null for any missing data.
        """),
    "sternite_counts": compress("""
        Find all or the sternite counts on each segment.
        For each sternite list:
            The species of the louse,
            The sex of the louse,
            The body region of the sternite,
            Which segment the sternites are on,
            The name of the sternite,
            What is the sternite count.
        Use null for any missing data.
        """),
    "tergite_counts": compress("""
        Find all or the tergite counts on each segment.
        For each tergite list:
            The species of the louse,
            The sex of the louse,
            The body region of the tergite,
            Which segment the tergites are on,
            The name of the tergite,
            What is the tergite count.
        Use null for any missing data.
        """),
    "plate_counts": compress("""
        Find all of the plate counts on all body parts.
        For each plate list:
            The species of the louse,
            The sex of the louse,
            The body region of the plate,
            The name of the plate,
            What is the plate count,
        Use null for any missing data.
        """),
    "dpts_length": compress("""
        The DPTS is also known as the dorsal principal head seta.
        For each DPTS length get:
            The species of the louse,
            The sex of the louse,
            The DPTS length,
            The maximum DPTS length,
            The mean DPTS length,
            The the range of DPTS lengths,
            What was the sample size for the DPTS lengths (n=?).
        Use null for any missing data.
        """),
    "mesothracic_spiracle": compress("""
        What is the diameter of the mesothoracic spiracle?
        For each diameter of the mesothoracic spiracle get:
            The species of the louse,
            The sex of the louse,
            The diameter of the mesothoracic spiracle,
            The maximum diameter of the mesothoracic spiracle,
            The mean diameter of the mesothoracic spiracle,
            The the range of mesothoracic spiracle diameters,
            What was the sample size for the mesothoracic spiracle diameters (n=?).
        Use null for any missing data.
        """),
    "denticle_counts": compress("""
        Find all the number of anteriolaral denticles ventrally?
        Also find the number of mediolateral denticles to first antennal segment.
        For each denticle count list:
            The species of the louse,
            The sex of the louse,
            The body region of the denticle,
            The name of the denticle,
            What is the denticle count,
            Which side the denticles are on.
        Use null for any missing data.
        """),
}


def run_lm(args: argparse.Namespace) -> None:
    log.started(args.log_file, args=args)

    args.raw_data_dir.mkdir(parents=True, exist_ok=True)

    paths = sorted(args.text_dir.glob("*.txt"))

    with OpenAI(base_url=args.api_host) as client:
        for in_path in paths:
            logging.info("**** %s ****", in_path.stem)

            with in_path.open() as fh:
                text = fh.read()

            output = [{"text": json.dumps({"text_file": in_path.name})}]

            for key, prompt in PROMPTS.items():
                msg = f"{key} started"
                logging.info(msg)

                began = datetime.now()

                response = client.chat.completions.create(
                    model=args.model_name,
                    messages=[
                        {"role": "system", "content": SYSTEM_ROLE},
                        {"role": "user", "content": prompt},
                        {"role": "user", "content": text},
                    ],
                    temperature=args.temperature,
                )
                content = response.choices[0].message.content or ""
                content = strip_json_fences(content)

                if not content:
                    output.append({key: "Nothing returned by the language model."})
                    continue

                try:
                    value = json.loads(content)
                except JSON_ERRORS:
                    logging.exception("JSON Error")
                    output.append({key: "Invalid JSON returned by the language model."})
                    continue

                output.append({key: value})

                elapsed = str(datetime.now() - began)
                msg = f"{key} elapsed {elapsed}"
                logging.info(msg)

            out_path = args.raw_data_dir / f"{in_path.stem}.json"
            with out_path.open("w") as f_out:
                json.dump(output, f_out, indent=4)

    log.finished()


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Parse data from lice descriptions."""),
    )
    arg_parser.add_argument(
        "--text-dir",
        type=Path,
        required=True,
        metavar="PATH",
        help="""The directory containing the text files to parse.""",
    )
    arg_parser.add_argument(
        "--raw-data-dir",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the raw language model results to this directory.""",
    )
    arg_parser.add_argument(
        "--model-name",
        default="google/gemma-4-26b-a4b",
        help="""Use this language model. (default: %(default)s)""",
    )
    # arg_parser.add_argument(
    #     "--threads",
    #     type=int,
    #     default=4,
    #     help="""How many parallel threads to run. (default: %(default)s)""",
    # )
    arg_parser.add_argument(
        "--api-host",
        default="http://localhost:1234/v1",
        help="""URL for the language model. (default: %(default)s)""",
    )
    arg_parser.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="""Model's temperature. (default: %(default)s)""",
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
    run_lm(ARGS)
