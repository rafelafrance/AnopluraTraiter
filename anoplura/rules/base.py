from dataclasses import dataclass

from spacy import Language
from traiter.rules.base import Base as TraiterBase

# Fields to skip when outputting data
SKIPS = {"start", "end", "trait"}
MORE_SKIPS = SKIPS | {"dim"}

# Parts get parsed differently so they cannot be the same object
PARTS: list[str] = [
    "part",
    "gonopod",
    "plate",
    "segment",
    "sternite",
    "tergite",
]


@dataclass(eq=False)
class Base(TraiterBase):
    sex: "Base | None" = None

    @classmethod
    def pipe(cls, nlp: Language) -> None: ...


def as_dict(trait: Base) -> dict:
    """Convert trait to a dict: ignore some fields and lift others into a flat dict."""
    dct = filter_fields(trait, SKIPS)
    key = next((k for k in dct if k.endswith("dims")), None)
    if key:
        for dim in dct[key]:
            new_key = f"{key}_{dim['dim']}"
            dct[new_key] = filter_fields(trait, MORE_SKIPS)
        del dct[key]
    return dct


def filter_fields(trait: Base, skips: set[str]) -> dict:
    """Remove some fields from an output dict when displaying traits."""
    return {
        k: v
        for k, v in trait.to_dict().items()
        if v is not None and k not in skips and not k.startswith("_")
    }
