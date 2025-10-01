from dataclasses import dataclass

from spacy import registry
from spacy.tokens import Span
from traiter.rules.date_ import Date as T_Date

from anoplura.rules.base import Base


@dataclass(eq=False)
class Date(T_Date, Base):
    @classmethod
    def date_match(cls, ent: Span) -> "Date":
        return super().date_match(ent)

    @classmethod
    def short_date(cls, ent: Span) -> "Date":
        return super().short_date(ent)


@registry.misc("date_match")
def date_match(ent: Span) -> Date:
    return Date.date_match(ent)


@registry.misc("short_date_match")
def short_date_match(ent: Span) -> Date:
    return Date.short_date(ent)
