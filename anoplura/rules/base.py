from dataclasses import dataclass

from spacy.language import Language
from traiter.rules.base import Base as TraiterBase

SKIPS = {"start", "end", "trait"}
MORE_SKIPS = SKIPS | {"dim"}

PARTS: list[str] = [
    "part",
    "gonopod",
    "plate",
    "segment",
    "sternite",
    "tergite",
]


@dataclass
class BodyPart:
    body_part: str | list[str] | None = None
    which: str | list[str] | list[int] | None = None


@dataclass(eq=False)
class Base(TraiterBase):
    sex: str | None = None
    body_part: str | None = None
    which: str | list[int] | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError


def as_dict(trait) -> dict:
    dct = {
        k: v
        for k, v in trait.to_dict().items()
        if v is not None and k not in SKIPS and not k.startswith("_")
    }
    key = next((k for k in dct if k.endswith("dims")), None)
    if key:
        for dim in dct[key]:
            new_key = f"{key}_{dim['dim']}"
            dct[new_key] = {
                k: v
                for k, v in dim.items()
                if v is not None and k not in MORE_SKIPS and not k.startswith("_")
            }
        del dct[key]
    return dct


def get_body_part(sub_ent) -> BodyPart:
    trait = sub_ent._.trait

    body_part = BodyPart(body_part=trait._trait)

    match trait._trait:
        case "part":
            body_part.which = trait.part
        case "gonopod":
            body_part.which = trait.gonopods
        case "plate":
            body_part.which = trait.plates
        case "segment":
            body_part.which = trait.segment if trait.segment else trait.segments
        case "subpart":
            body_part.which = trait.subpart
        case "sternite":
            body_part.which = trait.sternites
        case "tergite":
            body_part.which = trait.tergites

    return body_part


def get_all_body_parts(sub_ents):
    body_parts = [get_body_part(e) for e in sub_ents]
    parts = [p.body_part for p in body_parts]
    parts = parts[0] if len(parts) == 1 else parts
    which = [p.which for p in body_parts]
    which = which[0] if len(which) == 1 else which
    return parts, which
