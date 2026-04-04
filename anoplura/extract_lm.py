#!/usr/bin/env python3

import argparse
import json
import logging
import re
import textwrap
from datetime import datetime
from pathlib import Path

import lmstudio as lms

from anoplura.pylib import log

ERRORS = (json.JSONDecodeError, UnicodeDecodeError)

PREFIX: str = "Given the following text: "
SUFFIX: str = """
    Only get annotations from the document itself.
    If you cannot find the data do not include it.
    \n
"""

PROMPTS: dict[str, dict] = {
    "species": {
        "prompt": """
            Get the species name from the document.
            """,
    },
    "setae_counts": {
        "prompt": """
            Find all of the setae counts on all body parts.
            """,
    },
    "antennae_segments": {
        "prompt": """
            How many antennae segments are there?
            """,
    },
    "body_measurements": {
        "prompt": """
            Find the maximum body length, mean body lengths, body length range,
            and what was the sample size for body length (n=?).
            """,
    },
    "head_measurements": {
        "prompt": """
            Find the maximum head width, mean head width, head width range,
            and what was the sample size for head width (n=?).
            """,
    },
    "holotype_measurements": {
        "prompt": """
            What is the length of the holotype?
            Is the holotype female or male?
            """,
    },
    "allotype_measurements": {
        "prompt": """
            What is the length of the allotype?
            Is the allotype female or male?
            """,
    },
    "thorax_measurements": {
        "prompt": """
            Find the maximum thorax width, mean thorax width, thorax width range,
            and what was the sample size for thorax width (n=?).
            """,
    },
    "sternite_counts": {
        "prompt": """
            How many sternites are on each segment?
            """,
    },
    "tergite_counts": {
        "prompt": """
            How many tergites are on each segment?
            """,
    },
    "paratergal_plate_counts": {
        "prompt": """
            How many paratergal plates are on each segment?
            """,
    },
    "dpts_measurements": {
        "prompt": """
            Find the DPTS length, the mean DPTS length, and the range of DPTS lengths.
            """,
    },
    "mesothracic_spiracle": {
        "prompt": """
            What is the diameter of the mesothoracic spiracle?
            The mean mesothoracic diameter, and the range of mesothoracic diameters?
            """,
    },
    "denticles": {
        "prompt": """
            What is the number of anteriolaral denticles ventrally?
            What is the number of mediolateral denticles to first antennal segment on
            each side?
            """,
    },
}


def run_lm(args: argparse.Namespace) -> None:
    log.started(args.log_file, args=args)

    msg = f"Prefix = {PREFIX.strip()}"
    logging.info(msg)
    msg = f"Suffix = {SUFFIX.strip()}"
    logging.info(msg)

    for key, prompt_rec in PROMPTS.items():
        prompt, schema = prompt_rec
        msg = f"Prompt for {key}: {prompt.strip()}"
        logging.info(msg)
        msg = f"Schema for {key}: {schema.strip()}"
        logging.info(msg)

    args.json_dir.mkdir(parents=True, exist_ok=True)

    paths = sorted(args.text_dir.glob("*.txt"))

    with lms.Client() as client:
        config = lms.LlmLoadModelConfigDict(contextLength=args.context_length)
        model = client.llm.model(args.model, config=config)

        for in_path in paths:
            msg = f"**** {in_path.stem} ****"
            logging.info(msg)

            with in_path.open() as fh:
                text = fh.read()

            output = [{"text": str(in_path)}]

            for key, prompt_rec in PROMPTS.items():
                msg = f"{key} started"
                logging.info(msg)

                prompt, schema = prompt_rec

                began = datetime.now()

                prompt = prompt.strip()

                msg = PREFIX + prompt + SUFFIX
                msg += text

                chat = lms.Chat()
                chat.add_user_message(msg)

                try:
                    config = lms.LlmPredictionConfigDict(
                        temperature=args.temperature,
                        maxTokens=args.max_tokens,
                    )
                    lm_text = model.respond(chat, config=config, response_format=schema)

                except lms.LMStudioServerError as err:
                    lm_error = f"Server error: {err}"
                    logging.exception(lm_error)
                    output.append({key: str(err)})
                    continue

                if not lm_text:
                    output.append({key: "Nothing returned by the language model."})
                    continue

                try:
                    raw = re.sub(
                        r" ^ .* ( </think> | ```json ) ",
                        "",
                        str(lm_text),
                        flags=re.IGNORECASE | re.VERBOSE | re.DOTALL,
                    )
                    raw = raw.removesuffix("```")
                    results = json.loads(raw)

                except ERRORS as err:
                    lm_error = f"JSON error: {err}"
                    logging.exception(lm_error)
                    output.append({key: str(err)})
                    continue

                output.append({key: results})

                elapsed = str(datetime.now() - began)
                msg = f"{key} elapsed {elapsed}"
                logging.info(msg)

            out_path = args.json_dir / f"{in_path.stem}.json"
            with out_path.open("w") as out:
                json.dump(output, out, indent=4)

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
        help="""The directory containing the text documents to parse.""",
    )
    arg_parser.add_argument(
        "--json-dir",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the JSON results to this directory.""",
    )
    arg_parser.add_argument(
        "--model",
        default="qwen/qwen3.5-35b-a3b",
        help="""Use this language model. (default: %(default)s)""",
    )
    arg_parser.add_argument(
        "--api-host",
        default="http://localhost:1234/v1",
        help="""URL for the language model. (default: %(default)s)""",
    )
    arg_parser.add_argument(
        "--api-key",
        help="""API key.""",
    )
    arg_parser.add_argument(
        "--context-length",
        type=int,
        default=131_072,
        help="""Model's context length for input/output. (default: %(default)s)""",
    )
    arg_parser.add_argument(
        "--max-tokens",
        type=int,
        default=65_536,
        help="""Model's max tokens for output. (default: %(default)s)""",
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
