from spacy.language import Language
from spacy.tokens import Doc

SEX_LINKER = "sex_linker"


def pipe(nlp: Language, *, name: str | None = None) -> None:
    name = name if name else SEX_LINKER
    nlp.add_pipe(SEX_LINKER, name=name)


@Language.factory(SEX_LINKER)
class SexLinker:
    def __init__(self, nlp: Language, name: str) -> None:
        super().__init__()
        self.nlp = nlp
        self.name = name

        skip = {"sex"}
        skip |= {"taxon"}
        skip |= {"date", "elevation", "lat_long"}
        self.skip = skip

    def __call__(self, doc: Doc) -> Doc:
        sex = ""
        for ent in doc.ents:
            if ent.label_ == "sex":
                sex = ent._.trait.sex
            elif ent._.trait.links and any(
                lk.trait == "sex" for lk in ent._.trait.links
            ):
                link = next(lk for lk in ent._.trait.links if lk.trait == "sex")
                ent._.trait.sex = link.sex
            elif sex and not ent._.trait.sex and ent.label_ not in self.skip:
                ent._.trait.sex = sex

        return doc
