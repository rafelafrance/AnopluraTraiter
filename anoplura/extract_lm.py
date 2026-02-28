#!/usr/bin/env python3

import argparse
import textwrap
from pathlib import Path
from pprint import pp

import dspy
import lmstudio as lms
from rich import print as rprint

from anoplura.signatures.louse import SetaeCounts

PREFIX: str = "Given the following text: "
SUFFIX: str = """
    \n
    Only get annotations from the document itself.
    If you cannot find the data do not include it.
    \n\n
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
    "body_segments": "Find all of body segments annotations",
    "segment_morphology": "Get all segment morphology notations.",
    "sternite_count": "Find sternite counts on all of segments.",
    "sternite_shape": "Find all sternite shapes.",
    "sternite_setae": "Find the setae on every sternite",
    "sternite_morphology": "Get all sternite morphology annotations.",
    "tergite_count": "Find tergite counts on all of segments.",
    "tergite_shape": "Find all tergite shapes.",
    "tergite_setae": "Find all setae on every tergite",
    "tergite_morphology": "Get all tergite morphology annotations.",
    "body_part_shapes": "Get all body part shape notations.",
    "body_part_size": "Get all body part size notations.",
    "allotype_sizes": (
        "Get the allotype length, mean length, length range, and sample size."
        "This will also include allotype body part sizes (like head) and widths."
    ),
    "holotype_sizes": (
        "Get the allotype length, mean length, length range, and sample size."
    ),
    "sclerotization": "Find all body part sclerotization annotations.",
}


def dspy_extract_action(args: argparse.Namespace) -> None:
    with args.text_doc.open() as fh:
        text = fh.read()

    lm = dspy.LM(
        args.model_name,
        api_base=args.api_host,
        api_key=args.api_key,
        temperature=args.temperature,
        max_tokens=args.context_length,
        cache=args.cache,
    )
    dspy.configure(lm=lm)

    predictor = dspy.Predict(SetaeCounts)
    prediction = predictor(text=text)

    pp(prediction)


def extract_action(args: argparse.Namespace) -> None:
    with args.input_text.open() as fh:
        text = fh.read()

    with lms.Client(args.api_host) as client, args.output_md.open("w") as out:
        model = client.llm.model(
            args.model_name,
            config={
                "temperature": args.temperature,
                "contextLength": args.context_length,
            },
        )

        for key, prompt in PROMPTS.items():
            rprint(f"[blue]{key}")
            print(f"# {key}", file=out)
            msg = PREFIX + prompt + SUFFIX + text

            chat = lms.Chat()
            chat.add_user_message(msg)

            lm_text = ""
            try:
                lm_text = model.respond(chat)
            except lms.LMStudioServerError as err:
                lm_error = f"Server error: {err}"
                rprint(f"[red]{lm_error}")
                print(lm_error, file=out)
                continue

            rprint(f"[green]{lm_text}")
            print(lm_text, file=out)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Parse data from lice papers."""),
    )

    subparsers = arg_parser.add_subparsers(
        title="Subcommands", description="Actions for extracting lice traits"
    )

    # ------------------------------------------------------------
    extract_parser = subparsers.add_parser(
        "extract", help="""Extract DwC data from OCR records."""
    )
    extract_parser.add_argument(
        "--input-text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""The text document to parse.""",
    )
    extract_parser.add_argument(
        "--output-md",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the results to thei markdown file.""",
    )
    extract_parser.add_argument(
        "--model-name",
        default="lm_studio/google/gemma-3-27b",
        help="""Use this language model. (default: %(default)s)""",
    )
    extract_parser.add_argument(
        "--api-host",
        default="http://localhost:1234/v1",
        help="""URL for the language model. (default: %(default)s)""",
    )
    extract_parser.add_argument(
        "--api-key",
        help="""API key.""",
    )
    extract_parser.add_argument(
        "--context-length",
        type=int,
        default=65536,
        help="""Model's context length. (default: %(default)s)""",
    )
    extract_parser.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="""Model's temperature. (default: %(default)s)""",
    )
    extract_parser.add_argument(
        "--cache",
        action="store_true",
        help="""Use cached records?""",
    )
    extract_parser.set_defaults(func=extract_action)

    # ------------------------------------------------------------

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    ARGS = parse_args()
    ARGS.func(ARGS)
