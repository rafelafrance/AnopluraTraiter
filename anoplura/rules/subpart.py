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
class Subpart(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "position_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    subpart: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="subpart_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="subpart_patterns",
            compiler=cls.subpart_patterns(),
            overwrite=["part"],
        )
        add.cleanup_pipe(nlp, name="subpart_cleanup")

    @classmethod
    def subpart_patterns(cls):
        return [
            Compiler(
                label="subpart",
                on_match="subpart_match",
                decoder={
                    "adj": {"POS": "ADJ"},
                    "part": {"ENT_TYPE": "part"},
                    "subpart": {"ENT_TYPE": "bug_subpart"},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " subpart+ ",
                ],
            ),
        ]

    @classmethod
    def subpart_match(cls, ent):
        subpart = ent.text.lower()
        return cls.from_ent(ent, subpart=subpart)


@registry.misc("subpart_match")
def subpart_match(ent):
    return Subpart.subpart_match(ent)
