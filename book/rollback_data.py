"""The general rollback and safety guidance, printed as a page of its own.

Every Move carries its own `## Rollback` section; verify.py refuses to build a
Move that does not name a point of no return, and refuses one that moves
persistent state without saying how the state comes back. This module holds the
rules behind all of those notes, shared by the book and the website so the two
cannot drift.

This is the most important page in the book. Everything else costs money when it
goes wrong; this costs data.
"""

INTRO = (
    'Every Move in this book changes something that is running. Most are reversible '
    'for a stated window, a few are reversible only until a particular step, and '
    'three are not reversible at all. The difference between a migration and an '
    'incident is almost never the technique - it is whether somebody worked out the '
    'way back before they started, and whether anybody had ever tested it.'
)

POINTS = [
    ('Read the rollback first',
     'Not the runbook. The Rollback section of every Move names the point of no '
     'return: the step after which the old system can no longer serve traffic or no '
     'longer holds current data. Read it, decide whether you are willing to reach '
     'that step today, and only then start at step one.'),

    ('A backup nobody restored is not a backup',
     'It is a file. Before any Move in Part II, restore the backup you are relying on '
     'into a scratch environment and count the rows against production. The number of '
     'organisations that discover their backups were empty during the incident that '
     'needed them is not small, and every one of them had a green dashboard.'),

    ('Keep the old thing running, and keep paying for it',
     'The instinct after a successful cutover is to delete the source and book the '
     'saving. Do not. The Reversible field on each Move is how long the old system '
     'must stay warm, powered and receiving its own backups. That overlap is the '
     'entire cost of being wrong, and it is cheap.'),

    ('Cut over when you can undo it, not when you are confident',
     'Confidence is not evidence. The right time to move traffic is when the rollback '
     'has been rehearsed end to end, on the same day of the week, with the same people '
     'awake. A Tuesday morning with the team at their desks beats a Saturday night '
     'with one person and a laptop, every time.'),

    ('Write down the state you cannot recreate',
     'Before Part II, list every store whose contents exist nowhere else: the primary '
     'database, the uploads bucket, the secrets, the certificate private keys, the '
     'TOTP seeds for the accounts that own the domain. Everything else is rebuildable '
     'from a repository. That list is short, and it is the only part of the estate '
     'where a mistake is permanent.'),

    ('Verify by counting, not by looking',
     'A migration is finished when the destination answers the same questions as the '
     'source with the same answers. Row counts, checksums, a replayed hour of real '
     'traffic compared response by response. A page that loads is not evidence, and '
     'neither is an application that starts.'),

    ('Two people, one keyboard',
     'Every High-risk Move in this book assumes a second person who is not typing, is '
     'reading the runbook aloud, and has the authority to stop. It is the cheapest '
     'safety control in infrastructure and the first one teams drop when they are '
     'behind schedule.'),

    ('Stop when you are surprised',
     'Not when something breaks - when something is merely unexpected. A row count '
     'that is off by eleven, a certificate with the wrong issuer, a replica that '
     'caught up faster than it should have. Surprise means the model in your head and '
     'the system in front of you have diverged, and continuing is guessing.'),
]

DISCLAIMER = (
    'These are operational practices, not a warranty. The runbooks in this book were '
    'written against the services and versions named in each Move and will drift as '
    'those change. Rehearse every Move against a copy of your own estate before you '
    'run it against the real one, and treat any figure here as the shape of an answer '
    'rather than a quotation for your account.'
)
