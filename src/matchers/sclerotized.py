"""Extract sclerotized annotations."""

# from ..util import ATTACH_STEP, TRAIT_STEP


# def sclerotized(span):
#     """Enrich the match."""
#     data = {}
#     for token in span:
#         if token.ent_type_ == 'sclerotin':
#             pass
#         else:
#             data['sclerotized'] = token.lower_
#     return data


# def sclerotized_part(span):
#     """Enrich the match."""
#     data = {}
#     seg = ''
#     for token in span:
#         label = token.ent_type_
#         if label == 'sclerotized':
#             data['sclerotized'] = token._.data['sclerotized']
#         elif label == 'body_part':
#             data['body_part'] = token._.data['body_part']
#         elif label == 'segment':
#             seg = token.lower_
#         elif label == 'group':
#             data['group'] = token.lower_
#
#     if seg and not isinstance(data['part'], list):
#         data['body_part'] += ' ' + seg
#
#     return data


# SCLEROTIZED = {
#     TRAIT_STEP: [
#         {
#             'label': 'sclerotized',
#             'on_match': sclerotized,
#             'patterns': [
#                 [
#                     {'POS': 'ADV'},
#                     {'ENT_TYPE': 'sclerotin'},
#                 ],
#             ],
#         },
#     ],
#     ATTACH_STEP: [
#         {
#             'label': 'sclerotized_part',
#             'on_match': sclerotized_part,
#             'patterns': [
#                 [
#                     {'ENT_TYPE': 'segment', 'OP': '?'},
#                     {'ENT_TYPE': 'body_part'},
#                     {'ENT_TYPE': 'segment', 'OP': '?'},
#                     {'ENT_TYPE': '', 'OP': '*'},
#                     {'ENT_TYPE': 'group', 'OP': '?'},
#                     {'ENT_TYPE': '', 'OP': '*'},
#                     {'ENT_TYPE': 'sclerotized'},
#                 ],
#                 [
#                     {'ENT_TYPE': 'sclerotized'},
#                     {'ENT_TYPE': '', 'OP': '*'},
#                     {'ENT_TYPE': 'group', 'OP': '?'},
#                     {'ENT_TYPE': '', 'OP': '*'},
#                     {'ENT_TYPE': 'segment', 'OP': '?'},
#                     {'ENT_TYPE': 'body_part'},
#                     {'ENT_TYPE': 'segment', 'OP': '?'},
#                 ],
#             ],
#         },
#     ],
# }
