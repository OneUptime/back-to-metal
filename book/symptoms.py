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
     '10 58 70 48'),
    ('Egress is now the largest line on the invoice',
     '06 17 44 46'),
    ('We are being rate-limited by a database we pay a fortune for',
     '11 61 10 54'),
    ('The finance director has asked what happens if we just left',
     '04 64 74 02'),
    ('Something has to move this quarter and nothing may break',
     '49 02 10 11'),
    ('We cannot get a straight answer about an outage we did not cause',
     '12 15 33 54'),
    ('A single availability zone took us down anyway',
     '43 50 59 57'),
    ('The container registry is throttling our deploys',
     '60 70 11 67'),
    ('Our secrets are in four places and one of them is a spreadsheet',
     '66 04 40 12'),
    ('We have no idea what would happen if the cluster were deleted',
     '62 03 30 15'),
    ('The audit is in eight weeks and the evidence lives in a console',
     '64 63 33 02'),
    ('Nobody wants to be on call for hardware',
     '48 39 19 26'),
    ('The monitoring bill is larger than the thing it monitors',
     '67 22 44 57'),
    ('We are locked into one database we cannot price-compare',
     '64 31 42 52'),
    ('Latency between our services is worse than it should be',
     '33 26 56 28'),
    ('We were told we cannot leave because of compliance',
     '50 29 41 27'),
    ('Half the estate is serverless and nobody knows what it costs',
     '18 64 45 06'),
    ('We want out but the CDN and the mail are non-negotiable',
     '09 36 22 15'),
    ('Someone has to hold an IP address we actually own',
     '58 61 36 28'),
    ('The migration stalled and we are now running two of everything',
     '53 49 67 64'),
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
