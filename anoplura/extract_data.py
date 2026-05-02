#!/usr/bin/env python3

"""
Extract anatomical traits from louse descriptions using an LLM API.

Iterates over a set of prompts covering different trait types, sends each
prompt together with a text file to the language model, and writes the
structured JSON results to an output directory.
"""

import argparse
import json
import logging
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any

from openai import OpenAI

from anoplura.pylib import log
from anoplura.pylib.str_util import strip_json_fences

JSON_ERRORS = (json.JSONDecodeError, UnicodeDecodeError)

SYSTEM_ROLE = textwrap.dedent("""
    You are a biologist studying lice (Anoplura). You are gathering anatomical
    trait data from taxonomic descriptions for comparative evolutionary analysis.

    You will be given a document excerpt and asked to extract specific traits.
    Follow these rules strictly:

    1. Extract ONLY data that is explicitly stated in the document. Do not infer,
       guess, or hallucinate values.
    2. If a requested trait is not mentioned in the document, omit it entirely.
       Do not include entries with all-null fields.
    3. Return your answer as a JSON array of objects. Each object uses the exact
       field names provided in the prompt.
    4. Use null for any individual field that is not available in the text.
    5. For numeric ranges written as "X–Y" or "X to Y", split into the
       designated low/high fields. For a single value, use the value field and
       leave range fields null.
    6. Output ONLY the JSON array. No prose, no explanations, no markdown fences.
    """)

PROMPTS: dict[str, Any] = {
    "specimen_types": textwrap.dedent("""
        Find the types (holotype, allotype, paratypes) and return these exact fields.
            "species": species name (string or null),
            "sex": sex of the specimen (string or null),
            "type": one of holotype, allotype, or paratypes (string or null),
            "count": exact count of paratypes as a single number (number or null),
            "male_count": number of paratype males (number or null),
            "female_count": number of paratype females (number or null).
        Return a JSON array of objects.
        """),
    "seta_counts": textwrap.dedent("""
        Find all setae counts on all body parts.
        For each seta type found, return an object with these exact fields:
            "species": species name (string or null),
            "sex": sex of the specimen (string or null),
            "body_region": body region where the seta is located (string or null),
            "seta_name": name of the seta type (string or null),
            "count": exact count if given as a single number (number or null),
            "count_low": lower bound if given as a range (number or null),
            "count_high": upper bound if given as a range (number or null),
            "side": which side of the body (string or null),
            "rows": row position of the seta (string or null).
        Return a JSON array of objects.
        """),
    "antennae_segments": textwrap.dedent("""
        Find all antennae segment counts.
        For each antennae segment count found, return an object with these exact fields:
            "species": species name (string or null),
            "sex": sex of the specimen (string or null),
            "segment_count": number of antennal segments (number or null),
            "segment_count_low": lower bound if given as a range (number or null),
            "segment_count_high": upper bound if given as a range (number or null).
        Return a JSON array of objects.
        """),
    "body_lengths": textwrap.dedent("""
        Find all body length measurements.
        For each body length found, return an object with these exact fields:
            "species": species name (string or null),
            "sex": sex of the specimen (string or null),
            "type": whether holotype or allotype (string or null),
            "length": single measurement value if given (number or null),
            "mean_length": mean body length if stated (number or null),
            "length_low": lower bound of range (number or null),
            "length_high": upper bound of range (number or null),
            "n": sample size (number or null),
            "units": unit of measurement (string or null).
        Return a JSON array of objects.
        """),
    "head_widths": textwrap.dedent("""
        Find all head width measurements.
        For each head width found, return an object with these exact fields:
            "species": species name (string or null),
            "sex": sex of the specimen (string or null),
            "width": single measurement value if given (number or null),
            "mean_width": mean head width if stated (number or null),
            "width_low": lower bound of range (number or null),
            "width_high": upper bound of range (number or null),
            "n": sample size (number or null),
            "units": unit of measurement (string or null).
        Return a JSON array of objects.
        """),
    "thorax_widths": textwrap.dedent("""
        Find all thorax width measurements.
        For each thorax width found, return an object with these exact fields:
            "species": species name (string or null),
            "sex": sex of the specimen (string or null),
            "width": single measurement value if given (number or null),
            "mean_width": mean thorax width if stated (number or null),
            "width_low": lower bound of range (number or null),
            "width_high": upper bound of range (number or null),
            "n": sample size (number or null),
            "units": unit of measurement (string or null).
        Return a JSON array of objects.
        """),
    "sternite_counts": textwrap.dedent("""
        Find all sternite counts on each segment.
        For each sternite found, return an object with these exact fields:
            "species": species name (string or null),
            "sex": sex of the specimen (string or null),
            "body_region": body region of the sternite (string or null),
            "segment": segment number or identifier (string or null),
            "sternite_name": name of the sternite (string or null),
            "count": sternite count (number or null),
            "count_low": lower bound if given as a range (number or null),
            "count_high": upper bound if given as a range (number or null).
        Return a JSON array of objects.
        """),
    "tergite_counts": textwrap.dedent("""
        Find all tergite counts on each segment.
        For each tergite found, return an object with these exact fields:
            "species": species name (string or null),
            "sex": sex of the specimen (string or null),
            "body_region": body region of the tergite (string or null),
            "segment": segment number or identifier (string or null),
            "tergite_name": name of the tergite (string or null),
            "count": tergite count (number or null),
            "count_low": lower bound if given as a range (number or null),
            "count_high": upper bound if given as a range (number or null).
        Return a JSON array of objects.
        """),
    "plate_counts": textwrap.dedent("""
        Find all plate counts on all body parts.
        For each plate found, return an object with these exact fields:
            "species": species name (string or null),
            "sex": sex of the specimen (string or null),
            "body_region": body region of the plate (string or null),
            "plate_name": name of the plate (string or null),
            "count": plate count (number or null),
            "count_low": lower bound if given as a range (number or null),
            "count_high": upper bound if given as a range (number or null).
        Return a JSON array of objects.
        """),
    "dpts_lengths": textwrap.dedent("""
        Find all DPTS (dorsal principal head seta) length measurements.
        For each DPTS length found, return an object with these exact fields:
            "species": species name (string or null),
            "sex": sex of the specimen (string or null),
            "length": single measurement value if given (number or null),
            "mean_length": mean DPTS length if stated (number or null),
            "length_low": lower bound of range (number or null),
            "length_high": upper bound of range (number or null),
            "n": sample size (number or null),
            "units": unit of measurement (string or null).
        Return a JSON array of objects.
        """),
    "spiracle_diameters": textwrap.dedent("""
        Find all mesothoracic spiracle diameter measurements.
        For each measurement found, return an object with these exact fields:
            "species": species name (string or null),
            "sex": sex of the specimen (string or null),
            "diameter": single measurement value if given (number or null),
            "mean_diameter": mean diameter if stated (number or null),
            "diameter_low": lower bound of range (number or null),
            "diameter_high": upper bound of range (number or null),
            "n": sample size (number or null),
            "units": unit of measurement (string or null).
        Return a JSON array of objects.
        """),
}


def run_lm(args: argparse.Namespace) -> None:
    """Run LLM extraction for all text files in the input directory."""
    log.started(args.log_file, args=args)

    job_began = datetime.now()

    paths = sorted(args.text_dir.glob("*.txt"))

    with OpenAI(base_url=args.api_host) as client, args.llm_jsonl.open("w") as llm_out:
        for in_path in paths:
            file_began = datetime.now()

            logging.info("-" * 80)
            logging.info("**** %s ****", in_path.stem)

            with in_path.open() as fh:
                text = fh.read()

            for key, prompt in PROMPTS.items():
                began = datetime.now()

                msg = f"{key} started"
                logging.info(msg)

                record = key.removesuffix("s")

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
                    rec = {
                        "record": record,
                        "path": str(in_path),
                        "ERROR": "Nothing returned by LLM.",
                    }
                    print(json.dumps(rec), file=llm_out, flush=True)
                    continue

                try:
                    rows = json.loads(content)
                except JSON_ERRORS:
                    logging.exception("JSON Error")
                    rec = {
                        "record": record,
                        "path": str(in_path),
                        "ERROR": "Invalid JSON returned by LLM.",
                    }
                    print(json.dumps(rec), file=llm_out, flush=True)
                    continue

                for row in rows:
                    rec = {"record": record} | row
                    print(json.dumps(rec), file=llm_out, flush=True)

                elapsed = str(datetime.now() - began)
                msg = f"{key} elapsed {elapsed}"
                logging.info(msg)

            file_elapsed = str(datetime.now() - file_began)
            msg = f"File elapsed {file_elapsed}"
            logging.info(msg)

    logging.info("-" * 80)
    job_elapsed = str(datetime.now() - job_began)
    msg = f"Job elapsed {job_elapsed}"
    logging.info(msg)

    log.finished()


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the extraction script."""
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Parse data from louse descriptions."""),
    )
    arg_parser.add_argument(
        "--text-dir",
        type=Path,
        required=True,
        metavar="PATH",
        help="""The directory containing the text files to parse.""",
    )
    arg_parser.add_argument(
        "--llm-jsonl",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Append LLM results to this JSON lines file.""",
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
