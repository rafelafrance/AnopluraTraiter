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
        Path(__file__).parent / "terms" / "seta_terms.csv",
        Path(__file__).parent / "terms" / "shape_terms.csv",
        Path(__file__).parent / "terms" / "size_terms.csv",
    ]
    desc: ClassVar[list[str]] = [
        "morphology",
        "position",
        "rel_pos",
        "rel_size",
        "shape_term",
        "size_term",
    ]
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
            overwrite=["count", "number_suffix", "subpart", "seta", *PARTS],
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
                    "adv": {"POS": {"IN": ["ADV"]}},
                    "desc": {"ENT_TYPE": {"IN": cls.desc}},
                    "group": {"ENT_TYPE": "group"},
                    "linker": {"ENT_TYPE": "linker"},
                    "part_desc": {"ENT_TYPE": {"IN": ["seta", "subpart", *PARTS]}},
                    "pron": {"POS": {"IN": ["PRON"]}},
                    "rel": {"ENT_TYPE": {"IN": ["rel_pos", "rel_size"]}},
                    "sep": {"ENT_TYPE": "separator"},
                    "suffix": {"ENT_TYPE": "number_suffix"},
                    "verb": {"POS": "VERB"},
                },
                patterns=[
                    " 9+ -* suffix+ ",
                    # -----------------
                    " verb? adv* desc+ group* ",
                    " verb? adv* desc* group+ ",
                    " verb? adv* desc+ sep+ desc+ group* ",
                    " verb? adv* desc+ sep+ desc+ sep+ desc+ group* ",
                    # -----------------
                    " desc+ linker+ desc+ ",
                    " desc+ linker+ desc+ linker+ desc+ ",
                    " desc+ sep+    desc+ linker+ desc+ ",
                ],
            ),
        ]

    @classmethod
    def description_match(cls, ent: Span) -> "Description":
        return cls.from_ent(ent, description=ent.text.lower())


@registry.misc("description_match")
def description_match(ent: Span) -> Description:
    return Description.description_match(ent)
