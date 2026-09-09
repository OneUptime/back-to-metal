"""The general rollback and safety guidance, printed as a page of its own.

Every Move carries its own `## Rollback` section; verify.py refuses to build a
Move that does not name a point of no return, and refuses one that moves
persistent state without saying how the state comes back. This module holds the
rules behind all of those notes, shared by the book and the website so the two
cannot drift.

This is the most important page in the book. Everything else costs money when it
goes wrong; this costs data.
"""

def intro(oneway):
    """The opening paragraph, with the count of irreversible Moves passed in.

    It used to spell the number out, and the number it spelled was three while
    the book had thirteen - the failure this repository has a rule against, sat
    on the one page where being wrong costs data. Every output counts the Moves
    it is rendering and hands the answer in, the way mission.py takes the total.
    """
    tail = ('and none is labelled irreversible from the outset. Each still has a '
            'point of no return or conditions on recovery.'
            if oneway == 0 else
            f'and {oneway} are not reversible at all.')
    return (
        'Every Move in this book changes a plan, a commitment or a running system. Most are reversible '
        f'for a stated window, a few only until a particular step, {tail} The difference '
        'between a migration and an incident is almost never the technique - it is '
        'whether somebody worked out the way back before they started, and whether '
        'anybody had ever tested it.'
    )

POINTS = [
    ('Read the rollback first',
     'Not the runbook. The Rollback section of every Move names the point of no '
     'return: the step after which the old system can no longer serve traffic or no '
     'longer holds current data. Read it, decide whether you are willing to reach '
     'that step today, and only then start at step one.'),

    ('A backup nobody restored is not a backup',
     'Before Stage 4, restore the backup into isolation, with outbound jobs and '
     'subscriptions disabled. Validate the expected data at its recorded recovery '
     'point and test the recovered application. A changing production database '
     'is not a valid comparison for an older backup. Record recovery time and '
     'confirm the copy and its keys survive loss of the source site.'),

    ('Keep the old thing running, and keep paying for it',
     'The instinct after a successful cutover is to delete the source and book the '
     'saving. Keep the source for the window stated in that Move, with its backups. '
     'The Reversible field can also name a condition, such as an unsigned order; '
     'read it with the rollback. Once the destination accepts writes, a warm source '
     'is stale unless those writes are carried back. Recovery may need a restore '
     'and reconciliation before traffic can return.'),

    ('Cut over when you can undo it, not when you are confident',
     'Confidence is not evidence. The right time to move traffic is when the rollback '
     'has been rehearsed end to end, on the same day of the week, with the same people '
     'awake. A Tuesday morning with the team at their desks beats a Saturday night '
     'with one person and a laptop, every time.'),

    ('Write down the state you cannot recreate',
     'Before Stage 4, list every store whose contents exist nowhere else: the primary '
     'database, the uploads bucket, the secrets, the certificate private keys, the '
     'recovery codes for the accounts that own the domain. Everything else is '
     'rebuildable from a repository. That list is short, and it is the only part of '
     'the estate where a mistake is permanent.'),

    ('Verify by counting, not by looking',
     'A migration is finished when the destination answers the same questions as the '
     'source with the same answers. Row counts, checksums, a replayed hour of real '
     'traffic compared response by response. A page that loads is not evidence, and '
     'neither is an application that starts.'),

    ('Two people, one keyboard',
     'Every High-risk Move in this book assumes a second person who is not typing, is '
     'reading the runbook aloud, and has the authority to stop. It is the cheapest '
     'safety control in infrastructure and the first one teams drop when they are '
     'behind schedule. With two engineers on the whole programme, it is also the one '
     'you are most tempted to skip.'),

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
