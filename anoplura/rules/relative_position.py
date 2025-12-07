from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base_rule import ANY_PART, PARTS, BaseRule, ForOutput


@dataclass(eq=False)
class RelativePosition(BaseRule):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
    ]
    # ----------------------

    relative_position: str | None = None
    relative_part: str | None = None
    relative_part_number: list[int] | None = None

    def for_output(self) -> ForOutput:
        text = f"Position: {self.relative_position} {self.relative_part}"
        number = ""
        if self.relative_part_number:
            number = " " + ", ".join([str(n) for n in self.relative_part_number])
        return ForOutput("Position", value=text + number)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="relative_position_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.trait_pipe(
            nlp,
            name="relative_position_patterns",
            compiler=cls.relative_position_patterns(),
            overwrite=ANY_PART,
        )
        add.cleanup_pipe(nlp, name="relative_position_cleanup")

    @classmethod
    def relative_position_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="relative_position",
                on_match="relative_position_match",
                decoder={
                    "any_part": {"ENT_TYPE": {"IN": ANY_PART}},
                    "rel": {"ENT_TYPE": "rel_pos"},
                },
                patterns=[
                    " rel+ any_part+ ",
                ],
            ),
        ]

    @classmethod
    def relative_position_match(cls, ent: Span) -> "RelativePosition":
        size = []
        part, num = None, None
        for e in ent.ents:
            if e.label_ == "rel_pos":
                size.append(e.text.lower())
            elif e.label_ in PARTS:
                part = e._.trait.part
                num = e._.trait.number if hasattr(e._.trait, "number") else None
            elif e.label_ == "subpart":
                part = e._.trait.subpart
            elif e.label_ == "seta":
                part = e._.trait.seta

        size = " ".join(size)

        return cls.from_ent(
            ent, relative_position=size, relative_part=part, relative_part_number=num
        )


@registry.misc("relative_position_match")
def relative_position_match(ent: Span) -> RelativePosition:
    return RelativePosition.relative_position_match(ent)
