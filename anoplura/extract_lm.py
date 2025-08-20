#!/usr/bin/env python3

import argparse
import textwrap
from pathlib import Path
from pprint import pp

import dspy
from traiter.pylib.util import clean_text


class ExtractTraits(dspy.Signature):
    """Extract traits from species descriptions."""

    targets: str = dspy.InputField(descr="list of traits to extract")
    description: str = dspy.InputField(descr="may contain trait information")
    traits: list[dict[str, str]] = dspy.OutputField(descr="list of extracted traits")


def main(args: argparse.Namespace) -> None:
    lm = dspy.LM(args.model, api_base=args.api_base, api_key=args.api_key)

    dspy.configure(lm=lm)

    module = dspy.Predict(ExtractTraits)

    with args.text.open() as in_file:
        text = " ".join(in_file.readlines())
        text = clean_text(text)

    question = """find all louse traits in the text"""

    reply = module(targets=question, description=text)

    pp(reply.traits)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Parse data from lice papers."""),
    )

    arg_parser.add_argument(
        "--text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Path to the text file to parse.""",
    )

    arg_parser.add_argument(
        "--html-file",
        type=Path,
        metavar="PATH",
        help="""Output the results to this HTML file.""",
    )

    arg_parser.add_argument(
        "--model",
        default="ollama_chat/deepseek-r1:14b",
        help="""Use this LLM model.""",
    )

    arg_parser.add_argument(
        "--api-base",
        default="http://localhost:11434",
        help="""URL for the LM model.""",
    )

    arg_parser.add_argument(
        "--api-key",
        default="",
        help="""Key for the LM model.""",
    )

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
