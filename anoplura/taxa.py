#!/usr/bin/env python3

import argparse
import csv
import textwrap
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Taxon:
    label: str
    pattern: str
    rank: str
    raw: str
    replace: str = ""


def main(args):
    with args.in_csv.open() as inf:
        reader = csv.DictReader(inf)
        rows = list(reader)

    taxa = {}

    for row in rows:
        # From pattern
        label = row["label"]
        pattern = row["pattern"].lower()
        raw = row["pattern"]
        replace = row.get("replace", row["pattern"])

        words = pattern.split()
        abbrev = " ".join([f"{words[0][0]}."] + words[1:])

        taxa[pattern] = Taxon(
            label=label, pattern=pattern, rank="species", raw=raw, replace=replace
        )
        taxa[abbrev] = Taxon(
            label=label, pattern=abbrev, rank="species", raw=raw, replace=replace
        )
        taxa[words[0]] = Taxon(label=label, pattern=words[0], raw=raw, rank="genus")

        if pattern == replace:
            continue

        # From replace
        pattern = row["replace"].lower()
        raw = row["replace"]
        words = pattern.split()
        abbrev = " ".join([f"{words[0][0]}."] + words[1:])

        taxa[pattern] = Taxon(
            label=label, pattern=pattern, rank="species", raw=raw, replace=replace
        )
        taxa[abbrev] = Taxon(
            label=label, pattern=abbrev, rank="species", raw=raw, replace=replace
        )
        taxa[words[0]] = Taxon(label=label, pattern=words[0], raw=raw, rank="genus")

    taxa = sorted(taxa.values(), key=lambda t: (t.rank, t.pattern))

    with args.out_csv.open("w") as out:
        writer = csv.writer(out)
        writer.writerow(["label", "pattern", "replace", "rank"])
        for taxon in taxa:
            writer.writerow([taxon.label, taxon.pattern, taxon.replace, taxon.rank])


def parse_args():
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Create taxon terms from a species dump."""),
    )

    arg_parser.add_argument(
        "--in-csv",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Input CSV file containing taxon terms.""",
    )

    arg_parser.add_argument(
        "--out-csv",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the processed taxa to this CSV file.""",
    )

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
