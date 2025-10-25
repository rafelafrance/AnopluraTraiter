from dataclasses import asdict, dataclass

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.rules.elevation import Elevation as T_Elevation

from anoplura.rules.base import Base, ForOutput


@dataclass(eq=False)
class Elevation(Base, T_Elevation):
    def for_output(self) -> ForOutput:
        about = "about " if self.about else ""
        text = f"Elevation: {about}{self.elevation:0.2f}"
        if self.elevation_high:
            text += f" - {self.elevation_high:0.2f}"
        text += f" {self.units}"
        return ForOutput(key="Elevation", value=text)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        T_Elevation.pipe(nlp)

    @classmethod
    def convert_super(cls, sup: T_Elevation) -> "Elevation":
        return cls(**asdict(sup))

    @classmethod
    def elevation_match(cls, ent: Span) -> "Elevation":
        sup = super().elevation_match(ent)
        return cls.convert_super(sup)


@registry.misc("elevation_match")
def elevation_match(ent: Span) -> Elevation:
    return Elevation.elevation_match(ent)
