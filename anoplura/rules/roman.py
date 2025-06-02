from dataclasses import dataclass

from spacy import registry
from spacy.language import Language
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.pylib import roman
from anoplura.rules.base import Base


@dataclass(eq=False)
class Roman(Base):
    # Class vars ----------
    # ---------------------

    number: int = None
    is_roman: bool = True

    @classmethod
    def pipe(cls, nlp: Language):
        add.trait_pipe(
            nlp,
            name="roman_patterns",
            compiler=cls.roman_patterns(),
        )

    @classmethod
    def roman_patterns(cls):
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
    def roman_match(cls, ent):
        number = roman.from_roman(ent.text)
        return cls.from_ent(ent, number=number)


@registry.misc("roman_match")
def roman_match(ent):
    return Roman.roman_match(ent)
