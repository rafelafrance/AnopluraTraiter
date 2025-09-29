from dataclasses import dataclass

from spacy.language import Language
from traiter.rules.date_ import Date as T_Date

from anoplura.rules.base import Base


@dataclass(eq=False)
class Date(Base, T_Date):
    @classmethod
    def pipe(cls, nlp: Language) -> None:
        T_Date.pipe(nlp)
