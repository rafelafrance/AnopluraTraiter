#!/usr/bin/env python3
"""Convert a PDF to HTML and then to text."""
import argparse
import subprocess
import sys
import textwrap
from collections import defaultdict
from math import floor
from tempfile import NamedTemporaryFile

import regex
import toml
import traiter.util as t_util
from bs4 import BeautifulSoup

from anoplura.pylib.const import DASH
from anoplura.pylib.pipeline import pipeline


def main(args):
    """Convert the PDF to a text format we can use.

    The standard utilities for for converting PDFs don't really do what
    we need.
    """
    with t_util.get_temp_dir(where=args.temp_dir, keep=args.keep_temp_dir) as temp_dir:
        page_file = NamedTemporaryFile(
            suffix=".html", mode="r", dir=temp_dir, delete=(not args.keep_temp_dir)
        )
        to_html(args, page_file)
        page = clean_html(page_file)
        page_file.close()

    lines = order_lines(args, page)
    lines = [str(ln[4]) for ln in lines]

    lines = remove_before(args, lines)
    lines = remove_after(args, lines)
    lines = remove_lines(args, lines)
    text = join_lines(lines)
    lines = split_sentences(text)

    for ln in lines:
        args.text_file.write(ln)
        args.text_file.write("\n")


def split_sentences(text):
    """Split the text into sentences."""
    nlp = pipeline()
    doc = nlp(text)
    lines = [x for s in doc.sents if (x := " ".join(s.text.split()))]
    return lines


def join_lines(lines):
    """Join lines into a text blob."""
    dash = "|".join(DASH)
    text = "\n".join(lines)
    text = regex.sub(rf"(\w)(?:{dash})\n(\w)", r"\1\2", text)
    return text


def remove_lines(args, lines):
    """Filter lines like header, footers, and figures."""
    if args.remove_lines:
        return [ln for ln in lines if not args.remove_lines.search(ln)]
    return lines


def remove_before(args, lines):
    """Remove lines before the match."""
    if not args.remove_before:
        return lines

    new_lines = []
    found = False
    for ln in lines:
        if args.remove_before.search(ln):
            found = True

        if found:
            new_lines.append(ln)

    return new_lines


def remove_after(args, lines):
    """Remove lines before the match."""
    if not args.remove_after:
        return lines

    new_lines = []
    for ln in lines:
        new_lines.append(ln)
        if args.remove_after.search(ln):
            return new_lines

    return new_lines


def order_lines(args, page):
    """Convert html page into text paragraphs."""
    lines = []
    page = BeautifulSoup(page, features="lxml")
    for i, div in enumerate(page.find_all("div")):
        width = int(regex.search(r"width:(\d+)", div["style"])[1])
        half = width // 2
        for para in div.find_all("p"):
            top = int(regex.search(r"top:(\d+)", para["style"])[1])
            left = int(regex.search(r"left:(\d+)", para["style"])[1])
            column = floor(left // half)
            text = t_util.clean_text(para.get_text(), trans=args.mojibake)
            lines.append((i, column, top, left, text))
    return lines


def to_html(args, page_file):
    """Convert the PDF to html."""
    cmd = ["pdftohtml -s -i -q -noframes", args.pdf, page_file.name]
    cmd = " ".join(cmd)
    subprocess.run(cmd, shell=True, check=True)


def clean_html(page_file):
    """Clean HTML noise."""
    page = page_file.read()
    page = page.replace("&#160;", " ")  # Replace non-breaking spaces
    page = page.replace("-<br/>", "")  # Join words split with a - & line break
    page = page.replace("<br/>", " ")  # Remove hard line breaks
    return page


def toml_args(args):
    """Get arguments from a TOML file."""
    config = toml.load(args.toml_file)

    new_args = defaultdict(list)
    for key, values in config[args.toml_section].items():
        values = t_util.as_list(values)

        for value in values:
            if isinstance(value, str) and value.startswith("@"):
                sect, field = value.split(".")
                value = config[sect[1:]][field]

            new_args[key].append(value)

    for attr in [a for a in dir(args) if not a.startswith("__")]:
        if arg_value := getattr(args, attr):
            new_value = new_args.get(attr)
            if new_value and isinstance(new_value, list):
                new_args[attr].append(arg_value)
            else:
                new_args[attr] = arg_value

    if new_args["mojibake"]:
        mojibake = t_util.flatten(new_args["mojibake"])
        mojibake = {k: v for k, v in zip(mojibake[:-1:2], mojibake[1::2])}
        new_args["mojibake"] = mojibake

    new_args = t_util.DotDict(new_args)
    return new_args


def parse_args():
    """Process command-line arguments."""
    description = """Parse data from lice papers."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument("--pdf", "-p", help="""Path to the PDF paper to parse.""")

    arg_parser.add_argument(
        "--text-file",
        "-T",
        type=argparse.FileType("w"),
        help="""Output the results to this text file.""",
    )

    arg_parser.add_argument(
        "--toml-file",
        "--toml",
        "--config",
        "-c",
        help="""Read configuration parameter from this TOML file.""",
    )

    arg_parser.add_argument(
        "--toml-section",
        "--section",
        "-s",
        help="""Use configurations from this TOML section/table.""",
    )

    arg_parser.add_argument(
        "--mojibake",
        "-m",
        action="append",
        nargs=2,
        help="""Translation table to use for converting odd mojibake.""",
    )

    arg_parser.add_argument(
        "-r",
        "--remove-lines",
        action="append",
        help=r"""Remove lines that have this pattern. You may need to quote
            this argument. You may use this argument more than once. Removing
            lines happens after --remove-before and --remove-after.
            Examples: --remove '^Journal of' --remove '^\d+$'.""",
    )

    arg_parser.add_argument(
        "-b",
        "--remove-before",
        action="append",
        help="""Remove lines before this pattern. You may need to quote
            this argument. You may use this argument more than once. Use this
            to remove abstracts and other leading material.""",
    )

    arg_parser.add_argument(
        "-a",
        "--remove-after",
        action="append",
        help="""Remove lines after this pattern. You may need to quote
            this argument. You may use this argument more than once. Use this
            to remove acknowledgements and citations""",
    )

    arg_parser.add_argument(
        "-t",
        "--temp-dir",
        metavar="DIR",
        help="""Place temporary files in this directory. All files will be
            deleted after aTRAM completes. The directory must exist.""",
    )

    arg_parser.add_argument(
        "--keep-temp-dir",
        action="store_true",
        help="""This flag will keep the temporary files in the --temp-dir
            around for debugging.""",
    )

    args = arg_parser.parse_args()

    if not t_util.xor(args.toml_file, args.toml_section):
        sys.exit("You must provide both a --toml-file and a --toml-section.")

    args = toml_args(args)

    if args.mojibake:
        args.mojibake = str.maketrans(args.mojibake)

    for attr in ("remove_lines", "remove_before", "remove_after"):
        if value := args.get(attr):
            reg = regex.compile("|".join([f"(?:{v})" for v in value]))
            args[attr] = reg

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
