"""Structure: the shape of every Move file, checked before anything is built.

This is one of the two gates. It answers "is this a well-formed Move?" - the
template, the meta line, the arithmetic in the numbers strip, the Parts
invariant, and the house style rules that are a build failure rather than a
preference. audit.py answers the harder question of whether the content is right.

Both must come back clean before a commit.
"""
import re, sys, glob
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse import (LAYERS, ORDER, RISKS, SECTIONS, NOTE_LABELS, CLOUDS,
                   CUTOVER_CAP, section, money, MOVES)

# Marketing language, and the two words that hide difficulty from a reader who
# is about to move a production database. "Simply" and its friends are banned
# outright: if a step is simple it does not need saying, and if it is not, the
# word is a lie.
BANNED = [
    'seamless', 'effortless', 'blazing', 'game-changer', 'game changer',
    'leverage', 'unlock', 'revolutionary', 'painless', 'silver bullet',
    'best-in-class', 'cutting-edge', 'turnkey', 'synergy', 'simply',
    'easy as', 'no time at all', 'in a nutshell',
]

# A Move that moves persistent state must say, in its Rollback section, how the
# data comes back. This is the one failure on this book that would actually cost
# somebody something, so it is a build error rather than a review comment.
STATEFUL = re.compile(
    r'\b(database|postgres|postgresql|mysql|mariadb|aurora|rds|redis|elasticache|'
    r'kafka|msk|opensearch|elasticsearch|dynamodb|s3|bucket|object stor|'
    r'volume|pvc|persistentvolume|ebs|efs|etcd|backup|snapshot|'
    r'replica|wal|dump|restore)\b', re.I)
RESTORE = re.compile(r'\brestor(e|es|ed|ing|ation)\b', re.I)

ONEWAY_WORDS = re.compile(
    r'\b(irreversible|no way back|cannot be undone|can not be undone|'
    r'there is no rollback|no rollback)\b', re.I)

PONR = 'point of no return'


def main():
    files = sorted(glob.glob(str(MOVES / '*.md')),
                   key=lambda f: int(Path(f).name.split('-', 1)[0]))
    print(f'Files: {len(files)}')
    if not files:
        print('\nNo Move files yet.')
        return 0

    nums = [int(Path(f).name.split('-', 1)[0]) for f in files]
    missing = sorted(set(range(1, len(files) + 1)) - set(nums))
    print('Missing numbers:', missing or 'none')

    problems, rows = [], []

    for f in files:
        t = Path(f).read_text(encoding='utf-8')
        n = Path(f).name

        h1 = re.findall(r'^# (.+)$', t, re.M)
        h2 = re.findall(r'^## (.+)$', t, re.M)
        if len(h1) != 1:
            problems.append(f'{n}: {len(h1)} H1s')
        if not re.match(r'^\d{2,3} · \S', h1[0] if h1 else ''):
            problems.append(f'{n}: H1 is not "NN · Title"')
        if h2 != SECTIONS:
            problems.append(f'{n}: H2 mismatch -> {h2}')

        m = re.search(
            r'\*\*Layer:\*\* (.+?) · \*\*Leaving:\*\* (.+?) · \*\*Risk:\*\* (.+?)'
            r' · \*\*Cutover:\*\* (.+?) · \*\*Reversible:\*\* (.+?)\s*$', t, re.M)
        if not m:
            problems.append(f'{n}: meta line malformed')
            continue
        layer, leaving, risk, cutover_s, reversible = [g.strip() for g in m.groups()]

        if layer not in LAYERS:
            problems.append(f'{n}: unknown layer {layer!r}')
        if risk not in RISKS:
            problems.append(f'{n}: risk {risk!r} not one of {RISKS}')
        cm = re.match(r'^(\d+) min$', cutover_s)
        if not cm:
            problems.append(f'{n}: cutover {cutover_s!r} is not "N min"')
            cutover = None
        else:
            cutover = int(cm.group(1))
            if cutover > CUTOVER_CAP:
                problems.append(f'{n}: cutover {cutover} min is over the {CUTOVER_CAP} min '
                                f'dial cap - split the Move or call it an outage')
        # `No` is reserved and load-bearing: it is what marks a Move irreversible
        # everywhere else in the build. Beyond that the field is a short phrase,
        # because the manifest showed the enum was too narrow for real content -
        # "Until the order is signed" and "Per drive, at the cost of a Ceph
        # rebuild" are better answers than any fixed vocabulary allows.
        if not reversible or len(reversible) > 52:
            problems.append(f'{n}: reversible {reversible!r} is empty or over 52 characters')
        elif reversible.endswith('.'):
            problems.append(f'{n}: reversible {reversible!r} is a sentence; it is a label')
        elif reversible.lower() in ('none', 'never', 'n/a'):
            problems.append(f'{n}: reversible {reversible!r} - write "No", which is the '
                            f'value the rest of the build keys on')

        # ---- hook ---------------------------------------------------------
        hook = re.search(r'^> (.+)$', t, re.M)
        if not hook:
            problems.append(f'{n}: no hook line')
        elif len(hook.group(1)) > 170:
            problems.append(f'{n}: hook is {len(hook.group(1))} characters, over 170')

        # ---- leaving from: three clouds, named, in order --------------------
        got = re.findall(r'^- \*\*(.+?):\*\*\s*(.+?)\s+\u2014\s+(.+)$',
                         section(t, 'Leaving from'), re.M)
        if [g[0] for g in got] != CLOUDS:
            problems.append(f'{n}: "Leaving from" must name exactly {CLOUDS} in that order, '
                            f'each as "- **Cloud:** Service \u2014 what differs"; got '
                            f'{[g[0] for g in got]}')
        for cloud, service, note in got:
            if len(service) > 62:
                problems.append(f'{n}: {cloud} service name is {len(service)} characters, '
                                f'over 62 - name the service, put the detail after the dash')
            if len(note.split()) < 4:
                problems.append(f'{n}: {cloud} line says nothing about what differs there')

        # ---- runbook ------------------------------------------------------
        steps = re.findall(r'^\d+\. ', section(t, 'The runbook'), re.M)
        if not (3 <= len(steps) <= 9):
            problems.append(f'{n}: {len(steps)} runbook steps, want 3-9')

        for lab in NOTE_LABELS:
            if f'**{lab}:**' not in t:
                problems.append(f'{n}: missing **{lab}:**')

        # ---- rollback: the safety-critical section --------------------------
        rb = section(t, 'Rollback')
        w = len(rb.split())
        if not (30 <= w <= 140):
            problems.append(f'{n}: rollback is {w} words, want 30-140')
        if PONR not in rb.lower():
            problems.append(f'{n}: rollback does not name the "{PONR}"')
        oneway = reversible.strip().lower() == 'no'
        if oneway and not ONEWAY_WORDS.search(rb):
            problems.append(f'{n}: Reversible is No but the rollback does not say so plainly')
        # The honey rule's analogue: state moved is state that has to come back.
        touches_state = bool(STATEFUL.search(section(t, 'The runbook'))
                             or STATEFUL.search(section(t, 'Before you start'))
                             or layer == 'Data')
        if touches_state and not RESTORE.search(rb):
            problems.append(f'{n}: moves persistent state but the rollback never mentions '
                            f'restoring it')

        # ---- the numbers strip --------------------------------------------
        nm = re.search(
            r'\|\s*(\$[\d,]+(?:\.\d+)?(?:/mo)?|—)\s*\|\s*(\$[\d,]+(?:\.\d+)?(?:/mo)?|—)\s*'
            r'\|\s*([\-−]?\d+%|—)\s*\|\s*(\d+ min)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|',
            section(t, 'The numbers'))
        if not nm:
            problems.append(f'{n}: numbers strip not parsed - want '
                            f'| Was | Now | Saved | Cutover | Effort | Wait |')
        else:
            was_s, now_s, saved_s, cut_s, effort, wait = [g.strip() for g in nm.groups()]
            if cutover is not None and cut_s != f'{cutover} min':
                problems.append(f'{n}: numbers strip says cutover {cut_s!r}, '
                                f'meta line says {cutover} min')
            was, now = money(was_s), money(now_s)
            if was is not None and now is not None and saved_s != '—':
                if was == 0:
                    problems.append(f'{n}: "Was" is $0, so a saving cannot be computed')
                else:
                    want = round((was - now) / was * 100)
                    got = int(saved_s.replace('−', '-').rstrip('%'))
                    if abs(want - got) > 1:
                        problems.append(f'{n}: saved {got}% but ${was:,.0f} -> ${now:,.0f} '
                                        f'is {want}%')
            if not re.match(r'^(<\s*1 day|1 day|1 week|'
                            r'\d+(\.\d+)?\s*(days|weeks)|—)$', effort):
                problems.append(f'{n}: effort {effort!r} is not "< 1 day", "1 day", '
                                f'"N days" or "N weeks"')
            elif re.match(r'^1 (days|weeks)$', effort):
                problems.append(f'{n}: effort {effort!r} - one of them is singular')
            # Wait is calendar time before a dependent Move may start: a sampling
            # window, a circuit order, an RIR queue. A range is allowed and the
            # scheduler takes its pessimistic end.
            if not re.match(r'^(—|\d+(\.\d+)?(\s*(to|\u2013|-)\s*\d+(\.\d+)?)?\s*'
                            r'(day|days|week|weeks|month|months))$', wait):
                problems.append(f'{n}: wait {wait!r} is not "\u2014", "N days", "N weeks", '
                                f'"N months" or a range like "6 to 12 weeks"')
            elif re.match(r'^1 (days|weeks|months)$', wait):
                problems.append(f'{n}: wait {wait!r} - one of them is singular')

        if not section(t, 'What you can turn off').strip():
            problems.append(f'{n}: "What you can turn off" is empty')

        # ---- house style ---------------------------------------------------
        low = t.lower()
        for b in BANNED:
            if re.search(r'\b' + re.escape(b) + r'\b', low):
                problems.append(f'{n}: banned phrase {b!r}')
        # Fenced code may legitimately contain one; prose may not.
        prose = re.sub(r'```.*?```', '', t, flags=re.S)
        prose = re.sub(r'`[^`]*`', '', prose)
        if '!' in prose:
            problems.append(f'{n}: exclamation mark in prose')

        rows.append((Path(f).name.split('-', 1)[0], h1[0] if h1 else '?',
                     layer, risk, cutover, leaving))

    # ---- book-wide invariants ---------------------------------------------
    # Compare the TITLE, not the H1. The H1 carries the Move number, so
    # "01 · The first rack" and "23 · The first rack" are different strings and
    # this check silently passed every duplicate the book has ever had. The
    # website is what noticed: two Moves with the same title slug to the same
    # filename and one quietly overwrites the other.
    titles = [r[1].split(' · ', 1)[-1].strip() for r in rows]
    dupes = {x for x in titles if titles.count(x) > 1}
    if dupes:
        problems.append(f'duplicate titles: {sorted(dupes)}')

    # Two different titles can still reduce to the same slug - "Back-ups" and
    # "Backups" do - and the site writes one file per slug.
    slugs = {}
    for r, t in zip(rows, titles):
        sl = re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
        slugs.setdefault(sl, []).append(r[0])
    for sl, nums in slugs.items():
        if len(nums) > 1:
            problems.append(f'moves {", ".join(nums)} all slug to "{sl}", so the '
                            f'website would write one page for all of them')

    # The Parts must occupy contiguous, correctly-ordered ranges: the whole
    # front matter, every divider and the whole navigation assume it.
    seen, seq = [], [r[2] for r in rows]
    for lay in seq:
        if not seen or seen[-1] != lay:
            seen.append(lay)
    if seen != [l for l in ORDER if l in seen]:
        problems.append(f'Parts are not contiguous and in order: {seen}')

    print('\nPROBLEMS:' if problems else '\nNo problems found.')
    for p in problems:
        print('  -', p)

    print('\nParts:')
    for lay in ORDER:
        rs = [r for r in rows if r[2] == lay]
        if rs:
            print(f'  {LAYERS[lay]["roman"]:8s} {lay:9s} {rs[0][0]}-{rs[-1][0]}  '
                  f'{len(rs):2d} moves')
    print('\nRisk:   ', dict(Counter(r[3] for r in rows)))
    cuts = [r[4] for r in rows if r[4] is not None]
    if cuts:
        print(f'Cutover: {sum(1 for c in cuts if c == 0)} of {len(cuts)} at zero downtime; '
              f'max {max(cuts)} min; total {sum(cuts)} min across the book')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
