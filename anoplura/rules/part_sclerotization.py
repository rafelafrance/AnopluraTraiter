from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class PartSclerotization(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    sep: ClassVar[list[str]] = [",", "and"]
    # ----------------------

    amount_sclerotized: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="sclerotized_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="sclerotized_patterns",
            compiler=cls.sclerotized_patterns(),
            overwrite=["sclerotization"],
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
                    "part": {"ENT_TYPE": "part"},
                    "sclerotized": {"ENT_TYPE": "sclerotization"},
                    ",": {"LOWER": {"IN": cls.sep}},
                },
                patterns=[
                    "part+                   adv sclerotized",
                    "part+ ,* part+          adv sclerotized",
                    "part+ ,* part+ ,* part+ adv sclerotized",
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

        return cls.from_ent(ent, body_part=part, amount_sclerotized=amount)


@registry.misc("sclerotized_match")
def sclerotized_match(ent):
    return PartSclerotization.sclerotized_match(ent)
