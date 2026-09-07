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
    saved = sum((m['was'] or 0) - (m['now'] or 0) for m in moves)

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
               f'most of it waiting for hardware |')
    out.append(f'| At zero downtime | {zero} of {len(moves)} |')
    out.append(f'| Whole book, end to end | {total_cut} minutes of user-visible outage |')
    out.append(f'| Cannot be undone | {oneway} |')
    out.append(f'| Risk | {risks["Low"]} low, {risks["Medium"]} medium, '
               f'{risks["High"]} high |')
    out.append(f'| Dependencies | {sum(len(v) for v in DEPS.values())}, every one '
               f'pointing backwards |')
    if saved:
        # Net, not gross: Move 07 adds a cost line rather than removing one, and a
        # figure that quietly drops it would be the first number in this repository
        # that flattered the argument.
        out.append(f'| Illustrative monthly saving | ${saved:,.0f}, net of what the '
                   f'cage adds |')
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
