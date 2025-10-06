from dataclasses import dataclass

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.rules.elevation import Elevation as T_Elevation

from anoplura.rules.base import Base


@dataclass(eq=False)
class Elevation(Base, T_Elevation):
    def format(self) -> str:
        val = f"{self._trait}: {'~ ' if self.about else ''}{self.elevation:0.2f}"
        if self.elevation_high:
            val += f" - {self.elevation_high:0.2f}"
        if self.units:
            val += f" {self.units}"
        return val

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        T_Elevation.pipe(nlp)

    @classmethod
    def elevation_match(cls, ent: Span) -> "Elevation":
        return super().elevation_match(ent)


@registry.misc("elevation_match")
def elevation_match(ent: Span) -> Elevation:
    return Elevation.elevation_match(ent)
