#!/usr/bin/env python3

"""
Extract anatomical traits from louse descriptions using an LLM API.

Iterates over a set of prompts covering different trait types, sends each
prompt together with a text file to the language model, and writes the
structured JSON results to an output file.
"""

import argparse
import concurrent.futures as conc
import json
import logging
import textwrap
from datetime import datetime
from pathlib import Path

import requests

from anoplura.pylib import prompt_util, str_util, timer

JSON_ERRORS = (json.JSONDecodeError, UnicodeDecodeError)


def run_lm(args: argparse.Namespace) -> None:
    """Run LLM extraction for all text files in the input directory."""
    job_began = timer.job_began(args.log_file, args=args)

    text_paths = sorted(args.text_dir.glob("*.txt"))

    sys_prompt, field_names = prompt_util.read_lm_prompt(args.prompt)
    field_prompts = prompt_util.get_field_prompts(field_names)

    results: list[dict] = []

    with conc.ThreadPoolExecutor(max_workers=args.workers) as executor:
        for text_path in text_paths:
            file_began = datetime.now()

            logging.info("-" * 80)
            logging.info("**** %s ****", text_path.stem)

            with text_path.open() as fh:
                text = fh.read()

            futures = {
                executor.submit(
                    one_prompt, args, sys_prompt, field_prompt, field_name, text
                )
                for field_name, field_prompt in field_prompts.items()
            }

            for future in conc.as_completed(futures):
                results += future.result()

            timer.elapsed(file_began, text_path.stem)

    with args.lm_jsonl.open("a") as llm_out:
        for row in results:
            print(json.dumps(row), file=llm_out, flush=True)

    logging.info("-" * 80)
    timer.job_elapsed(job_began)


def one_prompt(
    args: argparse.Namespace,
    sys_prompt: str,
    field_prompt: str,
    field_name: str,
    text: str,
) -> list[dict]:
    """Extract a single trait from a file."""
    began = datetime.now()

    record_name = field_name.removesuffix("s")

    url = f"{args.api_host}/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": args.model_name,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": field_prompt},
            {"role": "user", "content": text},
        ],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }

    try:
        response = requests.post(
            url, headers=headers, json=payload, timeout=args.timeout
        )
        response.raise_for_status()
        result = response.json()

        content = result["choices"][0]["message"]["content"]
        content = str_util.clean_ocr(content)

    except Exception as e:
        logging.exception("API error")
        row = {"record": record_name, "ERROR": str(e)}
        return [row]

    try:
        rows = json.loads(content)
    except JSON_ERRORS as e:
        logging.exception("JSON Error")
        row = {"record": record_name, "ERROR": str(e)}
        return [row]

    result = []
    for row in rows:
        result = {"record": record_name} | row

    timer.elapsed(began, record_name)
    return result


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the extraction script."""
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Parse data from louse descriptions."""),
    )
    arg_parser.add_argument(
        "--prompt",
        type=Path,
        required=True,
        help="""A markdown file with a prompt and list of fields to parse.""",
    )
    arg_parser.add_argument(
        "--text-dir",
        type=Path,
        required=True,
        metavar="PATH",
        help="""The directory containing the text files to parse.""",
    )
    arg_parser.add_argument(
        "--lm-jsonl",
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
        "--max-tokens",
        type=int,
        help="""The LM response's maximum tokens.""",
    )
    arg_parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="""How many seconds to wait for a server response.
            (default: %(default)s)""",
    )
    arg_parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="""How many parallel threads to run. (default: %(default)s)""",
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
