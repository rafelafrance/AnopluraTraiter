from collections import defaultdict
from pathlib import Path

from spacy.tokens import Doc

from anoplura.rules.base import Base


def writer(doc: Doc, _text_file: Path) -> None:
    traits = [e._.trait for e in doc.ents]

    print("#" * 80)
    format_text(doc.text, traits)

    print("\n")
    print("#" * 80)
    unlinked_traits = [e._.trait for e in doc._.unlinked]
    format_text(doc.text, unlinked_traits)


def format_text(_text: str, traits: list[Base]) -> str:
    # Build index
    indexed = {t.start: t for t in traits}
    indexed = dict(sorted(indexed.items()))

    # Get root traits
    linked = set()
    for trait in indexed.values():
        if trait.links:
            for link in trait.links:
                linked.add(link.start)
    roots = set(indexed.keys()) - linked
    roots = sorted(roots)

    # Group root traits
    grouped = defaultdict(list)
    for start in roots:
        root = indexed[start]
        grouped[root.format()].append(start)
    grouped = dict(sorted(grouped.items()))

    for starts in grouped.values():
        print("=" * 80)
        for start in starts:
            parent = indexed[start]
            show_children(indexed, parent, 0)
            print()

    return ""


def show_children(indexed: dict[int, Base], parent: Base, depth: int = 0) -> None:
    spaces = "    " * depth
    print(f"{spaces} {parent.format()}")
    if parent.links:
        for link in parent.links:
            child = indexed[link.start]
            show_children(indexed, child, depth + 1)
