from dataclasses import dataclass

from spacy.language import Language
from traiter.rules.elevation import Elevation as T_Elevation


@dataclass(eq=False)
class Elevation(T_Elevation):
    sex: str | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        T_Elevation.pipe(nlp)
