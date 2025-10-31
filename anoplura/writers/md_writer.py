from datetime import datetime
from pathlib import Path

from spacy.tokens import Doc

from anoplura.rules.base import Base
from anoplura.writers.writer_util import get_text_pos, orgainize_traits

# from pprint import pp


def write(doc: Doc, md_file: Path) -> None:
    traits: list[Base] = [e._.trait for e in doc.ents]

    lines = format_traits(traits, doc.text, md_file)

    with md_file.open("w") as fout:
        for ln in lines:
            fout.write(ln + "\n\n")

    # unlinked_traits = [e._.trait for e in doc._.unlinked]


def format_traits(traits: list[Base], text: str, md_file: Path) -> list[str]:
    # Index traits by position and group traits by type
    trait_pos, parent_type = orgainize_traits(traits)

    lines = []
    # Add a document header
    now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
    lines.append(f"# {md_file.stem}   {now}")

    # Format each trait and its children
    for parents in parent_type.values():
        lines.append("---")
        header = parents[0].for_output().key

        lines.append(f"## {header}")

        # Format the raw text for each parent trait
        for parent in parents:
            start, end = get_text_pos(parent, trait_pos, parent.start, parent.end)
            lines.append(f"**Raw Text**  _{text[start:end]}_")

        # Sort parents so they are easier to group
        parents = sorted(parents, key=lambda p: p.for_output().value)

        # Format the trait nodes
        prev_value = ""
        for parent in parents:
            value = parent.for_output().value
            format_nodes(lines, trait_pos, parent, 0, hide=(value == prev_value))
            prev_value = value

    return lines


def format_nodes(
    lines: list[str],
    trait_pos: dict[int, Base],
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
            child = trait_pos[link.start]
            format_nodes(lines, trait_pos, child, depth + 1)
