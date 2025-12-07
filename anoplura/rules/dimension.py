from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base_rule import BaseRule, ForOutput


@dataclass(eq=False)
class Dimension(BaseRule):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "dimension_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ---------------------

    dimension: str = ""

    def for_output(self) -> ForOutput:
        return ForOutput(key="Dimension", value=self.dimension)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="dimension_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="dimension_patterns",
            compiler=cls.dimension_patterns(),
            overwrite=["dimension"],
        )
        add.cleanup_pipe(nlp, name="dimension_cleanup")

    @classmethod
    def dimension_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="dimension",
                on_match="dimension_match",
                decoder={
                    "dimension": {"ENT_TYPE": "dimension"},
                },
                patterns=[
                    " dimension* ",
                ],
            ),
        ]

    @classmethod
    def dimension_match(cls, ent: Span) -> "Dimension":
        dim = ""
        for sub_ent in ent.ents:
            if sub_ent.label_ == "dimension":
                dim = sub_ent.text.lower()
                dim = cls.replace.get(dim, dim)
        return cls.from_ent(ent, dimension=dim)


@registry.misc("dimension_match")
def dimension_match(ent: Span) -> Dimension:
    return Dimension.dimension_match(ent)
