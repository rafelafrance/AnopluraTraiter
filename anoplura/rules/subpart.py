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
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    subpart: str | None = None
    part: str | list[str] = None
    which: str | list[str] | list[int] | None = None
    position: str | None = None
    group: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="subpart_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="subpart_patterns",
            compiler=cls.subpart_patterns(),
            overwrite=["bug_subpart"],
        )
        add.cleanup_pipe(nlp, name="subpart_cleanup")

    @classmethod
    def subpart_patterns(cls):
        return [
            Compiler(
                label="subpart",
                on_match="subpart_match",
                decoder={
                    "fill": {"POS": {"IN": ["ADJ", "ADP"]}},
                    "group": {"ENT_TYPE": "group"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "pos": {"ENT_TYPE": "position"},
                    "subpart": {"ENT_TYPE": "bug_subpart"},
                },
                patterns=[
                    " subpart+ ",
                    " pos* part+ subpart+ group* ",
                    " part+ fill* pos* subpart+ group* ",
                ],
            ),
        ]

    @classmethod
    def subpart_match(cls, ent):
        subpart, part, which, pos, group = None, None, None, None, None

        for e in ent.ents:
            if e.label_ == "bug_subpart":
                subpart = e.text.lower()
            if e.label_ in PARTS:
                part = e._.trait.part
                which = e._.trait.which
            elif e.label_ == "position":
                pos = e._.trait.position
            elif e.label_ == "group":
                group = e._.trait.group

        return cls.from_ent(
            ent, subpart=subpart, part=part, which=which, position=pos, group=group
        )


@registry.misc("subpart_match")
def subpart_match(ent):
    return Subpart.subpart_match(ent)
