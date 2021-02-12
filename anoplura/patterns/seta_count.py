"""Extract setae count notations."""

import spacy
from traiter.patterns.matcher_patterns import MatcherPatterns

from anoplura.pylib.const import COMMON_PATTERNS, REPLACE

DECODER = COMMON_PATTERNS | {
    'seta': {'ENT_TYPE': 'seta'},
    'setae': {'ENT_TYPE': 'setae'},
    'seta_abbrev': {'ENT_TYPE': 'seta_abbrev'},
    'filler': {'POS': {'IN': ['ADP', 'ADJ']}},
    'group': {'ENT_TYPE': 'group'},
    '99': {'ENT_TYPE': 'integer'},
    'not_ent': {'ENT_TYPE': ''},
    'loc': {'ENT_TYPE': 'part_loc'},
    'part/loc': {'ENT_TYPE': {'IN': ['part_loc', 'body_part']}},
    'cconj': {'POS': 'CCONJ'},
}

SETAE = MatcherPatterns(
    'setae',
    decoder=DECODER,
    patterns=[
        'part* seta',
        'any_part+ seta',
    ],
)

SETAE_ABBREV = MatcherPatterns(
    'setae_abbrev',
    decoder=DECODER,
    patterns=['(? seta_abbrev )?'],
)

SETA_COUNT = MatcherPatterns(
    'seta_count',
    on_match='seta_count.v1',
    decoder=DECODER,
    patterns=[
        ' 99 not_ent? not_ent? setae seta_abbrev',
        ' 99 not_ent? not_ent? setae filler group ',
        ' 99 not_ent? not_ent? not_ent? not_ent? not_ent? setae ',
    ],
)

MULTIPLE_SETA = MatcherPatterns(
    'multiple_seta_count',
    on_match='multiple_seta_count.v1',
    decoder=DECODER,
    patterns=['99 not_ent? not_ent? cconj? 99 not_ent? not_ent? loc* part/loc? setae'],
)


@spacy.registry.misc(SETA_COUNT.on_match)
def seta_count(ent):
    """Enrich the match."""
    data = {'body_part': 'seta'}
    location = []

    for token in ent:
        label = token.ent_type_

        if label == 'setae':
            data['seta'] = REPLACE.get(token.lower_, token.lower_)

        elif label == 'integer':
            data = {**data, **token._.data}

        elif label == 'group':
            data['group'] = REPLACE.get(token.lower_, token.lower_)

    if data.get('count', data.get('low')) is None:
        data['present'] = True

    if location:
        data['type'] = ' '.join(location)

    ent._.data = data


@spacy.registry.misc(MULTIPLE_SETA.on_match)
def multiple_seta_count(ent):
    """Handle multiple setae in one match."""
    data = {'body_part': 'seta'}
    low, high = 0, 0

    for token in ent:
        label = token.ent_type_

        if label == 'setae':
            data['seta'] = REPLACE.get(token.lower_, token.lower_)

        elif label == 'integer':
            if token._.data.get('count'):
                low += token._.data['count']
            else:
                low += token._.data.get('low', 0)
                high += token._.data.get('high', 0)

        elif label == 'group':
            data['group'] = REPLACE.get(token.lower_, token.lower_)

    if high and low:
        data['low'] = low
        data['high'] = high
    else:
        data['count'] = low

    ent._.data = data
