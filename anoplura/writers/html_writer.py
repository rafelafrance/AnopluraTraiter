from datetime import datetime
from itertools import cycle
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from mohtml import div, span
from spacy.tokens import Doc

from anoplura.rules.base import Base
from anoplura.writers.writer_util import get_text_pos, orgainize_traits

# from pprint import pp

CSS_CLASSES_COUNT = 30  # Look in the html_writer.css file
CSS_CLASSES = cycle([f"cc{i}" for i in range(CSS_CLASSES_COUNT)])


def writer(doc: Doc, html_file: Path) -> None:
    env = Environment(
        loader=FileSystemLoader("./anoplura/writers/templates"), autoescape=True
    )

    traits: list[Base] = [e._.trait for e in doc.ents]

    text = format_traits(traits, doc.text)

    # unlinked_traits = [e._.trait for e in doc._.unlinked]

    template = env.get_template("html_writer.html").render(
        now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
        text=text,
        file_name=html_file.stem,
    )

    with html_file.open("w") as out_file:
        out_file.write(template)


def format_traits(traits: list[Base], text: str) -> str:
    # Index traits by position and group traits by type
    trait_pos, trait_type = orgainize_traits(traits)

    # Format each trait and its children
    frags = []
    for parents in trait_type.values():
        header = parents[0].for_output().key
        frags.append(div(header, klass="trait_type"))

        for parent in parents:
            format_raw_text(frags, parent, trait_pos, text)

        # Sort parents so they are easier to group
        parents = sorted(parents, key=lambda p: p.for_output().value)

        # Format the trait nodes
        prev_value = ""
        for parent in parents:
            value = parent.for_output().value
            format_nodes(frags, trait_pos, parent, 0, hide=(value == prev_value))
            prev_value = value

    return "".join(str(f) for f in frags)


def format_raw_text(
    frags: list[str], parent: Base, trait_pos: dict[int, Base], text: str
) -> None:
    start, end = get_text_pos(parent, trait_pos, parent.start, parent.end)
    frags.append(
        div(
            span("Raw Text", klass="raw_label"),
            span(text[start:end], klass="raw_text"),
            klass="text",
        )
    )


def format_nodes(
    frags: list[str],
    indexed: dict[int, Base],
    parent: Base,
    depth: int = 0,
    *,
    hide: bool = False,
) -> None:
    if not hide:
        html = parent.for_output()
        frags.append(div(span(html.value, klass="value"), klass=f"level-{depth}"))
    if parent.links:
        for link in parent.links:
            child = indexed[link.start]
            format_nodes(frags, indexed, child, depth + 1)
