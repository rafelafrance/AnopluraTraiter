from dataclasses import asdict, dataclass, field

from traiter.rules.rule import Rule as TraiterRule

# Fields to skip when outputting data
SKIPS = {"start", "end", "trait", "links"}

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

    def __hash__(self) -> int:
        return hash(tuple(self.to_dict().items()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Link):
            return False
        return self.to_dict() == other.to_dict()

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None and k[0] != "_"}


@dataclass
class ForOutput:
    key: str
    value: str = ""


@dataclass(eq=False)
class Rule(TraiterRule):
    sex: str = ""
    links: list = field(default_factory=list)

    def __hash__(self) -> int:
        dct = as_dict(self)
        if "links" in dct:
            del dct["links"]
        dct = {k: tuple(v) if isinstance(v, list) else v for k, v in dct.items()}
        return hash(tuple(dct.items()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rule):
            return False
        return as_dict(self) == as_dict(other)

    def link(self, child: "Rule") -> None:
        if child == self:
            return
        link = Link(
            trait=child._trait, start=child.start, end=child.end, _text=child._text
        )
        if not self.links:
            self.links = []
        if all(lk != link for lk in self.links):
            self.links.append(link)

    @property
    def is_linked(self) -> bool:
        return bool(self.links) and len(self.links) != 0

    @property
    def is_unlinked(self) -> bool:
        return not bool(self.links) or len(self.links) == 0

    def for_output(self) -> ForOutput:
        return ForOutput(key="Trait", value=self._text)


def as_dict(trait: Rule) -> dict:
    """Convert trait to a dict: ignore some fields & lift others into a flat dict."""
    dct = filter_fields(trait, SKIPS)
    key = next((k for k in dct if k.endswith("dims")), None)
    if key:
        for dim in dct[key]:
            new_key = f"{key}_{dim['dim']}"
            dct[new_key] = filter_fields(trait, SKIPS)
        del dct[key]

    if trait.links:
        dct["links"] = [filter_fields(link, SKIPS) for link in trait.links]

    return dct


def filter_fields(trait: Rule, skips: set[str]) -> dict:
    """Remove some fields from an output dict when displaying traits."""
    return {
        k: v
        for k, v in asdict(trait).items()
        if v is not None and k not in skips and not k.startswith("_")
    }
