from dataclasses import dataclass

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.pylib import roman
from anoplura.rules.base_rule import BaseRule


@dataclass(eq=False)
class Roman(BaseRule):
    number: int | None = None
    is_roman: bool = True

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.trait_pipe(
            nlp,
            name="roman_patterns",
            compiler=cls.roman_patterns(),
        )

    @classmethod
    def roman_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="roman",
                on_match="roman_match",
                decoder={
                    "iv": {"LOWER": {"REGEX": roman.LENIENT_PATTERN}},
                },
                patterns=[
                    " iv ",
                ],
            ),
        ]

    @classmethod
    def roman_match(cls, ent: Span) -> "Roman":
        number = roman.from_roman(ent.text)
        return cls.from_ent(ent, number=number)


@registry.misc("roman_match")
def roman_match(ent: Span) -> Roman:
    return Roman.roman_match(ent)
