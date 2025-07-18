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
    part: str | list[str] | None = None
    which: str | list[str] | list[int] | None = None


@dataclass(eq=False)
class Base(TraiterBase):
    sex: str | None = None

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
    part = BodyPart(part=trait.part, which=trait.which)
    return part


def get_all_body_parts(sub_ents):
    body_parts = [get_body_part(e) for e in sub_ents]
    parts = [p.part for p in body_parts]
    parts = parts[0] if len(parts) == 1 else parts
    which = [p.which for p in body_parts if p.which]
    which = which[0] if len(which) == 1 else which
    which = which if which else None
    return parts, which
