from collections import defaultdict
from pathlib import Path

from spacy.tokens import Doc

from anoplura.rules.base import Base

# from pprint import pp

ORDER = {
    "taxon": 0,
    "date": 100,
    "elevation": 200,
    "lat_long": 300,
    "specimen_type": 400,
    "sex": 500,
    "part": 600,
    "gonopod": 700,
    "plate": 800,
    "segment": 900,
    "sternite": 1000,
    "tergite": 1100,
    "subpart": 1200,
    "seta": 1300,
}


def write(doc: Doc, md_file: Path) -> None:
    traits: list[Base] = [e._.trait for e in doc.ents]

    lines = format_traits(traits, doc.text)

    with md_file.open("w") as fout:
        for ln in lines:
            fout.write(ln + "\n\n")

    # unlinked_traits = [e._.trait for e in doc._.unlinked]


def format_traits(traits: list[Base], text: str) -> list[str]:
    # Index the traits by their position in the document
    trait_pos = {t.start: t for t in traits}

    # Find the children of each trait
    child_traits = set()
    for trait in trait_pos.values():
        if trait.links:
            for link in trait.links:
                child_traits.add(link.start)

    # Parent traits are those that are not in child traits
    parent_pos = {k for k in trait_pos if k} - child_traits

    # Sort parent traits by their type
    trait_type = defaultdict(list)
    for start in parent_pos:
        parent = trait_pos[start]
        key = parent.for_output().key
        trait_type[(ORDER[parent._trait], key)].append(parent)
    trait_type = dict(sorted(trait_type.items()))

    # Format each trait and its children
    lines = []
    for parents in trait_type.values():
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


def get_text_pos(
    parent: Base, trait_pos: dict[int, Base], start: int, end: int
) -> tuple[int, int]:
    start = min(start, parent.start)
    end = max(end, parent.end)
    for link in parent.links:
        child = trait_pos[link.start]
        start, end = get_text_pos(child, trait_pos, start, end)
    return start, end


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
