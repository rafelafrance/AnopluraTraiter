from spacy.language import Language
from spacy.tokens import Doc

CLEAN_COUNT = 0


def pipe(nlp: Language, traits: list[str]):
    global CLEAN_COUNT
    CLEAN_COUNT += 1
    config = {"traits": traits}
    nlp.add_pipe("clean_traits", name=f"clean_traits_{CLEAN_COUNT}", config=config)


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


def clean_tokens(ent):
    if "" not in ent.doc.vocab.strings:
        ent.doc.vocab.strings.add("")
    ent.label = ent.doc.vocab.strings[""]
    for token in ent:
        token.ent_type = ent.doc.vocab.strings[""]
        token._.flag = ""
        token._.term = ""
