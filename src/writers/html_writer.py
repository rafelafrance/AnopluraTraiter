"""Write output to an HTML file."""


def html_writer(_, rows):
    """Output the data."""
    for row in rows:
        print(row['path'])

        for sent in row['doc'].sents:
            print('=' * 80)
            print(sent)
            for ent in sent.ents:
                print(ent.label_, ent._.data)
            print()
