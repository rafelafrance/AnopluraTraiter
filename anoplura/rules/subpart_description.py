from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class SubpartDescription(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "size_terms.csv",
        Path(__file__).parent / "terms" / "shape_terms.csv",
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    other_parts: ClassVar[list[str]] = [
        "gonopods",
        "plates",
        "segments",
        "sternites",
        "tergites",
    ]
    # ----------------------

    subpart: str | None = None
    part: str | list[str] | None = None
    which: str | list[str] | list[int] | None = None
    position: str | None = None
    group: str | None = None
    shape: list[str] | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="subpart_description_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="subpart_descr_patterns",
            compiler=cls.subpart_descr_patterns(),
            overwrite=["shape_term", "size_term", "position", *cls.other_parts],
        )
        add.context_pipe(
            nlp,
            name="subpart_description_patterns",
            compiler=cls.subpart_description_patterns(),
            overwrite=["subpart_descr"],
        )
        add.context_pipe(
            nlp,
            name="subpart_description_patterns2",
            compiler=cls.subpart_description_patterns2(),
            overwrite=["subpart_descr"],
        )
        add.cleanup_pipe(nlp, name="subpart_description_cleanup")

    @classmethod
    def subpart_descr_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="subpart_descr",
                is_temp=True,
                on_match="subpart_descr_match",
                decoder={
                    "adj": {"POS": {"IN": ["ADJ", "ADV"]}},
                    "pos": {"ENT_TYPE": "position"},
                    "other_parts": {"ENT_TYPE": {"IN": cls.other_parts}},
                    "shape": {"ENT_TYPE": {"IN": ["shape_term", "size_term"]}},
                },
                patterns=[
                    " adj* pos+ ",
                    " adj* shape+ pos* ",
                    " adj* shape+ other_parts* ",
                ],
            ),
        ]

    @classmethod
    def subpart_description_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="subpart_description",
                on_match="subpart_description_match",
                decoder={
                    ",": {"ENT_TYPE": "separator"},
                    "subpart": {"ENT_TYPE": "subpart"},
                    "shape": {"ENT_TYPE": "subpart_descr"},
                },
                patterns=[
                    " shape+   subpart+ ",
                    " subpart+ shape+ ",
                    " subpart+ shape+ ,* shape+ ",
                ],
            ),
        ]

    @classmethod
    def subpart_description_patterns2(cls) -> list[Compiler]:
        return [
            Compiler(
                label="subpart_description",
                on_match="subpart_description_match2",
                decoder={
                    "other_descr": {"ENT_TYPE": "subpart_description"},
                    "descr": {"ENT_TYPE": "subpart_descr"},
                    "subpart": {"ENT_TYPE": "subpart"},
                },
                patterns=[
                    " other_descr+ subpart+ descr+ ",
                ],
            ),
        ]

    @classmethod
    def subpart_descr_match(cls, ent: Span) -> "SubpartDescription":
        return cls.from_ent(ent)

    @classmethod
    def subpart_description_match(cls, ent: Span) -> "SubpartDescription":
        subpart, part, which, pos, group = None, None, None, None, None
        descr = []

        for e in ent.ents:
            if e.label_ == "subpart":
                subpart = e._.trait.subpart
                part = e._.trait.part
                which = e._.trait.which
                pos = e._.trait.position
                group = e._.trait.group
            elif e.label_ == "subpart_descr":
                descr.append(e.text.lower())

        return cls.from_ent(
            ent,
            subpart=subpart,
            part=part,
            which=which,
            position=pos,
            group=group,
            shape=descr,
        )

    @classmethod
    def subpart_description_match2(cls, ent: Span) -> "SubpartDescription":
        subpart, part, which, pos, group = None, None, None, None, None
        descr = []

        for e in ent.ents:
            if e.label_ == "subpart":
                subpart = e._.trait.subpart
                part = e._.trait.part
                which = e._.trait.which
                pos = e._.trait.position
                group = e._.trait.group
            elif e.label_ == "subpart_descr":
                descr.append(e.text.lower())

        return cls.from_ent(
            ent,
            subpart=subpart,
            part=part,
            which=which,
            position=pos,
            group=group,
            shape=descr,
        )


@registry.misc("subpart_description_match")
def subpart_description_match(ent: Span) -> SubpartDescription:
    return SubpartDescription.subpart_description_match(ent)


@registry.misc("subpart_description_match2")
def subpart_description_match2(ent: Span) -> SubpartDescription:
    return SubpartDescription.subpart_description_match2(ent)


@registry.misc("subpart_descr_match")
def subpart_descr_match(ent: Span) -> SubpartDescription:
    return SubpartDescription.subpart_descr_match(ent)
