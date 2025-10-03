from collections import defaultdict
from datetime import datetime
from html import escape
from itertools import cycle
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from anoplura.rules.base import Base, as_dict

COLOR_COUNT = 30
BACKGROUNDS = cycle([f"cc{i}" for i in range(COLOR_COUNT)])


def writer(traits: list[Base], text: str, html_file: Path) -> None:
    env = Environment(
        loader=FileSystemLoader("./anoplura/writers/templates"), autoescape=True
    )

    classes = build_classes(traits)

    template = env.get_template("html_writer.html").render(
        now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
        text=format_text(text, traits, classes),
        traits=format_traits(text, traits, classes),
        file_name=html_file.stem,
    )

    with html_file.open("w") as out_file:
        out_file.write(template)


def build_classes(traits: list[Base]) -> dict[str, int]:
    """Make tags for HTML text color highlighting."""
    classes = {}
    for trait in traits:
        if trait._trait not in classes:
            name = trait._trait.replace(" ", "_")
            classes[name] = next(BACKGROUNDS)
    return classes


def format_text(_text: str, traits: list[Base], _classes: dict[str, int]) -> str:
    """Colorize and format the text for HTML."""
    # Build index
    indexed = {t.start: t for t in traits}
    indexed = dict(sorted(indexed.items()))

    # Get unlinked traits
    linked = set()
    for trait in indexed.values():
        if trait.links:
            for link in trait.links:
                linked.add(link.start)
    roots = set(indexed.keys()) - linked

    for start in sorted(roots):
        print("=" * 80)
        parent = indexed[start]
        show_children(indexed, parent, 0)

    return ""


def show_children(indexed: dict[int, Base], parent: Base, depth: int = 0) -> None:
    spaces = "    " * depth
    print(f"{spaces} {parent}")
    if parent.links:
        for link in parent.links:
            child = indexed[link.start]
            show_children(indexed, child, depth + 1)


def old_format_text(text: str, traits: list[Base], classes: dict[str, int]) -> str:
    """Colorize and format the text for HTML."""
    frags = []

    prev = 0
    for trait in traits:
        cls = trait._trait.replace(" ", "_")

        start = trait.start
        end = trait.end
        title = ", ".join(f"{k} = {v}" for k, v in as_dict(trait).items())
        title = f"{trait._trait}: {title}" if title else trait._trait
        if prev < start:
            frags.append(escape(text[prev:start]))
        frags.append(f'<span class="{classes[cls]}" title="{title}">')
        frags.append(escape(text[start:end]))
        frags.append("</span>")
        prev = end

    if len(text) > prev:
        frags.append(text[prev:])

    return "".join(frags)


def new_format_traits(
    _text: str, _traits: list[Base], _classes: dict[str, int]
) -> dict[Any, Any]:
    formatted = {}
    return formatted


def format_traits(
    text: str, traits: list[Base], classes: dict[str, int]
) -> dict[Any, Any]:
    """Format the traits for HTML."""
    formatted = {}

    # Group by traits name
    groups = defaultdict(list)
    for trait in traits:
        groups[trait._trait].append(trait)

    groups = dict(sorted(groups.items(), key=lambda i: i[0]))

    # Format each trait group
    for cls, traits_ in groups.items():
        name = cls.replace("_", " ")
        span = f'<span class="{classes[cls]}">{name}</span>'

        # Format each trait within a trait group
        new_traits = []
        for trait in traits_:
            text_ = text[trait.start : trait.end]
            trait = ", ".join(
                f'<span title="{text_}">{k}:&nbsp;{v}</span>'
                for k, v in as_dict(trait).items()
            )
            new_traits.append(trait)

        formatted[span] = "<br/>".join(new_traits)

    return formatted
