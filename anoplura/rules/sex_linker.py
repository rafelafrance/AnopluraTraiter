from spacy import Language
from spacy.tokens import Doc

SEX_LINKER = "sex_linker"


def pipe(nlp: Language, *, name: str | None = None, skip: bool | None = None) -> None:
    name = name if name else SEX_LINKER

    if skip:
        skip = skip if isinstance(skip, list) else [skip]

    config = {"skip": skip}
    nlp.add_pipe(SEX_LINKER, name=name, config=config)


@Language.factory(SEX_LINKER)
class SexLinker:
    def __init__(self, nlp: Language, name: str, skip: list[str] | None) -> None:
        super().__init__()
        self.nlp = nlp
        self.name = name

        skip = set(skip) if skip else set()  # Don't assign a sex to these traits
        skip |= {"sex"}
        skip |= {"taxon"}
        skip |= {"number", "range", "roman"}
        skip |= {"lat_long", "elevation"}
        skip |= {"position", "group"}
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
