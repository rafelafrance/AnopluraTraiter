from anoplura.pylib import pipeline, util

PIPELINE = pipeline.build()


def parse(text: str) -> list:
    text = util.shorten(text)
    doc = PIPELINE(text)

    traits = [e._.trait for e in doc.ents]

    from pprint import pp

    pp(traits)

    return traits


def unlinked(text: str) -> list:
    text = util.shorten(text)
    doc = PIPELINE(text)

    traits = [e._.trait for e in doc._.unlinked]

    # from pprint import pp
    # pp(traits)

    return traits
