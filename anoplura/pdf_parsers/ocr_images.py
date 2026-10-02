#!/usr/bin/env python3

import argparse
import base64
import concurrent.futures as conc
import logging
import mimetypes
import os
import textwrap
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException
from tqdm import tqdm

from anoplura.pdf_parsers.pylib import fix_ocr, image_util, log
from anoplura.pylib import prompt_util


def main(args: argparse.Namespace) -> None:
    log.started()
    image_paths = sorted(args.image_dir.glob("*.jpg"))

    job_started = datetime.now()

    sys_prompt, _ = prompt_util.read_lm_prompt(args.prompt)

    frags = {}

    with (
        tqdm(total=len(len(image_paths))) as progress_bar,
        conc.ThreadPoolExecutor(max_workers=args.workers) as executor,
    ):
        futures = {
            executor.submit(call_model, args, sys_prompt, image_path): i
            for i, image_path in enumerate(image_paths)
        }

        for future in conc.as_completed(futures):
            i = futures[future]
            frags[i] = future.result()
            progress_bar.update(1)

    with args.ocr_text.open("w") as f:
        text = "".join([v for _, v in sorted(frags.items())])
        f.write(text)

    logging.info.log(f"Job Time: {datetime.now() - job_started}")
    log.finished()


def call_model(args: argparse.Namespace, sys_prompt: str, image_path: Path) -> dict:
    try:
        base64_image, mime_type = image_util.load_image(image_path, args.timeout)

        url = f"{args.api_host}/chat/completions"

        headers = {"Content-Type": "application/json"}
        if api_key := os.getenv("LLM_API_KEY"):
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": args.model_name,
            "messages": [
                {"role": "system", "content": sys_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "url": f"data:{mime_type};base64,{base64_image}",
                        }
                    ],
                },
            ],
            "chat_template_kwargs": {"enable_thinking": False},
        }

        if args.temperature is not None:
            payload["temperature"] = args.temperature

        if args.max_tokens is not None:
            payload["max_tokens"] = args.max_tokens

        response = requests.post(
            url, headers=headers, json=payload, timeout=args.timeout
        )
        response.raise_for_status()
        result = response.json()

        content = result["choices"][0]["message"]["content"] or ""
        content = fix_ocr.clean_ocr(content, convert_html=args.convert_html)

        content = result["choices"][0]["message"]["content"] or ""

        text = fix_ocr.clean_ocr(content)

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


def load_image(source: Path | str) -> tuple[str, str]:
    """Return (base64_image, mime_type) for a local path."""
    with Path(source).open("rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")
    mime_type, _ = mimetypes.guess_type(source)
    if not mime_type or not mime_type.startswith("image/"):
        mime_type = "application/octet-stream"
    return base64_image, mime_type


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
        "--prompt",
        type=Path,
        default="prompts/ocr_v1.md",
        metavar="PATH",
        help="""A markdown file with a prompt used to OCR images.
            (default: %(default)s)""",
    )
    arg_parser.add_argument(
        "--model-id",
        default="unsloth/gemma-4-E4B-it-GGUF:Q8_K_XL",
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
        default=2,
        metavar="INT",
        help="""How many parallel threads to run. (default: %(default)s)
            Increase this if the model server is powerful enough.""",
    )
    arg_parser.add_argument(
        "--temperature",
        type=float,
        metavar="FLOAT",
        help="""Model's temperature.""",
    )
    arg_parser.add_argument(
        "--max-tokens",
        type=int,
        default=2048,
        metavar="INT",
        help="""The OCR model's response maximum tokens. (default: %(default)s)""",
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
