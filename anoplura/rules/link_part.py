from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add, reject_match
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class LinkPart(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    others: ClassVar[list[str]] = [
        "linker",
        "separator",
        "subpart",
        "part_morphology",
        "subpart_morphology",
        "seta",
        "seta_count",
        "seta_morphology",
    ]
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="link_part_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="link_part_patterns",
            compiler=cls.link_part_patterns(),
            overwrite=["seta"],
        )
        add.cleanup_pipe(nlp, name="link_part_cleanup")

    @classmethod
    def link_part_patterns(cls):
        return [
            Compiler(
                label="link_part",
                on_match="link_part_match",
                decoder={
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "other": {"ENT_TYPE": {"IN": cls.others}},
                },
                patterns=[
                    " part+ other+ ",
                ],
            ),
        ]

    @classmethod
    def link_part_match(cls, ent):
        part, which = None, None
        subparts, morphs, setae = [], [], []

        for e in ent.ents:
            if e.label_ in PARTS:
                part = e._.trait.part
                which = e._.trait.which
            elif e.label_ == "subpart":
                subparts.append(e._.trait)
            elif e.label_ == "subpart_morphology":
                morphs.append(e._.trait)
            elif e.label_ == "seta":
                setae.append(e._.trait)

        cls.fill_subparts(subparts, part, which)
        cls.fill_subpart_morphology(morphs, part, which)
        cls.fill_setae(setae, part, which)

        raise reject_match.SkipTraitCreation

    @classmethod
    def fill_subparts(cls, subparts, part, which):
        for subpart in subparts:
            if not subpart.part:
                subpart.part = part
                subpart.which = which

    @classmethod
    def fill_subpart_morphology(cls, morphs, part, which):
        for morph in morphs:
            if not morph.part:
                morph.part = part
                morph.which = which

    @classmethod
    def fill_setae(cls, setae, part, which):
        for seta in setae:
            if not seta.part:
                seta.part = part
                seta.which = which


@registry.misc("link_part_match")
def link_part_match(ent):
    return LinkPart.link_part_match(ent)
