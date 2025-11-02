from datetime import datetime
from html import escape
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

    # index traits by position and group traits by type
    traits_by_pos, parents_by_type = orgainize_traits(traits)

    formatted_traits = format_traits(traits_by_pos, parents_by_type, doc.text)
    formatted_text = format_text(traits_by_pos, parents_by_type, doc.text)

    # unlinked_traits = [e._.trait for e in doc._.unlinked]

    template = env.get_template("html_writer.html").render(
        now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
        formatted_traits=formatted_traits,
        formatted_text=formatted_text,
        file_name=html_file.stem,
    )

    with html_file.open("w") as out_file:
        out_file.write(template)


def format_text(
    traits_by_pos: dict[int, list[Base]],
    parents_by_type: dict[str, list[Base]],
    text: str,
) -> str:
    frags = []
    slices = []

    for key, parents in parents_by_type.items():
        class_ = next(CSS_CLASSES)
        for parent in parents:
            start, end = get_text_pos(parent, traits_by_pos, parent.start, parent.end)
            slices.append((start, end, class_, key[1]))

    slices = sorted(slices)
    prev = 0

    for start, end, class_, type_ in slices:
        if prev < start:
            frags.append(escape(text[prev:start]))
        frags.append(f'<span class="{class_}" title="{type_}">')
        frags.append(escape(text[start:end]))
        frags.append("</span>")
        prev = end

    if len(text) > prev:
        frags.append(text[prev:])

    return "".join(frags)


def format_traits(
    traits_by_pos: dict[int, list[Base]],
    parents_by_type: dict[str, list[Base]],
    text: str,
) -> str:
    # Format each trait and its children
    frags = []
    for parents in parents_by_type.values():
        header = parents[0].for_output().key
        frags.append(div(header, klass="trait_type"))

        for parent in parents:
            format_raw_text(frags, parent, traits_by_pos, text)

        # Sort parents so they are easier to group
        parents = sorted(parents, key=lambda p: p.for_output().value)

        # Format the trait nodes
        prev_value = ""
        for parent in parents:
            value = parent.for_output().value
            format_nodes(frags, traits_by_pos, parent, 0, hide=(value == prev_value))
            prev_value = value

    return "".join(str(f) for f in frags)


def format_raw_text(
    frags: list[str], parent: Base, traits_by_pos: dict[int, list[Base]], text: str
) -> None:
    start, end = get_text_pos(parent, traits_by_pos, parent.start, parent.end)
    frags.append(
        div(
            span("Raw Text", klass="raw_label"),
            span(text[start:end], klass="raw_text"),
            klass="text",
        )
    )


def format_nodes(
    frags: list[str],
    traits_by_pos: dict[int, list[Base]],
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
            children = traits_by_pos[link.start]
            for child in children:
                format_nodes(frags, traits_by_pos, child, depth + 1)
