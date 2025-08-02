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
    replace: str
    rank: str


def main(args):
    with args.in_csv.open() as inf:
        reader = csv.DictReader(inf)
        rows = list(reader)

    taxa = {}

    # The rows look like any of the below:
    # header row: label,pattern,replace,rank
    # Whis a replacment name: anoplura,scipio longiceps,Scipio aulacodi,species
    # Without a replacment name: anoplura,scipio tripedatus,,species
    for row in rows:
        pattern = row["pattern"].lower()
        replace = row["replace"] if row["replace"] else row["pattern"]
        words = pattern.split()
        abbrev = " ".join([f"{words[0][0]}.", *words[1:]])

        # Regular species name, Canis lupus
        taxa[pattern] = Taxon(
            label=row["label"],
            pattern=pattern,
            replace=replace,
            rank="species",
        )

        # Species with the genus abbreviated, like C. lupus
        if len(words) > 1:
            taxa[abbrev] = Taxon(
                label=row["label"],
                pattern=abbrev,
                replace=replace,
                rank="species",
            )

        # Genus only, like Canis
        taxa[words[0]] = Taxon(
            label=row["label"],
            pattern=words[0],
            replace=words[0].title(),
            rank="genus",
        )

        # We have to do the same for a replaced species name
        if not row["replace"]:
            continue

        # From replace
        pattern = row["replace"].lower()
        words = pattern.split()
        abbrev = " ".join([f"{words[0][0]}.", *words[1:]])

        # Regular species name from the replace column, Canis lupus
        taxa[pattern] = Taxon(
            label=row["label"],
            pattern=pattern,
            replace=row["replace"],
            rank="species",
        )

        # Species with the genus abbreviated from the replace column, like C. lupus
        if len(words) > 1:
            taxa[abbrev] = Taxon(
                label=row["label"],
                pattern=abbrev,
                replace=row["replace"],
                rank="species",
            )

        # Genus only, like Canis
        taxa[words[0]] = Taxon(
            label=row["label"],
            pattern=words[0],
            replace=words[0].title(),
            rank="genus",
        )

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
