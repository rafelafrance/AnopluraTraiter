from collections import defaultdict

from anoplura.rules.base import Base

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


def get_text_pos(
    parent: Base, trait_pos: dict[int, Base], start: int, end: int
) -> tuple[int, int]:
    """Find the entire string used for the trait."""
    start = min(start, parent.start)
    end = max(end, parent.end)
    for link in parent.links:
        child = trait_pos[link.start]
        start, end = get_text_pos(child, trait_pos, start, end)
    return start, end


def orgainize_traits(traits: list[Base]) -> tuple[dict, dict]:
    """Index traits by position, and group traits by type."""
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
    parent_type = defaultdict(list)
    for start in parent_pos:
        parent = trait_pos[start]
        key = parent.for_output().key
        parent_type[(ORDER[parent._trait], key)].append(parent)
    parent_type = dict(sorted(parent_type.items()))

    return trait_pos, parent_type
