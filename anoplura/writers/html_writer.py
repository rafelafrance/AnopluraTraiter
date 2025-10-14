from collections import defaultdict
from datetime import datetime
from html import escape
from itertools import cycle
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from spacy.tokens import Doc

from anoplura.rules.base import Base

CSS_CLASSES_COUNT = 30  # Look in the html_writer.css file
CSS_CLASSES = cycle([f"cc{i}" for i in range(CSS_CLASSES_COUNT)])


def writer(doc: Doc, html_file: Path) -> None:
    env = Environment(
        loader=FileSystemLoader("./anoplura/writers/templates"), autoescape=True
    )

    traits: list[Base] = [e._.trait for e in doc.ents]

    text = format_trait_tree(traits, doc.text)

    # unlinked_traits = [e._.trait for e in doc._.unlinked]

    # print("\n")
    # print("=" * 80)
    # format_trait_tree(unlinked_traits, doc.text)

    template = env.get_template("html_writer.html").render(
        now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
        text=text,
        file_name=html_file.stem,
    )

    with html_file.open("w") as out_file:
        out_file.write(template)


def format_trait_tree(traits: list[Base], text: str) -> str:
    indexed_by_start_index = {t.start: t for t in traits}
    indexed_by_start_index = dict(sorted(indexed_by_start_index.items()))

    indexed_by_trait_name: dict[str, list[Base]] = defaultdict(list)
    _ = {indexed_by_trait_name[t._trait].append(t) for t in traits}

    frags = []
    for trait_name in ("taxon", "date", "lat_long", "elevation", "specimen_type"):
        traits = indexed_by_trait_name.get(trait_name, [])
        if traits:
            for trait in traits:
                format_parent_data(frags, trait, indexed_by_start_index, text)
                format_nodes(frags, indexed_by_start_index, trait, 0)
                del indexed_by_start_index[trait.start]

    # Get child traits
    child_traits = set()
    for trait in indexed_by_start_index.values():
        if trait.links:
            for link in trait.links:
                child_traits.add(link.start)

    # Parent traits are those that are not in child traits
    parent_indexes = {k for k in indexed_by_start_index if k} - child_traits

    for start in parent_indexes:
        parent = indexed_by_start_index[start]
        format_parent_data(frags, parent, indexed_by_start_index, text)
        format_nodes(frags, indexed_by_start_index, parent, 0)

    return "".join(frags)


def format_parent_data(
    frags: list[str], parent: Base, indexed_by_start_index: dict[int, Base], text: str
) -> None:
    start, end = get_text_indexes(
        parent, indexed_by_start_index, parent.start, parent.end
    )
    frags += [
        "<div class='trait_type'>",
        escape(" ".join(parent._trait.split("_")).title()),
        "</div>",
        "<div class='text'>",
        "<span class='raw_label'>Raw Text</span>",
        f"<span class='raw_text'>{escape(text[start:end])}</span>",
        "</div>",
    ]


def get_text_indexes(
    parent: Base, indexed_by_start_index: dict[int, Base], start: int, end: int
) -> tuple[int, int]:
    start = min(start, parent.start)
    end = max(end, parent.end)
    for link in parent.links:
        child = indexed_by_start_index[link.start]
        start, end = get_text_indexes(child, indexed_by_start_index, start, end)
    return start, end


def format_nodes(
    frags: list[str], indexed: dict[int, Base], parent: Base, depth: int = 0
) -> None:
    sex = escape(parent.sex.title()) if parent.sex and depth == 0 else ""
    html = parent.for_html()
    frags += [
        f"<div class='level-{depth}'>",
        f"<span class='sex'>{sex}</span>" if sex else "",
        f"<span class='key'>{escape(html.key)}</span>",
        f"<span class='value'>{escape(html.value)}</span>",
        "</div>",
    ]
    if parent.links:
        for link in parent.links:
            child = indexed[link.start]
            format_nodes(frags, indexed, child, depth + 1)
