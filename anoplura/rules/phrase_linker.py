from copy import deepcopy
from dataclasses import dataclass
from typing import Never

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add, reject_match
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class PhraseLinker(Base):
    # Class vars ----------
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        # add.debug_tokens(nlp)  # #########################################
        add.context_pipe(
            nlp,
            name="phrase_linker_patterns",
            compiler=cls.phrase_linker_patterns(),
        )

    @classmethod
    def phrase_linker_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="phrase_linker",
                on_match="phrase_linker_match",
                decoder={
                    "size": {"ENT_TYPE": "size"},
                    "words": {"TEXT": {"NOT_IN": [".", ";", ":"]}},
                },
                patterns=[
                    " words+ size* ",
                ],
            ),
        ]

    @classmethod
    def phrase_linker_match(cls, span: Span) -> Never:
        for ent in span.ents:
            others = [deepcopy(e._.trait) for e in span.ents if e != ent]
            if others:
                for o in others:
                    o.links = None
                ent._.trait.links = others

        raise reject_match.SkipTraitCreation

    @classmethod
    def fill_others(
        cls, others: list[Base], part: str, which: str | list[str] | list[int]
    ) -> None:
        for other in others:
            if not other.part:
                other.part = part
                other.which = which


@registry.misc("phrase_linker_match")
def phrase_linker_match(ent: Span) -> PhraseLinker:
    return PhraseLinker.phrase_linker_match(ent)
