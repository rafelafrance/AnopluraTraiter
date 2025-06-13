from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Segment(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    # ----------------------

    segments: list[int] | None = None
    segment_position: str | None = None
    segment_subpart: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="segment_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="segment_patterns",
            compiler=cls.segment_patterns(),
            overwrite=["number", "range", "subpart"],
        )
        add.cleanup_pipe(nlp, name="segment_cleanup")

    @classmethod
    def segment_patterns(cls):
        return [
            Compiler(
                label="segment",
                on_match="segment_match",
                decoder={
                    "9": {"ENT_TYPE": "number"},
                    "9-9": {"ENT_TYPE": "range"},
                    "adp": {"POS": "ADP"},
                    "pos": {"ENT_TYPE": "position"},
                    "segment": {"ENT_TYPE": "segments"},
                    "subpart": {"ENT_TYPE": "subpart"},
                },
                patterns=[
                    " segment 9 ",
                    " segment 9-9+ ",
                    " segment 9    adp* subpart+ ",
                    " segment 9-9+ adp* subpart+ ",
                    " pos+ segment 9* ",
                    " pos+ segment 9-9* ",
                    " pos+ segment 9*   adp* subpart+ ",
                    " pos+ segment 9-9* adp* subpart+ ",
                ],
            ),
        ]

    @classmethod
    def segment_match(cls, ent):
        segments = []
        pos = []
        subpart = None

        for sub_ent in ent.ents:
            if sub_ent.label_ == "number":
                segments.append(int(sub_ent._.trait.number))

            elif sub_ent.label_ == "position":
                pos.append(sub_ent.text.lower())

            elif sub_ent.label_ == "subpart":
                subpart = sub_ent._.trait.subpart

            elif sub_ent.label_ == "range":
                low = int(sub_ent._.trait.low)
                high = int(sub_ent._.trait.high)
                segments += list(range(low, high + 1))

        segments = sorted(set(segments)) if segments else None
        pos = " ".join(pos) if pos else None

        return cls.from_ent(
            ent, segments=segments, segment_position=pos, segment_subpart=subpart
        )


@registry.misc("segment_match")
def segment_match(ent):
    return Segment.segment_match(ent)
