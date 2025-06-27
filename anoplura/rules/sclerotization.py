from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Sclerotization(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    # ----------------------

    amount_sclerotized: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="sclerotized_patterns",
            compiler=cls.sclerotized_patterns(),
            overwrite=["part"],
        )
        add.cleanup_pipe(nlp, name="sclerotized_cleanup")

    @classmethod
    def sclerotized_patterns(cls):
        return [
            Compiler(
                label="sclerotized",
                on_match="sclerotized_match",
                decoder={
                    "adv": {"POS": "ADV"},
                    "sclerotized": {"ENT_TYPE": "sclerotization"},
                },
                patterns=[
                    "adv sclerotized",
                ],
            ),
        ]

    @classmethod
    def sclerotized_match(cls, ent):
        part = []
        for sub_ent in ent.ents:
            if sub_ent.label_ == "part":
                text = sub_ent.text.lower()
                part.append(cls.replace.get(text, text))

        amount = next((t.lower_ for t in ent if t.pos_ == "ADV"), None)

        return cls.from_ent(ent, part=part, amount_sclerotized=amount)


@registry.misc("sclerotized_match")
def sclerotized_match(ent):
    return Sclerotization.sclerotized_match(ent)
