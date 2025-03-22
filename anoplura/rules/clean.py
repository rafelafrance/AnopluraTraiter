from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add


def pipe(nlp: Language, clean: list[str]):
    config = {"clean": clean}
    add.custom_pipe(nlp, "clean", config=config)


def clean_tokens(ent):
    if "" not in ent.doc.vocab.strings:
        ent.doc.vocab.strings.add("")
    ent.label = ent.doc.vocab.strings[""]
    for token in ent:
        token.ent_type = ent.doc.vocab.strings[""]
        token._.flag = ""
        token._.term = ""


@Language.factory("clean")
class Clean:
    def __init__(
        self,
        nlp: Language,
        name: str,
        clean: list[str],
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.clean = clean if clean else []  # List of traits to clean

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent.label_ in self.clean:
                clean_tokens(ent)
                continue

            entities.append(ent)

        doc.ents = entities
        return doc
