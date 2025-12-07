import string
from collections import defaultdict
from copy import deepcopy

from anoplura.rules.gonopod import Gonopod
from anoplura.rules.plate import Plate
from anoplura.rules.rule import Rule
from anoplura.rules.segment import Segment
from anoplura.rules.sternite import Sternite
from anoplura.rules.tergite import Tergite

# Used for spliting numbered traits
NumberedPart = Gonopod | Plate | Segment | Sternite | Tergite

ORDER = {
    "taxon": 1,
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

SKIP_BEGIN = string.punctuation + string.whitespace


def get_text_pos(
    parent: Rule, traits_by_pos: dict[int, list[Rule]], start: int, end: int
) -> tuple[int, int]:
    """Find the entire string used for the trait."""
    start = min(start, parent.start)
    end = max(end, parent.end)
    for link in parent.links:
        children = traits_by_pos[link.start]
        for child in children:
            start, end = get_text_pos(child, traits_by_pos, start, end)
    return start, end


def expand_text_pos(text: str, start: int, end: int) -> tuple[int, int]:
    """Find the start of the phrase that contains the parsed text."""
    b_semi = text.rfind(";", 0, start)
    b_semi = max(b_semi, 0)
    b_dot = text.rfind(".", 0, start)
    b_dot = max(b_dot, 0)
    before = max(b_semi, b_dot)
    while text[before] in SKIP_BEGIN:
        before += 1

    length = len(text)
    a_semi = text.find(";", end)
    a_semi = a_semi if a_semi > -1 else length
    a_dot = text.find(".", end)
    a_dot = a_dot if a_dot > -1 else length
    after = min(a_semi + 1, a_dot + 1, length)

    return before, after


def orgainize_traits(traits: list[Rule]) -> tuple[dict[int, list], dict[str, list]]:
    """Index traits by position, and group traits by type."""
    # Index the traits by their position in the document
    traits_by_pos: dict[int, list[Rule]] = defaultdict(list)
    for trait in traits:
        traits_by_pos[trait.start].append(trait)

    # Find the children of each trait
    child_traits = set()
    for trait_list in traits_by_pos.values():
        for trait in trait_list:
            if trait.links:
                for link in trait.links:
                    child_traits.add(link.start)

    # Parent traits are those that are not in child traits
    parent_pos = set(traits_by_pos) - child_traits

    # Sort parent traits by their type
    sortable_parents = defaultdict(list)
    for start in parent_pos:
        parents = traits_by_pos[start]
        for parent in parents:
            type_ = parent.for_output().key
            sortable_parents[ORDER.get(parent._trait, 9999), type_].append(parent)
    sortable_parents = dict(sorted(sortable_parents.items()))
    parents_by_type = {k[1]: v for k, v in sortable_parents.items()}

    return traits_by_pos, parents_by_type


def split_traits(traits: list[Rule | NumberedPart]) -> list[Rule]:
    """Split numbered parts so that each number is in its own trait."""
    new_traits: list[NumberedPart | Rule] = []

    for trait in traits:
        if isinstance(trait, NumberedPart) and trait.number:
            for number in trait.number:
                new = deepcopy(trait)
                new.number = [number]
                new_traits.append(new)
        else:
            new_traits.append(trait)

    return new_traits
