"""The real index: the way the question actually arrives.

Nobody sits down at nine in the morning thinking in layers. They think "the bill
went up forty per cent and nobody can say why". This maps the symptom to the
Moves that answer it, and it is printed as a page of its own and rendered on the
website's front page.

Each entry is (the symptom, a space-separated list of Move numbers). Every number
is checked against the built book, so a Move that is renumbered or removed turns
the build red rather than leaving a dead reference here.
"""

SYMPTOMS = [
    ('The bill went up forty per cent and nobody can say why',
     '01 03 120 116'),
    ('Egress is now the largest line on the invoice',
     '93 53 94 105'),
    ('We are being rate-limited by a database we pay a fortune for',
     '71 73 47 09'),
    ('The finance director has asked what happens if we just left',
     '20 120 22 121'),
    ('Something has to move this quarter and nothing may break',
     '67 102 103 72'),
    ('We cannot get a straight answer about an outage we did not cause',
     '27 29 25 114'),
    ('A single availability zone took us down anyway',
     '24 115 42 75'),
    ('The container registry is throttling our deploys',
     '58 59 64 65'),
    ('Our secrets are in four places and one of them is a spreadsheet',
     '56 57 55 48'),
    ('We have no idea what would happen if the cluster were deleted',
     '52 115 65 74'),
    ('The audit is in eight weeks and the evidence lives in a console',
     '119 118 38 110'),
    ('Nobody wants to be on call for hardware',
     '113 110 111 22'),
    ('The monitoring bill is larger than the thing it monitors',
     '62 63 114 120'),
    ('We are locked into one database we cannot price-compare',
     '76 78 71 73'),
    ('Latency between our services is worse than it should be',
     '45 46 05 69'),
    ('We were told we cannot leave because of compliance',
     '119 27 35 118'),
    ('Half the estate is serverless and nobody knows what it costs',
     '89 66 68 90'),
    ('We want out but the CDN and the mail are non-negotiable',
     '105 107 106 116'),
    ('Someone has to hold an IP address we actually own',
     '91 96 94 104'),
    ('The migration stalled and we are now running two of everything',
     '120 121 103 116'),
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
