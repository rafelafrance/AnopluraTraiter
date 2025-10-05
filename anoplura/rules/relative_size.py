from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import ANY_PART, PARTS, Base


@dataclass(eq=False)
class RelativeSize(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "size_terms.csv",
    ]
    pos: ClassVar[list[str]] = ["ADV", "ADP", "ADJ"]
    # ----------------------

    relative_size: str | None = None
    relative_part: str | None = None
    relative_part_number: list[int] | None = None

    def __str__(self) -> str:
        val = f"{self._trait}: {self.relative_size} {self.relative_part}"
        if self.relative_part_number:
            val += f" {self.relative_part_number}"
        return val

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="relative_size_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.trait_pipe(
            nlp,
            name="relative_size_patterns",
            compiler=cls.relative_size_patterns(),
            overwrite=ANY_PART,
        )
        add.cleanup_pipe(nlp, name="relative_size_cleanup")

    @classmethod
    def relative_size_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="relative_size",
                on_match="relative_size_match",
                decoder={
                    "adv": {"POS": {"IN": cls.pos}},
                    "any_part": {"ENT_TYPE": {"IN": ANY_PART}},
                    "rel": {"ENT_TYPE": "rel_size"},
                },
                patterns=[
                    " adv* rel+ any_part+ ",
                ],
            ),
        ]

    @classmethod
    def relative_size_match(cls, ent: Span) -> "RelativeSize":
        part, num = None, None
        for e in ent.ents:
            if e.label_ in PARTS:
                part = e._.trait.part
                num = e._.trait.number if hasattr(e._.trait, "number") else None
            elif e.label_ == "subpart":
                part = e._.trait.subpart
            elif e.label_ == "seta":
                part = e._.trait.seta

        size = [
            t.lower_ for t in ent if t.ent_type_ == "relative_size" or t.pos_ in cls.pos
        ]
        size = " ".join(size)

        return cls.from_ent(
            ent, relative_size=size, relative_part=part, relative_part_number=num
        )


@registry.misc("relative_size_match")
def relative_size_match(ent: Span) -> RelativeSize:
    return RelativeSize.relative_size_match(ent)
