from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class Subpart(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "relative_terms.csv",
    ]
    dash: ClassVar[list[str]] = ["-", "–", "—"]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    subpart: str | None = None
    part: str | list[str] = None
    which: str | list[str] | list[int] | None = None
    position: str | None = None
    group: str | None = None
    description: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="subpart_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="subpart_subpart_suffix_patterns",
            compiler=cls.subpart_subpart_suffix_patterns(),
            overwrite=["number", "subpart_suffix"],
        )
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="subpart_patterns",
            compiler=cls.subpart_patterns(),
            overwrite=[
                "bug_subpart",
                "position",
                "group",
                "subpart_suffix",
                "relative_term",
            ],
        )
        add.cleanup_pipe(nlp, name="subpart_cleanup")

    @classmethod
    def subpart_subpart_suffix_patterns(cls):
        return [
            Compiler(
                label="subpart_suffix",
                is_temp=True,
                on_match="subpart_suffix_match",
                decoder={
                    "-": {"TEXT": {"IN": cls.dash}},
                    "9": {"ENT_TYPE": "number"},
                    "suffix": {"ENT_TYPE": "subpart_suffix"},
                },
                patterns=[
                    " 9 -+ suffix ",
                ],
            ),
        ]

    @classmethod
    def subpart_patterns(cls):
        return [
            Compiler(
                label="subpart",
                on_match="subpart_match",
                decoder={
                    "-": {"TEXT": {"IN": cls.dash}},
                    "fill": {"POS": {"IN": ["ADJ", "ADP"]}},
                    "group": {"ENT_TYPE": "group"},
                    "9": {"ENT_TYPE": "number"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "pos": {"ENT_TYPE": {"IN": ["position", "relative_term"]}},
                    "subpart": {"ENT_TYPE": "bug_subpart"},
                    "suffix": {"ENT_TYPE": "subpart_suffix"},
                },
                patterns=[
                    " pos* subpart+ group* ",
                    " pos* part+ subpart+ group* ",
                    " part+ fill* pos* subpart+ group* ",
                    " part+ suffix+ ",
                ],
            ),
        ]

    @classmethod
    def subpart_suffix_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def subpart_match(cls, ent):
        sub, part, which, group = None, None, None, None
        pos = []

        for e in ent.ents:
            if e.label_ == "bug_subpart":
                text = e.text.lower()
                sub = cls.replace.get(text, text)
            elif e.label_ in PARTS:
                part = e._.trait.part
                which = e._.trait.which
            elif e.label_ in ("position", "relative_term"):
                pos.append(e.text.lower())
            elif e.label_ == "group":
                group = e.text.lower()
            elif e.label_ == "subpart_suffix":
                sub = e.text.lower()

        pos = " ".join(pos) if pos else None

        return cls.from_ent(
            ent, subpart=sub, part=part, which=which, position=pos, group=group
        )


@registry.misc("subpart_suffix_match")
def subpart_suffix_match(ent):
    return Subpart.subpart_suffix_match(ent)


@registry.misc("subpart_match")
def subpart_match(ent):
    return Subpart.subpart_match(ent)
