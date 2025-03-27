from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class Segment(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "body_part_terms.csv",
    ]
    # ----------------------

    segments: list[int] | None = None
    segment_position: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="segment_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="segment_patterns",
            compiler=cls.segment_patterns(),
            overwrite=["number", "range"],
        )
        add.cleanup_pipe(nlp, name="segment_cleanup")

    @classmethod
    def segment_patterns(cls):
        return [
            Compiler(
                label="segment",
                on_match="segment_match",
                keep="segment",
                decoder={
                    "9": {"ENT_TYPE": "number"},
                    "9-9": {"ENT_TYPE": "range"},
                    "pos": {"ENT_TYPE": "position"},
                    "segment": {"ENT_TYPE": "segments"},
                },
                patterns=[
                    " segment 9 ",
                    " segment 9-9+ ",
                    " pos+ segment 9* ",
                    " pos+ segment 9-9* ",
                ],
            ),
        ]

    @classmethod
    def segment_match(cls, ent):
        segments = []
        pos = []

        for sub_ent in ent.ents:
            if sub_ent.label_ == "number":
                segments.append(int(sub_ent._.trait.number))

            elif sub_ent.label_ == "position":
                pos.append(sub_ent.text.lower())

            elif sub_ent.label_ == "range":
                low = int(sub_ent._.trait.low)
                high = int(sub_ent._.trait.high)
                segments += list(range(low, high + 1))

        segments = sorted(set(segments)) if segments else None
        pos = " ".join(pos) if pos else None

        return cls.from_ent(ent, segments=segments, segment_position=pos)


@registry.misc("segment_match")
def segment_match(ent):
    return Segment.segment_match(ent)
