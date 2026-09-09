"""Regenerate the tables at the foot of README.md from the Move files.

The repository's one rule is that no total is maintained by hand. The README is
not an exception: everything below the marker is written from moves/*.md, so a
Move that is added, renumbered or retitled cannot leave a stale row behind.

Run `make readme`, or let `make` do it.
"""
import sys
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from parse import load_all, LAYERS, ORDER
from deps import DEPS
from kit import REFERENCE
import costs as COSTS
import roadmap as RM

MARKER = '<!-- generated: everything below this line is written by book/readme.py -->'


def slug(m):
    import re
    return re.sub(r'[^a-z0-9]+', '-', m['title'].lower()).strip('-')


def main():
    moves = load_all()
    if not moves:
        sys.exit('readme: no Move files in moves/ yet')

    zero = sum(1 for m in moves if m['cutover'] == 0)
    oneway = sum(1 for m in moves if m['oneway'])
    risks = Counter(m['risk'] for m in moves)
    total_cut = sum(m['cutover'] for m in moves)
    # LINE savings: what the Move files themselves state, Move 07's cage
    # included as the cost it is. It is NOT the saving the book headlines, and
    # this file printed it under the heading "Illustrative monthly saving" for
    # two editions - which is the exact error the cost page calls the reason
    # repatriations get approved and then regretted, committed by the same
    # repository, on its own front page. Both numbers now appear, each under
    # the name of what it actually is.
    line_saved = sum((m['was'] or 0) - (m['now'] or 0) for m in moves)

    # The real one, computed the way the site and the printed book compute it:
    # the metal, the salaried time and the lines that never come home.
    retained = sum(m['now'] for m in moves
                   if m['was'] is not None and m['now'] is not None)
    # THE SAME FRAMING THE SITE AND THE BOOK USE, or this table prints a
    # headline that contradicts them - which it did, at 50 per cent against
    # their 36, because it divided by the bare bill while they divide by the
    # bill with the cloud's own operations time added to it. The dollar saving
    # is a delta and is identical either way; only the denominator moves.
    _o = COSTS.owned_month(REFERENCE['nodes'], REFERENCE['spares'], retained)
    owned = round(_o['infrastructure']) + round(_o['people']) + round(_o['retained'])
    _cp = round(COSTS.cloud_people_month())
    loaded = COSTS.BILL_MONTH + _cp
    saved = loaded - (owned + _cp)

    out = [MARKER, '']
    out.append('## The book at a glance')
    out.append('')
    out.append('| | |')
    out.append('|---|---|')
    out.append(f'| Moves | {len(moves)} |')
    for k in ORDER:
        rs = [m for m in moves if m['layer'] == k]
        if rs:
            out.append(f'| {LAYERS[k]["roman"]} · {k} | {len(rs)}, '
                       f'{rs[0]["num"]}–{rs[-1]["num"]} |')
    effort = sum(RM.effort_days(m) for m in moves)
    sched = RM.schedule(moves, 2)
    out.append(f'| Work | {effort:,.0f} person-days |')
    out.append(f'| End to end, two engineers | {sched["weeks"]:.0f} weeks, '
               f'including procurement and observation waits |')
    out.append(f'| At zero downtime | {zero} of {len(moves)} |')
    out.append(f'| Whole book, end to end | {total_cut} minutes of user-visible outage |')
    out.append(f'| Cannot be undone | {oneway} |')
    out.append(f'| Risk | {risks["Low"]} low, {risks["Medium"]} medium, '
               f'{risks["High"]} high |')
    out.append(f'| Dependencies | {sum(len(v) for v in DEPS.values())}, every one '
               f'pointing backwards |')
    if line_saved:
        out.append(f'| Line savings across the Moves | ${line_saved:,.0f} a month, '
                   f'after the facility line, before other platform costs |')
    if saved:
        out.append(f'| Saving, with everything counted | ${saved:,.0f} a month '
                   f'&mdash; ${saved * 12:,.0f} a year, {saved / loaded * 100:.0f} '
                   f'per cent of a ${loaded:,.0f} bill with the salary on both '
                   f'sides |')
    out.append('')
    out.append('Every Move names the real service on AWS, Google Cloud and Azure, and the one '
               'thing that differs on each.')
    out.append('')

    for k in ORDER:
        rs = [m for m in moves if m['layer'] == k]
        if not rs:
            continue
        out.append(f'## {LAYERS[k]["roman"]} · {k}')
        out.append('')
        out.append('| # | Move | Leaving | Risk | Cutover | Back out for |')
        out.append('|---|---|---|---|---|---|')
        for m in rs:
            out.append(f'| {m["num"]} | [{m["title"]}](moves/{m["file"]}) | '
                       f'{m["leaving"]} | {m["risk"]} | {m["cutover"]} min | '
                       f'{m["reversible"]} |')
        out.append('')

    body = '\n'.join(out).rstrip() + '\n'
    readme = ROOT / 'README.md'
    text = readme.read_text(encoding='utf-8')
    if MARKER in text:
        text = text.split(MARKER)[0].rstrip() + '\n\n' + body
    else:
        text = text.rstrip() + '\n\n' + body
    readme.write_text(text, encoding='utf-8')
    print(f'readme: {len(moves)} moves -> README.md '
          f'({len(body.splitlines())} generated lines)')


if __name__ == '__main__':
    main()
