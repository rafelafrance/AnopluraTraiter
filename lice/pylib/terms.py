"""Get terms from various sources (CSV files or SQLite database."""

import csv
import sqlite3

from .util import DATA_DIR, VOCAB_DIR

TERM_PATH = VOCAB_DIR / 'terms.csv'
ITIS_DB = DATA_DIR / 'ITIS.sqlite'


def read_terms():
    """Read and cache the terms."""
    with open(TERM_PATH) as term_file:
        reader = csv.DictReader(term_file)
        return list(reader)


TERMS = read_terms()
REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}


def itis_terms(name, kingdom_id=5, rank_id=220, abbrev=False):
    """Get terms from the ITIS database.

    kingdom_id =   5 == Animalia
    rank_id    = 220 == Species
    """
    select_tsn = """ select tsn from taxonomic_units where unit_name1 = ?; """
    select_names = """
        select complete_name
          from hierarchy
          join taxonomic_units using (tsn)
         where hierarchy_string like ?
           and kingdom_id = ?
           and rank_id = ?;
           """

    with sqlite3.connect(ITIS_DB) as cxn:
        cursor = cxn.execute(select_tsn, (name, ))
        tsn = cursor.fetchone()[0]
        mask = f'%-{tsn}-%'
        taxa = {n[0].lower() for n in
                cxn.execute(select_names, (mask, kingdom_id, rank_id))}

    terms = []
    name = name.lower()
    for taxon in sorted(taxa):
        terms.append({
            'label': name,
            'pattern': taxon,
            'attr': 'lower',
            'replace': taxon,
        })
        if abbrev:
            words = taxon.split()
            if len(words) > 1:
                first, *rest = words
                first = first[0]
                rest = ' '.join(rest)
                terms.append({
                    'label': name,
                    'pattern': f'{first} . {rest}',
                    'attr': 'lower',
                    'replace': taxon,
                })

    return terms
