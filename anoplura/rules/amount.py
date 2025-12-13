from dataclasses import dataclass

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base_rule import BaseRule, ForOutput


@dataclass(eq=False)
class Amount(BaseRule):
    # Class vars ----------
    # ---------------------

    amount: float = 0.0

    def for_output(self) -> ForOutput:
        return ForOutput(key="Amount", value=f"{self.amount:0.3f}")

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        # add.debug_tokens(nlp)  # #########################################
        add.trait_pipe(
            nlp,
            name="amount_patterns",
            compiler=cls.amount_patterns(),
            overwrite=["number"],
        )

        add.cleanup_pipe(nlp, name="amount_cleanup")

    @property
    def dimensions(self) -> tuple[str, ...]:
        return tuple(d.dim for d in self.dims if d.dim)

    @classmethod
    def amount_patterns(cls) -> list[Compiler]:
        decoder = {
            "99": {"ENT_TYPE": "number"},
        }
        return [
            Compiler(
                label="amount",
                on_match="amount_match",
                decoder=decoder,
                patterns=[
                    "99+",
                ],
            ),
        ]

    @classmethod
    def amount_match(cls, ent: Span) -> "Amount":
        num = next(e for e in ent.ents)
        return cls.from_ent(ent, amount=num._.trait.number)


@registry.misc("amount_match")
def amount_match(ent: Span) -> Amount:
    return Amount.amount_match(ent)
