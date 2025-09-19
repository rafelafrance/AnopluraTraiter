from dataclasses import dataclass

from spacy.language import Language
from traiter.rules.date_ import Date as T_Date


@dataclass(eq=False)
class Date(T_Date):
    @classmethod
    def pipe(cls, nlp: Language) -> None:
        T_Date.pipe(nlp)
