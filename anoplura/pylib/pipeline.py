import spacy
from traiter.pylib.pipes import extensions, sentence, tokenizer

from anoplura.pylib.rules.setae import Setae
from anoplura.pylib.rules.taxon import Taxon


def build():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner", "lemmatizer", "tok2vec"])

    tokenizer.setup_tokenizer(nlp)

    nlp.add_pipe(sentence.SENTENCES, before="parser")

    Taxon.pipe(nlp)
    Setae.pipe(nlp)

    return nlp
