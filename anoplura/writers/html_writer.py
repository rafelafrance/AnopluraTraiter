from collections import defaultdict
from itertools import cycle
from pathlib import Path
from typing import Any

from spacy.tokens import Doc

from anoplura.rules.base import Base, as_dict

CSS_CLASSES_COUNT = 30  # Look in the html_writer.css file
CSS_CLASSES = cycle([f"cc{i}" for i in range(CSS_CLASSES_COUNT)])


def writer(doc: Doc, _html_file: Path) -> None:
    # env = Environment(
    #     loader=FileSystemLoader("./anoplura/writers/templates"), autoescape=True
    # )

    traits: list[Base] = [e._.trait for e in doc.ents]

    # css_classes: dict[str, str] = build_css_classes(traits)

    print("#" * 80)
    format_trait_tree(traits, doc.text)

    # unlinked_traits = [e._.trait for e in doc._.unlinked]

    # print("\n")
    # print("=" * 80)
    # format_trait_tree(unlinked_traits, doc.text)

    # template = env.get_template("html_writer.html").render(
    #     now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
    #     text=format_text(text, traits, classes),
    #     traits=format_traits(text, traits, classes),
    #     file_name=html_file.stem,
    # )
    #
    # with html_file.open("w") as out_file:
    #     out_file.write(template)


def format_trait_tree(traits: list[Base], text: str) -> str:
    indexed_by_start_index = {t.start: t for t in traits}
    indexed_by_start_index = dict(sorted(indexed_by_start_index.items()))

    indexed_by_trait_name: dict[str, list[Base]] = defaultdict(list)
    _ = {indexed_by_trait_name[t._trait].append(t) for t in traits}

    for trait_name in ("taxon", "date", "lat_long", "elevation", "specimen_type"):
        traits = indexed_by_trait_name.get(trait_name, [])
        if traits:
            print("-" * 80)
            for trait in traits:
                format_parent_data(trait, indexed_by_start_index, text)
                format_nodes(indexed_by_start_index, trait, 0)
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
        print("-" * 80)
        parent = indexed_by_start_index[start]
        format_parent_data(parent, indexed_by_start_index, text)
        format_nodes(indexed_by_start_index, parent, 0)

    return ""


def format_parent_data(
    parent: Base, indexed_by_start_index: dict[int, Base], text: str
) -> None:
    start, end = get_text_indexes(
        parent, indexed_by_start_index, parent.start, parent.end
    )
    parent_name = " ".join(parent._trait.split("_")).title()
    print(f"Trait type: {parent_name}")
    print(f"Raw text: {text[start:end]}")
    print()


def get_text_indexes(
    parent: Base, indexed_by_start_index: dict[int, Base], start: int, end: int
) -> tuple[int, int]:
    start = min(start, parent.start)
    end = max(end, parent.end)
    for link in parent.links:
        child = indexed_by_start_index[link.start]
        start, end = get_text_indexes(child, indexed_by_start_index, start, end)
    return start, end


def format_nodes(indexed: dict[int, Base], parent: Base, depth: int = 0) -> None:
    spaces = "    " * depth
    sex = f"{parent.sex.title()} " if parent.sex and depth == 0 else ""
    formatted = f"{sex}{parent.for_html()}"
    print(f"{spaces}{formatted}")
    if parent.links:
        for link in parent.links:
            child = indexed[link.start]
            format_nodes(indexed, child, depth + 1)


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


def build_css_classes(traits: list[Base]) -> dict[str, str]:
    classes = {}
    for trait in traits:
        if trait._trait not in classes:
            name = trait._trait
            name = name.replace(" ", "_")
            classes[name] = next(CSS_CLASSES)
    return classes


# def old_format_text(text: str, traits: list[Base], classes: dict[str, int]) -> str:
#     """Colorize and format the text for HTML."""
#     frags = []
#
#     prev = 0
#     for trait in traits:
#         cls = trait._trait if trait._trait else ""
#         cls = cls.replace(" ", "_")
#
#         start = trait.start
#         end = trait.end
#         title = ", ".join(f"{k} = {v}" for k, v in as_dict(trait).items())
#         title = f"{trait._trait}: {title}" if title else trait._trait
#         if prev < start:
#             frags.append(escape(text[prev:start]))
#         frags.append(f'<span class="{classes[cls]}" title="{title}">')
#         frags.append(escape(text[start:end]))
#         frags.append("</span>")
#         prev = end
#
#     if len(text) > prev:
#         frags.append(text[prev:])
#
#     return "".join(frags)
