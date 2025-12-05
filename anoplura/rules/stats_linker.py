from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.const as t_const
from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add, reject_match
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class StatsLinker(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "dimension_terms.csv",
        Path(__file__).parent / "terms" / "separator_terms.csv",
        Path(__file__).parent / "terms" / "specimen_type_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    stats: ClassVar[set[str]] = {
        "dimension",
        "mean",
        "measure",
        "range",
        "sample_size",
        "size",
        "size_range",
        "specimen_type",
    }
    # ---------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="part_stats_terms", path=cls.terms)
        add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="part_stats_patterns",
            compiler=cls.part_stats_patterns(),
        )
        add.cleanup_pipe(nlp, name="part_stats_cleanup")

    @classmethod
    def part_stats_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="part_stats",
                on_match="part_stats_match",
                decoder={
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    ",": {"ENT_TYPE": "separator"},
                    "dim": {"ENT_TYPE": "dimension"},
                    "of": {"ENT_TYPE": "linker"},
                    "measure": {"ENT_TYPE": "measure"},
                    "mean": {"ENT_TYPE": "mean"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "range": {"ENT_TYPE": "size_range"},
                    "sample": {"ENT_TYPE": "sample_size"},
                    "size": {"ENT_TYPE": "size"},
                    "type": {"ENT_TYPE": "specimen_type"},
                },
                patterns=[
                    " measure* dim* part+ size+ ,* (? mean+ ,* (? sample+ )? ",
                    " part+ ,* measure* dim* size+ (? sample+ )? ",
                    " measure* dim* of* part+ ,* size+ ",
                    " part+ dim* of* type* ,* size+ ,* mean+ ,* range* (? sample+ )? ",
                ],
            ),
        ]

    @classmethod
    def part_stats_match(cls, ent: Span) -> "StatsLinker":
        part = next(e._.trait for e in ent.ents if e.label_ in PARTS)
        stats = [e._.trait for e in ent.ents if e.label_ in cls.stats]

        for stat in stats:
            part.link(stat)

        mean = next((e._.trait for e in ent.ents if e.label_ == "mean"), None)
        size = next((e._.trait for e in ent.ents if e.label_ == "size"), None)
        dim = next((e._.trait for e in ent.ents if e.label_ == "dim"), None)

        if dim and size:
            size.dims[0].dim = dim.dimension

        if mean and size:
            mean.mean[0].dim = size.dims[0].dim

        raise reject_match.SkipTraitCreation


@registry.misc("part_stats_match")
def part_stats_match(ent: Span) -> StatsLinker:
    return StatsLinker.part_stats_match(ent)
