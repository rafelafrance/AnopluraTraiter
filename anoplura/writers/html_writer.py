from datetime import datetime
from html import escape
from itertools import cycle
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from spacy.tokens import Doc

from anoplura.rules.base_rule import BaseRule
from anoplura.writers.writer_util import (
    expand_text_pos,
    get_text_pos,
    orgainize_traits,
    split_traits,
)

# from pprint import pp

CSS_CLASSES_COUNT = 30  # Look in the html_writer.css file
CSS_CLASSES = cycle([f"cc{i}" for i in range(CSS_CLASSES_COUNT)])


def writer(doc: Doc, html_file: Path) -> None:
    env = Environment(
        loader=FileSystemLoader("./anoplura/writers/templates"), autoescape=True
    )

    traits: list[BaseRule] = [e._.trait for e in doc.ents]
    traits = split_traits(traits)

    # index traits by position and group traits by type
    traits_by_pos, parents_by_type = orgainize_traits(traits)

    color_classes = get_color_classes(parents_by_type)

    formatted_text = format_text(
        traits_by_pos, parents_by_type, doc.text, color_classes
    )
    formatted_traits = format_traits(
        traits_by_pos, parents_by_type, doc.text, color_classes
    )

    # unlinked_traits = [e._.trait for e in doc._.unlinked]

    template = env.get_template("html_writer.html").render(
        now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
        formatted_traits=formatted_traits,
        formatted_text=formatted_text,
        file_name=html_file.stem,
    )

    with html_file.open("w") as out_file:
        out_file.write(template)


def get_color_classes(parents_by_type: dict[str, list]) -> dict[str, str]:
    color_classes = {}
    for type_ in parents_by_type:
        if type_ not in color_classes:
            if type_.lower() not in ("subpart", "setae"):
                color_classes[type_] = next(CSS_CLASSES)
            elif type_.lower() == "subpart":
                color_classes[type_] = "err0"
            elif type_.lower() == "setae":
                color_classes[type_] = "err1"
    return color_classes


def format_text(
    traits_by_pos: dict[int, list[BaseRule]],
    parents_by_type: dict[str, list[BaseRule]],
    text: str,
    color_classes: dict[str, str],
) -> str:
    frags = []
    slices = {}

    for type_, parents in parents_by_type.items():
        for parent in parents:
            start, end = get_text_pos(parent, traits_by_pos, parent.start, parent.end)
            if end not in slices:
                slices[end] = start, type_
            else:
                old_start, old_type_ = slices[end]
                start = min(start, old_start)
                slices[end] = start, old_type_

    slices = dict(sorted(slices.items()))
    prev = 0

    for end, (start, type_) in slices.items():
        # Add interstitial text
        if prev < start:
            frags.append(escape(text[prev:start]))

        # Set the color and appearance of the text
        class_ = color_classes[type_]

        # Add the text
        frags.append(f"""<span class="{class_}" title="{type_}">""")
        frags.append(escape(text[start:end]))
        frags.append("</span>")

        prev = end

    # Add trailing text
    if len(text) > prev:
        frags.append(escape(text[prev:]))

    return "".join(frags)


def format_traits(
    traits_by_pos: dict[int, list[BaseRule]],
    parents_by_type: dict[str, list[BaseRule]],
    text: str,
    color_classes: dict[str, str],
) -> str:
    # Format each trait and its children
    frags = []
    for type_, parents in parents_by_type.items():
        header = parents[0].for_output().key
        frags.append(f"""<div class="trait_type">{escape(header)}</div>""")

        color_class = color_classes[type_]
        for parent in parents:
            format_raw_text(frags, parent, traits_by_pos, text, color_class)

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
    frags: list[str],
    parent: BaseRule,
    traits_by_pos: dict[int, list[BaseRule]],
    text: str,
    color_class: str,
) -> None:
    start, end = get_text_pos(parent, traits_by_pos, parent.start, parent.end)
    before, after = expand_text_pos(text, start, end)
    frags.append("""<div class="text">""")
    frags.append("""<span class="raw_label">Raw text</span>""")
    frags.append(f"""<span class="raw_text">{escape(text[before:start])}</span>""")
    frags.append(
        f"""<span class="raw_text {color_class}">{escape(text[start:end])}</span>"""
    )
    frags.append(f"""<span class="raw_text">{escape(text[end:after])}</span>""")
    frags.append("""</div>""")


def format_nodes(
    frags: list[str],
    traits_by_pos: dict[int, list[BaseRule]],
    parent: BaseRule,
    depth: int = 0,
    *,
    hide: bool = False,
) -> None:
    if not hide:
        html = parent.for_output()
        frags.append(f"""<div class="level-{depth}">""")
        frags.append(f"""<span class="value">{escape(html.value)}</span>""")
        frags.append("""</div>""")

    if parent.links:
        for link in parent.links:
            children = traits_by_pos[link.start]
            for child in children:
                format_nodes(frags, traits_by_pos, child, depth + 1)
