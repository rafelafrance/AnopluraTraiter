from spacy.language import Language
from spacy.tokens import Doc
from traiter.pipes import add, pipe_util


def pipe(nlp: Language, check: list[str]) -> None:
    config = {
        "check": check,
    }
    add.custom_pipe(nlp, "delete_unlinked", config=config)


@Language.factory("delete_unlinked")
class DeleteUnlinked:
    def __init__(
        self,
        nlp: Language,
        name: str,
        check: list[str],
    ) -> None:
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.check = check if check else []  # List of traits to check

    def __call__(self, doc: Doc) -> Doc:
        entities = []
        links = set()

        # Get links
        for ent in doc.ents:
            trait = ent._.trait
            if not trait.links:
                continue
            for link in trait.links:
                links.add(link.start)

        # Delete unlinked
        for ent in doc.ents:
            if ent.label_ in self.check and ent._.trait.start not in links:
                pipe_util.clear_tokens(ent)
                continue

            entities.append(ent)

        doc.ents = entities
        return doc
