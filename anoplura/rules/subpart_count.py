from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class SubpartCount(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "group_terms.csv"
    # ----------------------

    subpart: str | None = None
    count_low: int | None = None
    count_high: int | None = None
    description: str | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.trait_pipe(
            nlp,
            name="subpart_count_description",
            compiler=cls.subpart_count_description_patterns(),
            overwrite=["shape"],
        )
        add.context_pipe(
            nlp,
            name="subpart_count_patterns",
            compiler=cls.subpart_count_patterns(),
            overwrite=["count", "subpart_count_description", "shape"],
        )
        add.cleanup_pipe(nlp, name="subpart_count_cleanup")

    @classmethod
    def subpart_count_description_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="subpart_count_description",
                is_temp=True,
                on_match="subpart_count_description_match",
                decoder={
                    "descr": {"POS": {"IN": ["ADP", "ADJ", "ADV", "NOUN"]}},
                    "shape": {"ENT_TYPE": "shape"},
                },
                patterns=[" shape* descr+ shape* "],
            ),
        ]

    @classmethod
    def subpart_count_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="subpart_count",
                on_match="subpart_count_match",
                decoder={
                    "99": {"ENT_TYPE": "count"},
                    "descr": {"ENT_TYPE": "subpart_count_description"},
                    "subpart": {"ENT_TYPE": "subpart"},
                },
                patterns=[
                    " 99+ descr* subpart+ ",
                ],
            ),
        ]

    @classmethod
    def subpart_count_description_match(cls, ent: Span) -> "SubpartCount":
        return cls.from_ent(ent)

    @classmethod
    def subpart_count_match(cls, ent: Span) -> "SubpartCount":
        low, high, subpart = None, None, None
        descr = []

        for e in ent.ents:
            if e.label_ == "subpart":
                subpart = e._.trait.subpart
            elif e.label_ == "subpart_count_description":
                descr.append(e.text.lower())
            elif e.label_ == "shape":
                descr.append(e._.trait.shape)
            elif e.label_ == "count":
                low = e._.trait.count_low
                high = e._.trait.count_high

        descr = " ".join(descr) if descr else None

        return cls.from_ent(
            ent,
            subpart=subpart,
            count_low=low,
            count_high=high,
            description=descr,
        )


@registry.misc("subpart_count_description_match")
def subpart_count_description_match(ent: Span) -> SubpartCount:
    return SubpartCount.subpart_count_description_match(ent)


@registry.misc("subpart_count_match")
def subpart_count_match(ent: Span) -> SubpartCount:
    return SubpartCount.subpart_count_match(ent)
