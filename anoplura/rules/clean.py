from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add


def pipe(nlp: Language, traits: list[str]):
    config = {"traits": traits}
    add.custom_pipe(nlp, "clean_traits", config=config)


def clean_tokens(ent):
    if "" not in ent.doc.vocab.strings:
        ent.doc.vocab.strings.add("")
    ent.label = ent.doc.vocab.strings[""]
    for token in ent:
        token.ent_type = ent.doc.vocab.strings[""]
        token._.flag = ""
        token._.term = ""


@Language.factory("clean_traits")
class CleanTraits:
    def __init__(
        self,
        nlp: Language,
        name: str,
        traits: list[str],
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.traits = traits if traits else []  # List of traits to clean

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent.label_ in self.traits:
                clean_tokens(ent)
                continue

            entities.append(ent)

        doc.ents = entities
        return doc
