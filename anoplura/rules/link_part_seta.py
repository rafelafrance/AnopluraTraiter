from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add, reject_match
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class LinkPartSeta(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    others: ClassVar[list[str]] = ["seta_count", "linker"]
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="link_part_seta_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="link_part_seta_patterns",
            compiler=cls.link_part_seta_patterns(),
            overwrite=["seta"],
        )
        add.cleanup_pipe(nlp, name="link_part_seta_cleanup")

    @classmethod
    def link_part_seta_patterns(cls):
        return [
            Compiler(
                label="link_part_seta",
                on_match="link_part_seta_match",
                decoder={
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "other": {"ENT_TYPE": {"IN": cls.others}},
                    "seta": {"ENT_TYPE": "seta"},
                },
                patterns=[
                    " part+ other* seta+ ",
                ],
            ),
        ]

    @classmethod
    def link_part_seta_match(cls, ent):
        part, which, seta = None, None, None

        for e in ent.ents:
            if e.label_ in PARTS:
                part = e._.trait.part
                which = e._.trait.which
            elif e.label_ == "seta":
                seta = e._.trait

        seta.part = part
        seta.which = which
        raise reject_match.SkipTraitCreation


@registry.misc("link_part_seta_match")
def link_part_seta_match(ent):
    return LinkPartSeta.link_part_seta_match(ent)
