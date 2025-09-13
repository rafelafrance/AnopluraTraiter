from dataclasses import dataclass

from spacy import Language
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


@dataclass(eq=False)
class Base(TraiterBase):
    sex: str | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None: ...


def as_dict(trait: Base) -> dict:
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
