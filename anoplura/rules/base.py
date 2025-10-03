from dataclasses import asdict, dataclass

from spacy.language import Language
from traiter.rules.base import Base as TraiterBase

# Fields to skip when outputting data
SKIPS = {"start", "end", "trait", "links"}
DIM_SKIPS = SKIPS | {"dim"}

# Parts get parsed differently so they are not the same object
PARTS: list[str] = [
    "part",
    "gonopod",
    "plate",
    "segment",
    "sternite",
    "tergite",
]

ANY_PART: list[str] = [*PARTS, "subpart", "seta"]


@dataclass
class Link:
    trait: str
    start: int
    end: int
    _text: str = ""

    def __eq__(self, other: "Link") -> bool:
        return self.to_dict() == other.to_dict()

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None and k[0] != "_"}


@dataclass(eq=False)
class Base(TraiterBase):
    sex: str | None = None
    links: list | None = None

    def __eq__(self, other: "Base") -> bool:
        return as_dict(self) == as_dict(other)

    def __str__(self) -> str:
        return f"{self._trait}: {self._text}"

    @classmethod
    def pipe(cls, nlp: Language) -> None: ...

    def link(self, child: "Base") -> None:
        if child == self:
            return
        link = Link(
            trait=child._trait, start=child.start, end=child.end, _text=child._text
        )
        if not self.links:
            self.links = []
        if all(lk != link for lk in self.links):
            self.links.append(link)


def as_dict(trait: Base) -> dict:
    """Convert trait to a dict: ignore some fields & lift others into a flat dict."""
    dct = filter_fields(trait, SKIPS)
    key = next((k for k in dct if k.endswith("dims")), None)
    if key:
        for dim in dct[key]:
            new_key = f"{key}_{dim['dim']}"
            dct[new_key] = filter_fields(trait, DIM_SKIPS)
        del dct[key]

    if trait.links:
        dct["links"] = [filter_fields(link, SKIPS) for link in trait.links]

    return dct


def filter_fields(trait: Base, skips: set[str]) -> dict:
    """Remove some fields from an output dict when displaying traits."""
    return {
        k: v
        for k, v in asdict(trait).items()
        if v is not None and k not in skips and not k.startswith("_")
    }
