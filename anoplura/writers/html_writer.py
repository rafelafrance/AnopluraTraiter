from collections import defaultdict
from datetime import datetime
from itertools import cycle
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from mohtml import div, span
from spacy.tokens import Doc

from anoplura.rules.base import Base

# from pprint import pp

CSS_CLASSES_COUNT = 30  # Look in the html_writer.css file
CSS_CLASSES = cycle([f"cc{i}" for i in range(CSS_CLASSES_COUNT)])

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
    frags = []
    for parents in trait_type.values():
        frags.append(
            div(" ".join(parents[0]._trait.split("_")).title(), klass="trait_type")
        )
        for parent in parents:
            format_raw_text(frags, parent, trait_pos, text)
        for parent in parents:
            format_nodes(frags, trait_pos, parent, 0)

    return "".join(str(f) for f in frags)


def format_raw_text(
    frags: list[str], parent: Base, trait_pos: dict[int, Base], text: str
) -> None:
    start, end = get_text_indexes(parent, trait_pos, parent.start, parent.end)
    frags.append(
        div(
            span("Raw Text", klass="raw_label"),
            span(text[start:end], klass="raw_text"),
            klass="text",
        )
    )


def get_text_indexes(
    parent: Base, trait_pos: dict[int, Base], start: int, end: int
) -> tuple[int, int]:
    start = min(start, parent.start)
    end = max(end, parent.end)
    for link in parent.links:
        child = trait_pos[link.start]
        start, end = get_text_indexes(child, trait_pos, start, end)
    return start, end


def format_nodes(
    frags: list[str], indexed: dict[int, Base], parent: Base, depth: int = 0
) -> None:
    sex = parent.sex.title() if parent.sex and depth == 0 else ""
    html = parent.for_output()
    frags.append(
        div(
            span(sex, klass="sex"),
            span(html.key, klass="key"),
            span(html.value, klass="value"),
            klass=f"level-{depth}",
        )
    )
    if parent.links:
        for link in parent.links:
            child = indexed[link.start]
            format_nodes(frags, indexed, child, depth + 1)
