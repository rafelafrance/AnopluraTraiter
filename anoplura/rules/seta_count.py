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
class SetaCount(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "size_terms.csv",
        Path(__file__).parent / "terms" / "shape_terms.csv",
        Path(__file__).parent / "terms" / "group_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    seta: str | None = None
    seta_part: str | None = None
    count_low: int | None = None
    count_high: int | None = None
    count_group: str | None = None
    description: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="seta_count_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="seta_count_description",
            compiler=cls.seta_count_description_patterns(),
            overwrite=["shape_term", "size_term", "group", "position"],
        )
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="seta_count_patterns",
            compiler=cls.seta_count_patterns(),
            overwrite=["count", "seta_count_description"],
        )
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="seta_count_patterns2",
            compiler=cls.seta_count_patterns2(),
            overwrite=["seta_count_description"],
        )
        add.cleanup_pipe(nlp, name="seta_count_cleanup")

    @classmethod
    def seta_count_description_patterns(cls):
        shapes = ["shape_term", "size_term", "position"]
        return [
            Compiler(
                label="seta_count_description",
                is_temp=True,
                on_match="seta_count_description_match",
                decoder={
                    "adv": {"POS": {"IN": ["ADV", "ADJ"]}},
                    "group": {"ENT_TYPE": "group"},
                    "shape": {"ENT_TYPE": {"IN": shapes}},
                },
                patterns=[
                    " adv? shape+ group* ",
                    " adv? shape* group+ ",
                ],
            ),
        ]

    @classmethod
    def seta_count_patterns(cls):
        return [
            Compiler(
                label="seta_count",
                on_match="seta_count_match",
                decoder={
                    "99": {"ENT_TYPE": "count"},
                    "descr": {"ENT_TYPE": "seta_count_description"},
                    "seta": {"ENT_TYPE": "seta"},
                },
                patterns=[
                    " 99+   seta+  descr* ",
                    " 99+   descr* seta+ ",
                    " seta+ 99+    descr* ",
                ],
            ),
        ]

    @classmethod
    def seta_count_patterns2(cls):
        return [
            Compiler(
                label="seta_count",
                on_match="seta_count_match2",
                decoder={
                    "99": {"ENT_TYPE": "seta_count"},
                    "descr": {"ENT_TYPE": "seta_count_description"},
                    "seta": {"ENT_TYPE": "seta"},
                },
                patterns=[
                    " 99+   seta+ descr+ ",
                    " seta+ 99+   descr+ ",
                ],
            ),
        ]

    @classmethod
    def seta_count_description_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def seta_count_match(cls, ent):
        seta, low, high, group, seta_part = None, None, None, None, None
        descr = []

        for e in ent.ents:
            if e.label_ == "count":
                low = e._.trait.count_low
                high = e._.trait.count_high
                group = e._.trait.count_group
            elif e.label_ == "seta":
                seta = e._.trait.seta
                seta_part = e._.trait.seta_part
            elif e.label_ == "seta_count_description":
                descr.append(e.text.lower())

        descr = " ".join(descr) if descr else None

        return cls.from_ent(
            ent,
            count_low=low,
            count_high=high,
            count_group=group,
            description=descr,
            seta=seta,
            seta_part=seta_part,
        )

    @classmethod
    def seta_count_match2(cls, ent):
        seta, low, high, group, seta_part = None, None, None, None, None
        descr = []

        for e in ent.ents:
            if e.label_ == "seta_count":
                low = e._.trait.count_low
                high = e._.trait.count_high
                group = e._.trait.count_group
            elif e.label_ == "seta":
                seta = e._.trait.seta
                seta_part = e._.trait.seta_part
            elif e.label_ == "seta_count_description":
                descr.append(e.text.lower())

        descr = " ".join(descr) if descr else None

        return cls.from_ent(
            ent,
            count_low=low,
            count_high=high,
            count_group=group,
            description=descr,
            seta=seta,
            seta_part=seta_part,
        )


@registry.misc("seta_count_description_match")
def seta_count_description_match(ent):
    return SetaCount.seta_count_description_match(ent)


@registry.misc("seta_count_match")
def seta_count_match(ent):
    return SetaCount.seta_count_match(ent)


@registry.misc("seta_count_match2")
def seta_count_match2(ent):
    return SetaCount.seta_count_match2(ent)
