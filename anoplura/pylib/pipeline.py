import spacy
from traiter.pylib.pipes import extensions, tokenizer
from traiter.pylib.rules.number import Number

from anoplura.rules.range import Range
from anoplura.rules.seta import Seta
from anoplura.rules.seta_count import SetaCount
from anoplura.rules.sex import Sex
from anoplura.rules.taxon import Taxon


def build():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner", "lemmatizer", "tok2vec"])

    tokenizer.setup_tokenizer(nlp)

    Taxon.pipe(nlp)
    Sex.pipe(nlp)

    Seta.pipe(nlp)

    Number.pipe(nlp)
    Range.pipe(nlp)

    SetaCount.pipe(nlp)

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp
