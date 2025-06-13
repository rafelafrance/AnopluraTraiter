from spacy import Language
from spacy.tokens import Doc

SEX_ASSIGNMENT = "sex_assignment"


def pipe(nlp: Language, *, name: str, skip=None):
    if skip:
        skip = skip if isinstance(skip, list) else [skip]

    config = {"skip": skip}
    nlp.add_pipe(SEX_ASSIGNMENT, name=name, config=config)


@Language.factory(SEX_ASSIGNMENT)
class SexAssignment:
    def __init__(self, nlp: Language, name: str, skip: list[str]):
        super().__init__()
        self.nlp = nlp
        self.name = name

        self.skip = set(skip) if skip else set()  # Don't assign a sex to these traits
        skip |= {"range", "roman", "sex", "sex_count", "sexual_dimorphism", "taxon"}

    def __call__(self, doc: Doc) -> Doc:
        sex = ""
        for ent in doc.ents:
            if ent.label_ == "sex":
                sex = ent._.trait.sex
            elif sex and not ent._.trait.sex and ent.label_ not in self.skip:
                ent._.trait.sex = sex

        return doc
