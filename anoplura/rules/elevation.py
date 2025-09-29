from dataclasses import dataclass

from spacy.language import Language
from traiter.rules.elevation import Elevation as T_Elevation

from anoplura.rules.base import Base


@dataclass(eq=False)
class Elevation(Base, T_Elevation):
    @classmethod
    def pipe(cls, nlp: Language) -> None:
        T_Elevation.pipe(nlp)
