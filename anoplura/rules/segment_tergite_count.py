from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class SegmentTergiteCount(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "position_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    segments: list[int] | None = None
    segment_position: str | None = None
    tergites: list[int] | None = None
    tergite_count_low: int | None = None
    tergite_count_high: int | None = None
    tergite_position: int | None = None
    segment_tergite_count_position: str | None = None
    segment_tergite_count_group: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="segment_tergite_count_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="segment_tergite_count_patterns",
            compiler=cls.segment_tergite_count_patterns(),
            overwrite=["segment", "tergite_count"],
        )
        add.cleanup_pipe(nlp, name="segment_tergite_count_cleanup")

    @classmethod
    def segment_tergite_count_patterns(cls):
        return [
            Compiler(
                label="segment_tergite_count",
                on_match="segment_tergite_count_match",
                decoder={
                    "filler": {"POS": {"IN": ["ADP"]}},
                    "count": {"ENT_TYPE": "tergite_count"},
                    "group": {"ENT_TYPE": "group"},
                    "pos": {"ENT_TYPE": "position"},
                    "seg": {"ENT_TYPE": "segment"},
                },
                patterns=[
                    " count+ pos* filler* group* seg+ ",
                ],
            ),
        ]

    @classmethod
    def segment_tergite_count_match(cls, ent):
        segs, seg_pos = None, None
        terg, terg_low, terg_high, terg_pos = None, None, None, None
        pos, group = None, None

        for sub_ent in ent.ents:
            if sub_ent.label_ == "segment":
                segs = sub_ent._.trait.segments
                seg_pos = sub_ent._.trait.segment_position

            elif sub_ent.label_ == "tergite_count":
                terg = sub_ent._.trait.tergites
                terg_low = sub_ent._.trait.tergite_count_low
                terg_high = sub_ent._.trait.tergite_count_high
                terg_pos = sub_ent._.trait.tergite_position

            elif sub_ent.label_ == "position":
                text = sub_ent.text.lower()
                pos = cls.replace.get(text, text)

            elif sub_ent.label_ == "group":
                text = sub_ent.text.lower()
                group = cls.replace.get(text, text)

        return cls.from_ent(
            ent,
            segments=segs,
            segment_position=seg_pos,
            tergites=terg,
            tergite_count_low=terg_low,
            tergite_count_high=terg_high,
            tergite_position=terg_pos,
            segment_tergite_count_position=pos,
            segment_tergite_count_group=group,
        )


@registry.misc("segment_tergite_count_match")
def segment_tergite_count_match(ent):
    return SegmentTergiteCount.segment_tergite_count_match(ent)
