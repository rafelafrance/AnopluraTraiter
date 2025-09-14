from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class Description(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "morphology_terms.csv",
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "separator_terms.csv",
        Path(__file__).parent / "terms" / "shape_terms.csv",
        Path(__file__).parent / "terms" / "size_terms.csv",
    ]
    descr: ClassVar[list[str]] = ["shape_term", "size_term", "position", "rel_pos"]
    dash: ClassVar[list[str]] = ["-", "–", "—"]
    # ----------------------

    description: str | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="description_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.trait_pipe(
            nlp,
            name="description_patterns",
            compiler=cls.description_patterns(),
            overwrite=["count", "number_suffix"],
        )
        add.cleanup_pipe(nlp, name="description_cleanup")

    @classmethod
    def description_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="description",
                on_match="description_match",
                decoder={
                    "-": {"TEXT": {"IN": cls.dash}},
                    "9": {"ENT_TYPE": "count"},
                    "adp": {"POS": {"IN": ["ADP"]}},
                    "adv": {"POS": {"IN": ["ADV"]}},
                    "descr": {"ENT_TYPE": {"IN": cls.descr}},
                    "group": {"ENT_TYPE": "group"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "sep": {"ENT_TYPE": {"IN": ["linker", "separator"]}},
                    "suffix": {"ENT_TYPE": "number_suffix"},
                    "morph": {"ENT_TYPE": "morphology"},
                    "pro": {"POS": "PRON"},
                    "verb": {"POS": "VERB"},
                },
                patterns=[
                    " descr+ group* ",
                    " descr* group+ ",
                    " 9+ -* suffix+ ",
                    " verb? descr+ sep* descr+ group* ",
                    " verb? descr+ sep* descr+ sep* descr+ group* ",
                    " verb? descr+ sep* descr* adp* descr+ group* ",
                    " verb? descr+ sep* descr* adp* descr+ group* ",
                    " verb? descr+ sep* verb?  adp* descr+ group* ",
                    " adv+  descr+ ",
                    " pro?  morph+ sep? verb? ",
                ],
            ),
        ]

    @classmethod
    def description_match(cls, ent: Span) -> "Description":
        return cls.from_ent(ent, description=ent.text.lower())


@registry.misc("description_match")
def description_match(ent: Span) -> Description:
    return Description.description_match(ent)
