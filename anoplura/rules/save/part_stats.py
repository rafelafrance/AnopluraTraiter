from dataclasses import dataclass, field
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
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "dimension_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    sep: ClassVar[list[str]] = [",", "=", "is"]
    # ---------------------

    part: str | None = None
    part_dims: list[Dimension] = field(default_factory=list)
    specimen_type: str | None = None
    specimen_sex: str | None = None
    specimen_type_other: str | None = None
    part_mean: list[Dimension] = field(default_factory=list)
    part_range: list[Dimension] = field(default_factory=list)
    part_sample_size: list[Dimension] = field(default_factory=list)

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="part_stats_patterns",
            compiler=cls.part_stats_patterns(),
            overwrite=["part_size", "part_mean", "part_range", "part_sample"],
        )

    @classmethod
    def part_stats_patterns(cls):
        return [
            Compiler(
                label="part_stats",
                on_match="part_stats_match",
                decoder={
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    ",": {"LOWER": {"IN": cls.sep}},
                    "size": {"ENT_TYPE": "part_size"},
                    "mean": {"ENT_TYPE": "part_mean"},
                    "range": {"ENT_TYPE": "part_range"},
                    "sample": {"ENT_TYPE": "part_sample"},
                },
                patterns=[
                    " size+ ,* mean+ ,* range+ ,* (? sample+ )? ",
                ],
            ),
        ]

    @classmethod
    def part_stats_match(cls, ent):
        part = None
        part_dims = None
        specimen_type = None
        specimen_sex = None
        specimen_type_other = None
        part_mean = None
        part_range = None
        part_sample_size = None

        for e in ent.ents:
            if e.label_ == "part_size":
                part = e._.trait.part
                part_dims = e._.trait.part_dims
                specimen_type = e._.trait.specimen_type
                specimen_sex = e._.trait.specimen_sex
                specimen_type_other = e._.trait.specimen_type_other
            elif e.label_ == "part_mean":
                part_mean = e._.trait.part_mean
            elif e.label_ == "part_range":
                part_range = e._.trait.part_range
            elif e.label_ == "part_sample":
                part_sample_size = e._.trait.part_sample_size

        return cls.from_ent(
            ent,
            part=part,
            part_dims=part_dims,
            specimen_type=specimen_type,
            specimen_sex=specimen_sex,
            specimen_type_other=specimen_type_other,
            part_mean=part_mean,
            part_range=part_range,
            part_sample_size=part_sample_size,
        )


@registry.misc("part_stats_match")
def part_stats_match(ent):
    return PartStats.part_stats_match(ent)
