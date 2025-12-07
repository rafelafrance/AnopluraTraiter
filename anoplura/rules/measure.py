from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.rule import ForOutput, Rule


@dataclass(eq=False)
class Measure(Rule):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "dimension_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ---------------------

    measure: str = ""

    def for_output(self) -> ForOutput:
        return ForOutput(key="Measure", value=self.measure.lower())

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="measure_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="measure_patterns",
            compiler=cls.measure_patterns(),
            overwrite=["measure"],
        )
        add.cleanup_pipe(nlp, name="measure_cleanup")

    @classmethod
    def measure_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="measure",
                on_match="measure_match",
                decoder={
                    "measure": {"ENT_TYPE": "measure"},
                },
                patterns=[
                    " measure+ ",
                ],
            ),
        ]

    @classmethod
    def measure_match(cls, ent: Span) -> "Measure":
        measure = ""
        for sub_ent in ent.ents:
            if sub_ent.label_ == "measure":
                measure = sub_ent.text.lower()
                measure = cls.replace.get(measure, measure)
        return cls.from_ent(ent, measure=measure)


@registry.misc("measure_match")
def measure_match(ent: Span) -> Measure:
    return Measure.measure_match(ent)
