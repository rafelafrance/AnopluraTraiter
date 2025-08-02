from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class PartCount(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "group_terms.csv"
    parts: ClassVar[list[str]] = ["sternite", "tergite"]
    # ----------------------

    part: str | None = None
    which: list[int] | None = None
    count_low: int | None = None
    count_high: int | None = None
    description: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="part_count_description",
            compiler=cls.part_count_description_patterns(),
            overwrite=["shape"],
        )
        add.context_pipe(
            nlp,
            name="part_count_patterns",
            compiler=cls.part_count_patterns(),
            overwrite=["count", "part_count_description", "shape"],
        )
        add.cleanup_pipe(nlp, name="part_count_cleanup")

    @classmethod
    def part_count_description_patterns(cls):
        return [
            Compiler(
                label="part_count_description",
                is_temp=True,
                on_match="part_count_description_match",
                decoder={
                    "descr": {"POS": {"IN": ["ADP", "ADJ", "ADV", "PUNCT", "NOUN"]}},
                    "shape": {"ENT_TYPE": "shape"},
                },
                patterns=[" shape* descr+ shape* "],
            ),
        ]

    @classmethod
    def part_count_patterns(cls):
        return [
            Compiler(
                label="part_count",
                on_match="part_count_match",
                decoder={
                    "99": {"ENT_TYPE": "count"},
                    "descr": {"ENT_TYPE": "part_count_description"},
                    "part": {"ENT_TYPE": {"IN": cls.parts}},
                },
                patterns=[
                    " 99+ descr* part+ ",
                ],
            ),
        ]

    @classmethod
    def part_count_description_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def part_count_match(cls, ent):
        low, high, part, which = None, None, None, None
        descr = []

        for e in ent.ents:
            if e.label_ in cls.parts:
                part = e._.trait.part
                which = e._.trait.which
            elif e.label_ == "part_count_description":
                descr.append(e.text.lower())
            elif e.label_ == "shape":
                descr.append(e._.trait.shape)
            elif e.label_ == "count":
                low = e._.trait.count_low
                high = e._.trait.count_high

        descr = " ".join(descr) if descr else None

        return cls.from_ent(
            ent,
            part=part,
            which=which,
            count_low=low,
            count_high=high,
            description=descr,
        )


@registry.misc("part_count_description_match")
def part_count_description_match(ent):
    return PartCount.part_count_description_match(ent)


@registry.misc("part_count_match")
def part_count_match(ent):
    return PartCount.part_count_match(ent)
