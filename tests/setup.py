from traiter.pylib import pipeline
from traiter.pylib.util import compress

PIPELINE = pipeline.build()


def parse(text: str) -> list:
    text = compress(text)
    doc = PIPELINE(text)

    return [e._.trait for e in doc.ents]
