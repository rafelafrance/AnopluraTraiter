#!/usr/bin/env python3

import argparse
import base64
import concurrent.futures as conc
import logging
import os
import re
import textwrap
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException
from tqdm import tqdm

from anoplura.pylib import log


def main(args: argparse.Namespace) -> None:
    log.started(args=args)
    image_paths = sorted(args.image_dir.glob("*.jpg"))

    job_started = datetime.now()

    with args.prompt_md.open() as md:
        prompt = md.read()
    prompt = re.sub("^---$.*?^---$", "", prompt, flags=re.MULTILINE | re.DOTALL).strip()

    frags = {}

    with (
        tqdm(total=len(image_paths)) as progress_bar,
        conc.ThreadPoolExecutor(max_workers=args.threads) as executor,
    ):
        futures = {
            executor.submit(call_model, args, image_path, prompt): i
            for i, image_path in enumerate(image_paths)
        }

        for future in conc.as_completed(futures):
            i = futures[future]
            frags[i] = future.result()
            progress_bar.update(1)

    with args.ocr_file.open("w") as f:
        text = "".join([v for _, v in sorted(frags.items())])
        f.write(text)

    logging.info(f"Job Time: {datetime.now() - job_started}")
    log.finished()


def call_model(args: argparse.Namespace, image_path: Path, prompt: str) -> str:
    with image_path.open("rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")

    headers = {"Content-Type": "application/json"}
    if api_key := os.getenv("LLM_API_KEY"):
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": args.model_id,
        "messages": [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            },
        ],
    }

    try:
        response = requests.post(
            f"{args.api_host}/chat/completions",
            headers=headers,
            json=payload,
            timeout=args.timeout,
        )
        response.raise_for_status()
        result = response.json()

        text = result["choices"][0]["message"]["content"] or ""
        text = text.strip()

    except (
        IndexError,
        KeyError,
        OSError,
        RequestException,
        TypeError,
        ValueError,
    ) as err:
        logging.error(f"Error: {image_path.stem} {str(err)[:120]}")
        return ""

    return text


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""OCR images."""),
    )
    arg_parser.add_argument(
        "--image-dir",
        type=Path,
        required=True,
        metavar="PATH",
        help="""OCR all images in this directory.""",
    )
    arg_parser.add_argument(
        "--ocr-file",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Put OCRed text into this CSV file. This appends data to the file.""",
    )
    arg_parser.add_argument(
        "--prompt-md",
        type=Path,
        default="prompts/ocr_v1.md",
        metavar="PATH",
        help="""A markdown file with a prompt used to OCR images.
            (default: %(default)s)""",
    )
    arg_parser.add_argument(
        "--model-id",
        default="Qwen3.6-35B-A3B-MTP-GGUF",
        metavar="STRING",
        help="""Use this language model. (default: %(default)s)""",
    )
    arg_parser.add_argument(
        "--api-host",
        default="http://localhost:9931/v1",
        metavar="STRING",
        help="""URL for the language model. (default: %(default)s)""",
    )
    arg_parser.add_argument(
        "--threads",
        type=int,
        default=4,
        metavar="INT",
        help="""How many parallel threads to run. (default: %(default)s)
            Increase this if the model server is powerful enough.""",
    )
    arg_parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        metavar="INT",
        help="""How long to wait for the OCR model to complete in seconds.
            (default: %(default)s).""",
    )
    arg_parser.add_argument(
        "--convert-html",
        action="store_true",
        help="""Convert HTML to text. Some models return HTML only.""",
    )
    ns: argparse.Namespace = arg_parser.parse_args(args)
    if ns.image_dir and not ns.image_dir.is_dir():
        arg_parser.error(f"--image-dir is not a directory: {ns.image_dir}")
    return ns


if __name__ == "__main__":
    load_dotenv()
    ARGS = parse_args()
    main(ARGS)
