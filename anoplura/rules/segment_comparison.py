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
class SegmentComparison(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "relative_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    segments: list[int] | None = None
    segment_position: str | None = None
    segment_comparison: str | None = None
    segment_shape: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="segment_comparison_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="segment_comparison_patterns",
            compiler=cls.segment_comparison_patterns(),
            overwrite=["segment"],
        )
        add.cleanup_pipe(nlp, name="segment_comparison_cleanup")

    @classmethod
    def segment_comparison_patterns(cls):
        return [
            Compiler(
                label="segment_comparison",
                on_match="segment_comparison_match",
                decoder={
                    "and": {"POS": {"IN": ["CCONJ"]}},
                    "filler": {"POS": {"IN": ["ADP"]}},
                    "pos": {"ENT_TYPE": "position"},
                    "rel": {"ENT_TYPE": "relative_term"},
                    "seg": {"ENT_TYPE": "segment"},
                    "other": {"ENT_TYPE": "segments"},
                },
                patterns=[
                    " seg+ rel+ other+ ",
                    " seg+ rel+ other+ and rel+ ",
                ],
            ),
        ]

    @classmethod
    def segment_comparison_match(cls, ent):
        segs, seg_pos, other = None, None, ""
        rel = [[]]

        for sub_ent in ent.ents:
            if sub_ent.label_ == "segment":
                segs = sub_ent._.trait.segments
                seg_pos = sub_ent._.trait.segment_position

            elif sub_ent.label_ == "segments":
                text = sub_ent.text.lower()
                other = text
                rel.append([])

            elif sub_ent.label_ == "relative_term":
                text = sub_ent.text.lower()
                rel[-1].append(text)

        compare = " ".join([*rel[0], other])
        shape = " ".join(rel[1]) if len(rel) > 1 else None

        return cls.from_ent(
            ent,
            segments=segs,
            segment_position=seg_pos,
            segment_comparison=compare,
            segment_shape=shape,
        )


@registry.misc("segment_comparison_match")
def segment_comparison_match(ent):
    return SegmentComparison.segment_comparison_match(ent)
