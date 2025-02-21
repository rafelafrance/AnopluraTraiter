import spacy
from traiter.pylib.pipeline import tokenizer
from traiter.pylib.pipes import extensions

from anoplura.pylib.rules.setae import Setae
from anoplura.pylib.rules.taxon import Taxon


def build():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner", "lemmatizer", "tok2vec"])

    tokenizer.setup_tokenizer(nlp)

    # nlp.add_pipe("sentencizer", before="parser")

    Taxon.pipe(nlp)
    Setae.pipe(nlp)

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp
