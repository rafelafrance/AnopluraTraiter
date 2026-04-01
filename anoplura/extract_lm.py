#!/usr/bin/env python3

import argparse
import json
import logging
import textwrap
from datetime import datetime
from pathlib import Path

import lmstudio as lms

from anoplura.pylib import log

ERRORS = (json.JSONDecodeError, UnicodeDecodeError)

PREFIX: str = "Given the following text: "
SUFFIX: str = """
    Put the results into JSON format.
    Only get annotations from the document itself.
    If you cannot find the data do not include it.
    \n
"""

PROMPTS: dict[str, str] = {
    "setae_counts": "Find the setae counts on all body parts.",
    "gonopods": (
        "Find all of the gonopods and get their annotations including their "
        "shapes, setae, and any other information."
    ),
    "antennae_segments": (
        "Find all antennae segments and get their number, positions, and shapes"
    ),
    "leg_segments": "Find leg segments and get their number, positions, and shapes",
    # "body_segments": "Find all of body segments annotations",
    # "segment_morphology": "Get all segment morphology notations.",
    "sternite_count": "Find sternite counts on all of segments.",
    # "sternite_shape": "Find all sternite shapes.",
    "sternite_setae": "Find the setae on every sternite",
    # "sternite_morphology": "Get all sternite morphology annotations.",
    "tergite_count": "Find tergite counts on all of segments.",
    # "tergite_shape": "Find all tergite shapes.",
    "tergite_setae": "Find all setae on every tergite",
    # "tergite_morphology": "Get all tergite morphology annotations.",
    "body_part_shapes": "Get all body part shape notations.",
    "body_part_size": "Get all body part size notations.",
    # "allotype_sizes": (
    #     "Get the allotype length, mean length, length range, and sample size."
    #     "This will also include allotype body part sizes (like head) and widths."
    # ),
    # "holotype_sizes": (
    #     "Get the allotype length, mean length, length range, and sample size."
    # ),
    # "sclerotization": "Find all body part sclerotization annotations.",
}


def run_lm(args: argparse.Namespace) -> None:
    log.started(args.log_file)

    with args.text.open() as fh:
        text = fh.read()

    output = []

    with lms.Client() as client, args.output.open("w") as out:
        config = lms.LlmLoadModelConfigDict(contextLength=args.context_length)
        model = client.llm.model(args.model, config=config)

        for key, prompt in PROMPTS.items():
            logging.info(key)

            began = datetime.now()

            msg = PREFIX + prompt + SUFFIX
            logging.info(msg.strip())
            msg += text

            chat = lms.Chat()
            chat.add_user_message(msg)

            try:
                config = lms.LlmPredictionConfigDict(
                    temperature=args.temperature,
                    maxTokens=args.max_tokens,
                )
                lm_text = model.respond(chat, config=config)
            except lms.LMStudioServerError as err:
                lm_error = f"Server error: {err}"
                logging.exception(lm_error)
                output.append({key: err})
                print(lm_error, file=out)
                continue

            if not lm_text:
                output.append({key: "Nothing returned by the language model."})
                continue

            try:
                parts = str(lm_text).split("</think>")
                results = json.loads(parts[-1])
            except ERRORS as err:
                lm_error = f"JSON error: {err}"
                logging.exception(lm_error)
                output.append({key: str(err)})
                print(lm_error, file=out)
                continue

            output.append({key: results})

            elapsed = str(datetime.now() - began)
            msg = f"Elapsed {elapsed}"
            logging.info(msg)

    with args.output.open("w") as out:
        json.dump(output, out, indent=4)

    log.finished()


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Parse data from lice descriptions."""),
    )
    arg_parser.add_argument(
        "--text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""The text document to parse.""",
    )
    arg_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the results to this file.""",
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
        default=200_000,
        help="""Model's context length for input/output. (default: %(default)s)""",
    )
    arg_parser.add_argument(
        "--max-tokens",
        type=int,
        default=100_000,
        help="""Model's max tokens for output. (default: %(default)s)""",
    )
    arg_parser.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="""Model's temperature. (default: %(default)s)""",
    )
    arg_parser.add_argument(
        "--cache",
        action="store_true",
        help="""Use cached records?""",
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
