"""Write output to an HTML file."""
from collections import defaultdict
from datetime import datetime
from html import escape
from itertools import cycle

from jinja2 import Environment, FileSystemLoader
from spacy import displacy

OPTIONS = {
    "colors": {
        "GENUS": "#a6cee388",
        "SCI_NAME": "#1f78b488",
        "BODY_PART": "#cab2d688",
        "DESCRIPTION": "#b2df8a88",
        "SETAE": "#33a02c88",
        "SIZE": "#fb9a9988",
        "SETA_COUNT": "#e31a1c88",
        "TOTAL_LENGTH": "#fdbf6f88",
        "MAX_WIDTH": "#ff7f0088",
        "SEX": "#b1592888",
        "qq2": "#ffff9988",
        "qq5": "#6a3d9a88",
        "qq3": "#dddddd88",
        "HEADING": "#b3b3b388",
    },
}


def html_writer(_, rows):
    """Output the data."""
    sentences = []
    for row in rows:
        sentences += list(row["doc"].sents)
        # for sent in row['doc'].sents:
        #     print('=' * 80)
        #     print(sent)
        #     for ent in sent.ents:
        #         print(ent.label_, ent._.data)
        #     print()
    displacy.serve(sentences, style="ent", options=OPTIONS)


COLOR_COUNT = 14
BACKGROUNDS = cycle([f"c{i}" for i in range(COLOR_COUNT)])
BORDERS = cycle([f"b{i}" for i in range(COLOR_COUNT)])

SKIPS = {"start", "end", "trait", "part", "subpart"}


def html_writer_(args, rows):
    """Output the data."""
    rows = sorted(rows, key=lambda r: (r.get("flora_id"), r["family"], r["taxon"]))

    classes = build_classes(rows)

    for row in rows:
        row["raw_text"] = row["text"]
        row["text"] = format_text(row, classes)
        row["traits"] = format_traits(row, classes)

    env = Environment(
        loader=FileSystemLoader("./anoplura/writers/templates"), autoescape=True
    )

    template = env.get_template("html_writer.html").render(
        now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"), rows=rows
    )
    args.html_file.write(template)
    args.html_file.close()


def build_classes(rows):
    """
    Make tags for HTML text color highlighting.

    Tag keys are the trait name and if it's an open or close tag.
    For example:
        (trait_name, is_open) -> <span class="css_class">
        (trait_name, not_open) -> </span>
    """
    backgrounds = {}
    borders = {}

    tags = {
        "part": "bold",
        "subpart": "bold-italic",
    }

    for row in rows:
        for trait in row["traits"]:
            if trait["trait"] in {"part", "subpart"}:
                continue
            if "part" not in trait:
                continue
            name = trait_label(trait, "_")
            name_parts = name.split("_")
            bg, border = name_parts[0], name_parts[-1]
            if bg not in backgrounds:
                backgrounds[bg] = next(BACKGROUNDS)
            if border not in borders:
                borders[border] = next(BORDERS)
            classes = f"{backgrounds[bg]} {borders[border]} c{backgrounds[bg]}"
            tags[name] = classes
    return tags


def format_traits(row, classes):
    """Format the traits for HTML."""
    new_dict = {}

    # Group by trait name
    groups = defaultdict(list)
    for trait in row["traits"]:
        if "part" not in trait:
            continue
        if trait["trait"] not in {"part", "subpart"}:
            label = trait_label(trait, "_")
            groups[label].append(trait)
    groups = dict(sorted(groups.items(), key=lambda i: i[0]))

    # Format each trait group
    for name, traits in groups.items():
        label = name.replace("_", " ")
        span = f'<span class="{classes[name]}">{label}</span>'

        # Format each trait within a trait group
        new_traits = []
        for trait in traits:
            text = row["raw_text"][trait["start"] : trait["end"]]
            trait = ", ".join(
                f'<span title="{text}">{k}:&nbsp;{v}</span>'
                for k, v in trait.items()
                if k not in SKIPS
            )
            new_traits.append(trait)
        new_dict[span] = "<br/>".join(new_traits)

    return new_dict


def format_text(row, classes):
    """Colorize and format the text for HTML."""
    text = row["raw_text"]
    frags = []

    prev = 0
    for trait in row["traits"]:
        if "part" not in trait:
            continue
        if trait["trait"] == "part":
            label = trait["part"]
            name = "part"
        elif trait["trait"] == "subpart":
            label = f"{trait['part']} {trait['subpart']}"
            name = "subpart"
        else:
            label = trait_label(trait)
            name = trait_label(trait, "_")

        start = trait["start"]
        end = trait["end"]
        title = ", ".join(f"{k} = {v}" for k, v in trait.items() if k not in SKIPS)
        title = f"{label}: {title}" if title else label
        if prev < start:
            frags.append(escape(text[prev:start]))
        frags.append(f'<span class="{classes[name]}" title="{title}">')
        frags.append(escape(text[start:end]))
        frags.append("</span>")
        prev = end

    if len(text) > prev:
        frags.append(text[prev:])

    return "".join(frags)


def trait_label(trait, sep=" "):
    """Generate a label for the trait."""
    label = [trait["part"]]
    if "subpart" in trait:
        label.append(trait["subpart"])
    label.append(trait["trait"])
    label = sep.join(label)
    label = label.replace("-", "")
    label = label.replace("indumentum" + sep + "surface", "indumentum")
    return label
