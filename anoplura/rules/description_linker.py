from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add, reject_match
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base_rule import ANY_PART, BaseRule


@dataclass(eq=False)
class DescriptionLinker(BaseRule):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    descr: ClassVar[list[str]] = [
        "group",
        "morphology",
        "position",
        "relative_position",
        "relative_size",
        "shape",
        "size_description",
    ]
    all_descr: ClassVar[list[str]] = [*descr, "group_prefix"]
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="description_linker_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.context_pipe(
            nlp,
            name="description_linker_patterns",
            compiler=cls.description_linker_patterns(),
        )
        add.cleanup_pipe(nlp, name="description_linker_cleanup")

    @classmethod
    def description_linker_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="description_linker",
                on_match="description_linker_match",
                decoder={
                    "(": {"TEXT": {"IN": t_const.OPEN}},
                    ")": {"TEXT": {"IN": t_const.CLOSE}},
                    "all_descr": {"ENT_TYPE": {"IN": cls.all_descr}},
                    "any_part": {"ENT_TYPE": {"IN": ANY_PART}},
                    "desc": {"ENT_TYPE": {"IN": cls.descr}},
                    "group": {"ENT_TYPE": "group"},
                    "linker": {"ENT_TYPE": "linker"},
                    "prefix": {"ENT_TYPE": "group_prefix"},
                    "junk": {"POS": {"IN": ["PRON", "VERB"]}},
                    "pos": {"ENT_TYPE": {"IN": ["position", "relative_position"]}},
                    "sep": {"ENT_TYPE": {"IN": ["separator", "linker"]}},
                    "size": {"ENT_TYPE": {"IN": ["size_description", "relative_size"]}},
                },
                patterns=[
                    " (? any_part+ )? sep* junk? desc+ ",
                    " all_descr+ any_part+ pos+ group* ",
                    " all_descr+ any_part+ group+ ",
                    " all_descr+ linker? any_part+ ",
                    " any_part+ desc+ sep+ pos+ ",
                    " any_part+ desc+ linker+ pos+ ",
                    " any_part+ size+ sep+ size+ ",
                    " (? desc+ )? any_part+ ",
                    " all_descr+ sep* all_descr+ any_part+ ",
                ],
            ),
        ]

    @classmethod
    def description_linker_match(cls, span: Span) -> Never:
        descr = [e._.trait for e in span.ents if e.label_ in cls.all_descr]
        part = next(e._.trait for e in span.ents if e.label_ in ANY_PART)

        for d in descr:
            part.link(d)

        raise reject_match.SkipTraitCreation


@registry.misc("description_linker_match")
def description_linker_match(ent: Span) -> DescriptionLinker:
    return DescriptionLinker.description_linker_match(ent)
