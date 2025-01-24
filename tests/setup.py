from traiter.pylib.util import compress

from anoplura.pylib import pipeline

PIPELINE = pipeline.build()


def parse(text: str) -> list:
    text = compress(text)
    doc = PIPELINE(text)

    return [e._.trait for e in doc.ents]
