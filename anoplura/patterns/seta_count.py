"""Extract seta count notations."""

import re

import spacy
from traiter.const import DASH_RE, INT_TOKEN_RE
from traiter.patterns.matcher_patterns import MatcherPatterns
from traiter.util import to_positive_int

from anoplura.pylib.const import COMMON_PATTERNS, MISSING, REPLACE

IS_INT = re.compile(INT_TOKEN_RE)
HAS_RANGE = re.compile(fr'[0-9]\s*({DASH_RE}|to)\s*[0-9]')

DECODER = COMMON_PATTERNS | {
    'seta': {'ENT_TYPE': 'seta'},
    'cheta': {'ENT_TYPE': 'cheta'},
    'seta_abbrev': {'ENT_TYPE': 'seta_abbrev'},
    'cheta_abbrev': {'ENT_TYPE': 'cheta_abbrev'},
    'filler': {'POS': {'IN': ['ADP', 'ADJ']}},
    'group': {'ENT_TYPE': 'group'},
    'not_ent': {'ENT_TYPE': ''},
    'nine': {'ENT_TYPE': 'number_word'},
    'loc': {'ENT_TYPE': 'part_loc'},
    'part/loc': {'ENT_TYPE': {'IN': ['part_loc', 'body_part']}},
    'cconj': {'POS': 'CCONJ'},
}

SETAE = MatcherPatterns(
    'seta',
    decoder=DECODER,
    patterns=[
        'part* cheta',
        'any_part+ cheta',
    ],
)

SETAE_ABBREV = MatcherPatterns(
    'seta_abbrev',
    decoder=DECODER,
    patterns=['(? cheta_abbrev )?'],
)

SETA_COUNT = MatcherPatterns(
    'setae_count',
    on_match='anoplura.seta_count.v1',
    decoder=DECODER,
    patterns=[
        'nine not_ent? not_ent? seta seta_abbrev',
        'nine not_ent? not_ent? seta filler group ',
        'missing not_ent? not_ent? seta seta_abbrev',
        'missing not_ent? not_ent? seta filler group ',
        'nine not_ent? not_ent? not_ent? not_ent? not_ent? seta ',
        '99 not_ent? not_ent? seta seta_abbrev',
        '99 not_ent? not_ent? seta filler group ',
        '99 not_ent? not_ent? not_ent? not_ent? not_ent? seta ',
        'group not_ent? not_ent? seta seta_abbrev?',
    ],
)

MULTIPLE_SETA = MatcherPatterns(
    'multiple_seta_count',
    on_match='anoplura.multiple_seta_count.v1',
    decoder=DECODER,
    patterns=[
        '99 -/to 99 not_ent? not_ent? loc* part/loc? seta',
        '99 not_ent? not_ent? not_ent? 99 not_ent? not_ent? loc* part/loc? seta',
        'nine not_ent? not_ent? not_ent? nine not_ent? not_ent? loc* part/loc? seta',
        ('99 -/to 99 not_ent? not_ent? loc* '
         'part/loc? seta not_ent? not_ent? group'),
        ('99 not_ent? not_ent? not_ent? 99 not_ent? not_ent? loc* '
         'part/loc? seta not_ent? not_ent? group'),
        ('nine not_ent? not_ent? not_ent? nine not_ent? not_ent? loc* '
         'part/loc? seta not_ent? not_ent? group'),
    ],
)


@spacy.registry.misc(SETA_COUNT.on_match)
def seta_count(ent):
    """Enrich the match."""
    data = {'body_part': 'seta'}
    location = []

    for token in ent:
        label = token._.cached_label

        if label == 'seta':
            data['seta'] = REPLACE.get(token.lower_, token.lower_)

        elif label == 'number_word':
            data['count'] = int(REPLACE.get(token.lower_, -1))

        elif token.lower_ in MISSING:
            data['count'] = 0

        elif label == 'group':
            data['group'] = token.lower_

        elif match := IS_INT.match(token.text):
            data['count'] = to_positive_int(match.group(0))

    if data.get('count', data.get('low')) is None:
        data['present'] = True

    if location:
        data['type'] = ' '.join(location)

    ent._.new_label = 'seta_count'
    ent._.data = data


@spacy.registry.misc(MULTIPLE_SETA.on_match)
def multiple_seta_count(ent):
    """Handle multiple seta in one match."""
    data = {'body_part': 'seta'}
    values = []

    for token in ent:
        label = token._.cached_label

        if label == 'seta':
            data['seta'] = REPLACE.get(token.lower_, token.lower_)

        elif label == 'number_word':
            values.append(to_positive_int(REPLACE.get(token.lower_)))

        elif match := IS_INT.match(token.text):
            value = to_positive_int(match.group(0))
            values.append(value)

        elif label == 'group':
            data['group'] = token.lower_

    if HAS_RANGE.search(ent.text.lower()):
        if len(values) == 2:
            data['low'] = min(values)
            data['high'] = max(values)
        else:
            data['count'] = values[0]
    else:
        data['count'] = sum(values)

    ent._.new_label = 'seta_count'

    ent._.data = data
