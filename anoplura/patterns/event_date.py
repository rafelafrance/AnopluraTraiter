"""Parse date notations."""
# import spacy
# from dateutil import parser
#
# COLLECTION_DATE = [
#     {
#         'label': 'event_date',
#         'on_match': 'event_date.v1',
#         'patterns': [
#             [
#                 {'LIKE_NUM': True},
#                 {'ENT_TYPE': 'month'},
#                 {'LIKE_NUM': True},
#             ]
#         ]
#     },
# ]
#
#
# @spacy.registry.misc(COLLECTION_DATE[0]['on_match'])
# def event_date(span):
#     """Enrich the match with data."""
#     data = {}
#
#     if not (value := parser.parse(span.text)):
#         return {}
#
#     data['date'] = value.isoformat()[:10]
#     return data
