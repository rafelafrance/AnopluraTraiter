from datetime import datetime
from pathlib import Path

from spacy.tokens import Doc

from anoplura.rules.base import Base
from anoplura.writers.writer_util import (
    expand_text_pos,
    get_text_pos,
    orgainize_traits,
    split_traits,
)

# from pprint import pp


def write(doc: Doc, md_file: Path) -> None:
    traits: list[Base] = [e._.trait for e in doc.ents]
    traits = split_traits(traits)

    lines = format_traits(traits, doc.text, md_file)

    with md_file.open("w") as fout:
        for ln in lines:
            fout.write(ln + "\n\n")

    # unlinked_traits = [e._.trait for e in doc._.unlinked]


def format_traits(traits: list[Base], text: str, md_file: Path) -> list[str]:
    # Index traits by position and group traits by type
    traits_by_pos, parents_by_type = orgainize_traits(traits)

    lines = []
    # Add a document header
    now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
    lines.append(f"# {md_file.stem}   {now}")

    formatted_text = format_text(traits_by_pos, parents_by_type, text)
    lines.append(formatted_text)

    # Format each trait and its children
    for parents in parents_by_type.values():
        lines.append("---")
        header = parents[0].for_output().key

        lines.append(f"## {header}")

        # Format the raw text for each parent trait
        for parent in parents:
            start, end = get_text_pos(parent, traits_by_pos, parent.start, parent.end)
            before, after = expand_text_pos(text, start, end)
            lines.append(
                f"**Raw Text:** {text[before:start]} "
                f"**{text[start:end]}** {text[end:after]}"
            )

        # Sort parents so they are easier to group
        parents = sorted(parents, key=lambda p: p.for_output().value)

        # Format the trait nodes
        prev_value = ""
        for parent in parents:
            value = parent.for_output().value
            format_nodes(lines, traits_by_pos, parent, 0, hide=(value == prev_value))
            prev_value = value

    return lines


def format_text(
    traits_by_pos: dict[int, list[Base]],
    parents_by_type: dict[str, list[Base]],
    text: str,
) -> str:
    frags = []
    slices = {}

    for parents in parents_by_type.values():
        for parent in parents:
            start, end = get_text_pos(parent, traits_by_pos, parent.start, parent.end)
            slices[end] = start

    slices = dict(sorted(slices.items()))
    prev = 0

    for end, start in slices.items():
        if prev < start:
            frags.append(text[prev:start])
        frags.append(text[start:end])
        prev = end

    if len(text) > prev:
        frags.append(text[prev:])

    return "".join(frags)


def format_nodes(
    lines: list[str],
    traits_by_pos: dict[int, list[Base]],
    parent: Base,
    depth: int = 0,
    *,
    hide: bool = False,
) -> None:
    if not hide:
        indent = "    " * depth
        lines.append(f"{indent}- {parent.for_output().value}")
    if parent.links:
        for link in parent.links:
            children = traits_by_pos[link.start]
            for child in children:
                format_nodes(lines, traits_by_pos, child, depth + 1)
