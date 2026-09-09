"""The real index: the way the question actually arrives.

Nobody sits down at nine in the morning thinking in stages. They think "the bill
went up forty per cent and nobody can say why". This maps the symptom to the
Moves that answer it, and it is printed as a page of its own and rendered on the
website's front page.

Each entry is (the symptom, a space-separated list of Move numbers). Every number
is checked against the built book, so a Move that is renumbered or removed turns
the build red rather than leaving a dead reference here.
"""

SYMPTOMS = [
    ('The bill went up and nobody can say why',
     '01 02 03'),
    ('Somebody has asked what would happen if we just left',
     '03 04 07'),
    ('Egress is now one of the largest lines on the invoice',
     '01 14 18'),
    ('The database costs more than the engineers who query it',
     '05 12 16'),
    ('We have no idea what we are actually running',
     '02 13 20'),
    ('We are being asked to do this and we have two engineers',
     '03 06 19'),
    ('The hardware sounds like a full-time job nobody has',
     '07 09 11'),
    ('Something has to move this quarter and nothing may break',
     '14 17 18'),
    ('We want remote hands to handle the hardware calls',
     '07 19 06'),
    ('We were told we cannot leave, and nobody has checked',
     '04 15 20'),
]


def check(moves):
    """Called through the build: every number here must be a real Move."""
    have = {m['num'] for m in moves}
    out = []
    for q, ns in SYMPTOMS:
        for n in ns.split():
            if n not in have:
                out.append(f'symptoms.py: "{q[:44]}" points at move {n}, '
                           f'which does not exist')
    return out
