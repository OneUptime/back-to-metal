"""Do the three artefacts quote the same numbers?

The fourth gate, and it exists because one bug has now been found three times
in three files. The book publishes the same figures in a website, a printed
interior and a README, each rendered by a different function, and the saving
can honestly be divided by two different denominators: the bare cloud bill, or
that bill with the cloud's own operations time added to it. Both are true. Only
one can be the headline.

  - costs.py's self-test printed 79 per cent while the site printed 56.
  - README.md printed 50 per cent while the site printed 36.
  - build.py was one edit away from the same thing.

Each was caught by somebody reading two outputs side by side and noticing, which
is not a method. So this reads the built artefacts - not the model, the OUTPUT,
because the model agreeing with itself is what was never in doubt - pulls the
figures out of each, and fails if they disagree.

It deliberately checks the RENDERED text rather than calling totals() three
times. A shared function that every caller uses correctly needs no test; the
failure mode here was a caller doing its own arithmetic on the way to the page.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = ROOT / 'site'
BOOK = ROOT / 'build' / 'book.html'
README = ROOT / 'README.md'

# Every figure that appears in more than one artefact, with how to find it in
# each. A pattern that matches nothing is reported rather than skipped: a
# headline that has quietly stopped being printed is exactly as interesting as
# one that disagrees.
MONEY = r'\$([\d,]+)'
PCT = r'(\d+)'

CHECKS = [
    ('the saving, a month', [
        (SITE / 'index.html', rf'Saved a month.*?bal-n">{MONEY}<'),
        (SITE / 'cost.html', rf'class="save".*?{MONEY}'),
        (README, rf'Saving, with everything counted \| {MONEY} a month'),
    ]),
    ('the saving, a year', [
        (SITE / 'index.html', rf'bal-y">{MONEY} a year'),
        (README, rf'Saving, with everything counted.*?&mdash; {MONEY} a year'),
    ]),
    ('the headline percentage', [
        (SITE / 'index.html', rf'a year &middot; {PCT} per cent'),
        (README, rf'a year, {PCT} per cent'),
    ]),
    ('the cloud bill', [
        (SITE / 'cost.html', rf'Infrastructure</th><td data-h="Cloud now">{MONEY}'),
        (SITE / 'index.html', rf'bill around {MONEY} a month'),
    ]),
    ('the saving, in the printed book', [
        (BOOK, rf'What the difference buys</h4><p>{MONEY} a month'),
        (SITE / 'index.html', rf'Saved a month.*?bal-n">{MONEY}<'),
    ]),
    ('the year, in the printed book', [
        (BOOK, rf'What the difference buys.*?a month, or\s*{MONEY} a year'),
        (README, rf'Saving, with everything counted.*?&mdash; {MONEY} a year'),
    ]),
    ('person-days', [
        (SITE / 'index.html', rf'About {PCT} days of work'),
        (README, rf'\| Work \| {PCT} person-days \|'),
    ]),
    ('weeks end to end', [
        (SITE / 'index.html', rf'days of work\s+spread across {PCT}\s+weeks'),
        (README, rf'End to end, two engineers \| {PCT} weeks'),
    ]),
]


def find(path, pattern):
    if not path.exists():
        return None, f'{path.name} not built'
    m = re.search(pattern, path.read_text(encoding='utf-8'), re.S)
    if not m:
        return None, f'not found in {path.name}'
    return m.group(1).replace(',', ''), None


def main():
    if not SITE.exists():
        sys.exit('agree: no site/ - run `make site` first')
    problems, checked = [], 0
    for label, places in CHECKS:
        seen = {}
        for path, pattern in places:
            value, err = find(path, pattern)
            if err:
                problems.append(f'{label}: {err}')
                continue
            seen.setdefault(value, []).append(path.name)
        if len(seen) > 1:
            where = '; '.join(f'{v} in {", ".join(ns)}' for v, ns in seen.items())
            problems.append(f'{label}: DISAGREE - {where}')
        elif seen:
            checked += 1
            print(f'  {label:24} {list(seen)[0]:>10}  '
                  f'{", ".join(sorted(n for ns in seen.values() for n in ns))}')

    if problems:
        print(f'\nagree: {len(problems)} problems')
        for p in problems:
            print('  -', p)
        return 1
    print(f'\nagree: {checked} figures, and every artefact quotes the same one')
    return 0


if __name__ == '__main__':
    sys.exit(main())
