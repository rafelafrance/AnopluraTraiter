from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base, ForOutput


@dataclass(eq=False)
class Segment(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    # ----------------------

    part: str = "segment"
    number: list[int] | None = None

    def for_output(self) -> ForOutput:
        number = ""
        if self.number:
            number = " " + ", ".join([str(n) for n in self.number])
        text = self.part.title() + number
        return ForOutput(key=text, value=text)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="segment_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.trait_pipe(
            nlp,
            name="segment_patterns",
            compiler=cls.segment_patterns(),
            overwrite=["number", "range", "position"],
        )
        add.cleanup_pipe(nlp, name="segment_cleanup")

    @classmethod
    def segment_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="segment",
                on_match="segment_match",
                decoder={
                    "9": {"ENT_TYPE": "number"},
                    "9-9": {"ENT_TYPE": "range"},
                    "pos": {"ENT_TYPE": "position"},
                    "segment": {"ENT_TYPE": "segments"},
                },
                patterns=[
                    " segment+ ",
                    " segment+ 9 ",
                    " segment+ 9-9+ ",
                    " pos+ segment+ 9* ",
                    " pos+ segment+ 9-9* ",
                ],
            ),
        ]

    @classmethod
    def segment_match(cls, ent: Span) -> "Segment":
        number = []
        part = []

        for sub_ent in ent.ents:
            if sub_ent.label_ == "number":
                number.append(int(sub_ent._.trait.number))

            elif sub_ent.label_ == "position":
                part.append(sub_ent.text.lower())

            elif sub_ent.label_ == "range":
                low = int(sub_ent._.trait.low)
                high = int(sub_ent._.trait.high)
                number += list(range(low, high + 1))

        part = " ".join([*part, "segment"])

        number = sorted(set(number)) if number else None

        return cls.from_ent(ent, part=part, number=number)


@registry.misc("segment_match")
def segment_match(ent: Span) -> Segment:
    return Segment.segment_match(ent)
