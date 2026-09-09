"""Existing runbook excerpts arranged as operator records in every edition.

Only headings and blank-record labels are new. Substantive text is selected
verbatim from the parsed Moves and attributed to its source section. Sentence
ranges are zero-based, end-exclusive; runbook step numbers are one-based.
"""
import re

HEADING = 'Operator worksheets'
INTRO = 'Runbook excerpts and space for observations.'
RECORD_FIELDS = ('Service / scope', 'Move / record reference',
                 'Date / time zone', 'Operator / reviewer')

# Each source is (Move, parsed field, step number or note label, first, stop).
TEMPLATES = [
    {
        'id': 'rehearsal-record',
        'title': 'Rehearsal record',
        'purpose': ('14', 'why', None, 0, 2),
        'fields': [
            ('Starting state', ('14', 'steps', 1, 1, 3)),
            ('Service checks', ('14', 'steps', 4, 1, 3)),
            ('Stop conditions', ('18', 'steps', 2, 0, 2)),
            ('Measured recovery', ('19', 'steps', 3, 2, 3)),
            ('Result and evidence', ('19', 'notes', 'Watch out', 0, 2)),
        ],
    },
    {
        'id': 'restore-proof',
        'title': 'Restore proof',
        'purpose': ('19', 'why', None, 0, 2),
        'fields': [
            ('PostgreSQL recovery copy', ('16', 'steps', 5, 0, 1)),
            ('Protection and keys', ('19', 'steps', 2, 3, 5)),
            ('PostgreSQL isolation and comparison', ('16', 'steps', 5, 1, 2)),
            ('PostgreSQL application and elapsed time', ('16', 'steps', 5, 2, 3)),
            ('Next drill', ('19', 'notes', 'Do it faster', 0, 2)),
        ],
    },
    {
        'id': 'cutover-decision',
        'title': 'Cutover decision',
        'purpose': ('18', 'why', None, 0, 1),
        'fields': [
            ('Proceed / hold / abort', ('18', 'steps', 2, 0, 2)),
            ('Readiness evidence', ('18', 'steps', 6, 0, 2)),
            ('PostgreSQL write authority', ('16', 'steps', 7, 0, 2)),
            ('PostgreSQL point of no return', ('16', 'rollback', None, 1, 3)),
            ('Old edge return window', ('18', 'steps', 9, 0, 4)),
        ],
    },
    {
        'id': 'operating-review',
        'title': 'Operating review',
        'purpose': ('19', 'steps', 6, 3, 4),
        'fields': [
            ('Invoices and period', ('03', 'steps', 2, 0, 2)),
            ('Retained services', ('03', 'steps', 5, 0, 3)),
            ('Hours and migration costs', ('03', 'steps', 4, 2, 4)),
            ('Health and capacity', ('19', 'steps', 4, 2, 3)),
            ('Escalation and handover', ('19', 'steps', 6, 1, 3)),
        ],
    },
]


def excerpt(by_number, source):
    number, field, item, start, stop = source
    move = by_number[number]
    if field == 'steps':
        text = move[field][item - 1]
        label = f'Runbook step {item}'
    elif field == 'notes':
        text = dict(move[field])[item]
        label = f"Operator's notes: {item}"
    else:
        text = move[field]
        label = {'why': 'Why this works', 'rollback': 'Rollback'}[field]
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', text)
    if not 0 <= start < stop <= len(sentences):
        raise ValueError(f'worksheet excerpt outside Move {number}, {label}')
    return {'text': ' '.join(sentences[start:stop]), 'move': number,
            'source': f'Move {number} · {label}'}


def records(moves):
    by_number = {m['num']: m for m in moves}
    return [
        {'id': template['id'], 'title': template['title'],
         'purpose': excerpt(by_number, template['purpose']),
         'fields': [{'label': label, **excerpt(by_number, source)}
                    for label, source in template['fields']]}
        for template in TEMPLATES
    ]
