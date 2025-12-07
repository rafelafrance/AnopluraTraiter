from dataclasses import asdict, dataclass

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.rules.date_ import Date as T_Date

from anoplura.rules.rule import ForOutput, Rule


@dataclass(eq=False)
class Date(Rule, T_Date):
    def for_output(self) -> ForOutput:
        text = "Date: "
        text += self.date if self.date else ""
        if self.century_adjust:
            text += ", century adjusted"
        if self.missing_day:
            text += ", missing day"
        return ForOutput(key="Date", value=text)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        T_Date.pipe(nlp)

    @classmethod
    def date_match(cls, ent: Span) -> "Date":
        sup = super().date_match(ent)
        return cls(**asdict(sup))

    @classmethod
    def short_date(cls, ent: Span) -> "Date":
        sup = super().short_date(ent)
        return cls(**asdict(sup))


@registry.misc("date_match")
def date_match(ent: Span) -> Date:
    return Date.date_match(ent)


@registry.misc("short_date_match")
def short_date_match(ent: Span) -> Date:
    return Date.short_date(ent)
