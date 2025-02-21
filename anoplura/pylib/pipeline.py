import spacy
from traiter.pylib.pipeline import tokenizer
from traiter.pylib.pipes import extensions
from traiter.pylib.rules.number import Number

from anoplura.pylib.rules.range import Range
from anoplura.pylib.rules.seta import Seta
from anoplura.pylib.rules.seta_count import SetaCount
from anoplura.pylib.rules.taxon import Taxon


def build():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner", "lemmatizer", "tok2vec"])

    tokenizer.setup_tokenizer(nlp)

    # nlp.add_pipe("sentencizer", before="parser")

    Taxon.pipe(nlp)

    Seta.pipe(nlp)

    Number.pipe(nlp)
    Range.pipe(nlp)

    SetaCount.pipe(nlp)

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp
