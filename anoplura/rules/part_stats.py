from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.const as t_const
from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.pylib.dimension import Dimension
from anoplura.rules.base import Base


@dataclass(eq=False)
class PartStats(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "dimension_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    sep: ClassVar[list[str]] = [",", "=", ";", ":", "is", "of"]
    sep += t_const.OPEN + t_const.CLOSE
    # ---------------------

    measure: str | None = None
    mean: float | None = None
    mean_units: str | None = None
    sample_size: int | None = None
    range: Dimension | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="part_stats_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="part_stats_patterns",
            compiler=cls.part_stats_patterns(),
            overwrite=["part", "size", "part_mean", "part_sample"],
        )

    @classmethod
    def part_stats_patterns(cls):
        return [
            Compiler(
                label="part_stats",
                on_match="part_stats_match",
                decoder={
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    ",": {"LOWER": {"IN": cls.sep}},
                    "dim": {"ENT_TYPE": "dimension"},
                    "max": {"ENT_TYPE": "measure"},
                    "mean": {"ENT_TYPE": "part_mean"},
                    "part": {"ENT_TYPE": "part"},
                    "sample": {"ENT_TYPE": "part_sample"},
                    "size": {"ENT_TYPE": "size"},
                },
                patterns=[
                    " max+ part+ size+ ",
                    " max+ dim+ ,* part+ ,* size+ ",
                    " max+ part+ size+          ,* mean+ ,* sample+ )? ",
                    " max+ part+ size+          ,* sample+ )? ",
                    " part+ ,* max+ size+       ,* sample+ )? ",
                    " max+ part+ dim+ ,* size+  ,* mean+ ,* sample+ )? ",
                    " max+ part+ dim+ ,* size+  ,* sample+ )? ",
                ],
            ),
        ]

    @classmethod
    def part_stats_match(cls, ent):
        part, measure, mean, units, sample, range_ = None, None, None, None, None, None
        dim = None

        for e in ent.ents:
            if e.label_ == "part":
                part = e._.trait.part
            elif e.label_ == "measure":
                measure = e.text.lower()
            elif e.label_ == "size":
                range_ = e._.trait.dims[0]
            elif e.label_ == "part_mean":
                mean = e._.trait.mean
                units = e._.trait.units
            elif e.label_ == "part_sample":
                sample = e._.trait.sample_size
            elif e.label_ == "dimension":
                text = e.text.lower()
                dim = cls.replace.get(text, text)

        if dim:
            range_.dim = dim

        measure = f"{measure} {part} {range_.dim}"

        return cls.from_ent(
            ent,
            measure=measure,
            mean=mean,
            mean_units=units,
            sample_size=sample,
            range=range_,
        )


@registry.misc("part_stats_match")
def part_stats_match(ent):
    return PartStats.part_stats_match(ent)
