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
import zipfile
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = ROOT / 'site'
BOOK = ROOT / 'build' / 'book.html'
README = ROOT / 'README.md'

from parse import load_all, inline
import imprint as IMP

EPUB_COSTS = ROOT / 'dist' / IMP.EPUB_NAME / 'OEBPS' / 'costs.xhtml'


class VisibleText(HTMLParser):
    """Extract content, excluding script/style payloads that can mask omissions."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def normalise(markup):
    parser = VisibleText()
    parser.feed(markup)
    # Print uses uppercase metadata and separate spans; typography is not drift.
    return re.sub(r'\s+', '', ''.join(parser.parts)).casefold()


def move_fragments(m):
    # Short metadata values need labelled, exact checks below: "No" can occur
    # inside "not", and zero minutes can occur in an unrelated cost or command.
    for key in ('title', 'leaving', 'hook', 'why', 'rollback', 'turnoff'):
        yield key, m[key]
    for o in m['origins']:
        yield f'{o["cloud"]} service', o['service']
        yield f'{o["cloud"]} extraction', o['note']
    for group in m['pre_groups']:
        for i, item in enumerate(group['items'], 1):
            yield f'prerequisite {group["name"] or ""} {i}', item
    for i, step in enumerate(m['steps'], 1):
        yield f'step {i}', step
    for label, note in m['notes']:
        yield f'note {label}', note
    for label, value in zip(('Was', 'Now', 'Saved', 'Cutover', 'Effort', 'Wait'), m['figures']):
        yield label, value


def metadata_problems(m, output, markup):
    """Compare safety metadata in its labelled field, including both cutovers."""
    # A hidden copy of a correct field must not repair a missing visible one.
    markup = re.sub(r'<(script|style)\b[^>]*>.*?</\1\s*>', '', markup,
                    flags=re.S | re.I)

    def matches(pattern, source=markup):
        return [normalise(value) for value in re.findall(pattern, source, re.S)]

    if output == 'print':
        fields = {
            key: matches(r'<div\b[^>]*class="k"[^>]*>\s*' + label
                         + r'\s*</div>\s*<div\b[^>]*class="v(?: [^"]*)?"[^>]*>'
                         + r'(.*?)</div>')
            for key, label in [('risk', 'Risk'), ('reversible', 'Reversible')]
        }
        fields['Cutover'] = matches(
            r'<div\b[^>]*class="mk"[^>]*>Cutover</div>\s*'
            r'<div\b[^>]*class="mv"[^>]*>(.*?)</div>')
        fields['Cutover figure'] = matches(
            r'<div\b[^>]*class="fig"[^>]*>\s*'
            r'<div\b[^>]*class="v"[^>]*>([^<]*)</div>\s*'
            r'<div\b[^>]*class="k"[^>]*>Cutover</div>')
    elif output == 'website':
        fields = {
            key: matches(r'<dt\b[^>]*>\s*' + label
                         + r'\s*</dt>\s*<dd\b[^>]*>(.*?)</dd>')
            for key, label in [('risk', 'Risk'), ('reversible', 'Back out'),
                               ('Cutover', 'Cutover')]
        }
    else:
        meta = matches(r'<p\b[^>]*class="meta"[^>]*>(.*?)</p>')
        numbers = matches(r'<p\b[^>]*class="numbers"[^>]*>(.*?)</p>')
        fields = {
            key: [value for line in meta for value in matches(pattern, line)]
            for key, pattern in [
                ('risk', r'(?:^|·)([^·]*)risk(?:·|$)'),
                ('reversible', r'(?:^|·)reversible:([^·]*)(?:·|$)'),
                ('Cutover', r'(?:^|·)([^·]*)cutover(?:·|$)'),
            ]
        }
        fields['Cutover figure'] = [
            value for line in numbers
            for value in matches(r'(?:^|·)cutover([^·]*)(?:·|$)', line)
        ]

    expected = {'risk': m['risk'], 'reversible': m['reversible'],
                'Cutover': f'{m["cutover"]} min', 'Cutover figure': m['figures'][3]}
    if output == 'website' and m['reversible'] == 'No':
        expected['reversible'] = 'Cannot be undone'
    return [f'Move {m["num"]}: {output} missing or stale {key} metadata'
            for key, values in fields.items()
            if values != [normalise(inline(expected[key]))]]


def content_problems(moves, book, site, epub):
    """Check each Move in the actual rendered outputs, not renderer return values."""
    problems = []
    for m in moves:
        n = m['num']
        spreads = re.findall(r'<section\b[^>]*data-move="' + n
                             + r'"[^>]*>.*?</section>', book, re.S)
        if len(spreads) != 2:
            problems.append(f'Move {n}: print has {len(spreads)} pages, expected two')
        rendered = {'print': ''.join(spreads), 'website': site.get(n, ''),
                    'EPUB': epub.get(n, '')}
        for output, markup in rendered.items():
            problems += metadata_problems(m, output, markup)
            text = normalise(markup)
            for label, fragment in move_fragments(m):
                if normalise(inline(fragment)) not in text:
                    problems.append(f'Move {n}: {output} missing or stale {label}')
    return problems


def check_content():
    moves = load_all()
    problems = []
    epub_path = ROOT / 'dist' / IMP.EPUB_NAME
    if not BOOK.exists() or not epub_path.exists():
        return ['print HTML or EPUB missing: run make artefacts']
    site, epub = {}, {}
    with zipfile.ZipFile(epub_path) as archive:
        for m in moves:
            slug = re.sub(r'[^a-z0-9]+', '-', m['title'].lower()).strip('-')
            path = SITE / 'm' / f'{m["num"]}-{slug}.html'
            if path.exists():
                site[m['num']] = path.read_text(encoding='utf-8')
            name = f'OEBPS/m/{m["num"]}.xhtml'
            if name in archive.namelist():
                epub[m['num']] = archive.read(name).decode('utf-8')
    problems += content_problems(moves, BOOK.read_text(encoding='utf-8'), site, epub)
    for name in (IMP.PDF_NAME, IMP.EPUB_NAME):
        source, download = ROOT / 'dist' / name, SITE / name
        if not source.exists() or not download.exists():
            problems.append(f'{name}: built edition or website download missing')
        elif source.read_bytes() != download.read_bytes():
            problems.append(f'{name}: website download differs from built edition')
    if not problems:
        print(f'  {len(moves)} complete Moves agree across print, EPUB and web; downloads match')
    return problems

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
        (EPUB_COSTS, rf'id="monthly-owned-saved">{MONEY}<'),
    ]),
    ('the saving, a year', [
        (SITE / 'index.html', rf'bal-y">{MONEY} a year'),
        (README, rf'Saving, with everything counted.*?&mdash; {MONEY} a year'),
    ]),
    ('the headline percentage', [
        (SITE / 'index.html', rf'a year &middot; {PCT} per cent'),
        (SITE / 'cost.html', rf'a year, or {PCT} per cent of everything you spend'),
        (README, rf'a year, {PCT} per cent'),
    ]),
    ('the cloud bill', [
        (SITE / 'cost.html', rf'Infrastructure</th><td data-h="Cloud now">{MONEY}'),
        (SITE / 'index.html', rf'cloud bill is around {MONEY} a month'),
        (EPUB_COSTS, rf'id="monthly-cloud-infrastructure">{MONEY}<'),
    ]),
    ('the saving, in the printed book', [
        (BOOK, rf'What the difference buys</h4><p>{MONEY} a month'),
        (SITE / 'index.html', rf'Saved a month.*?bal-n">{MONEY}<'),
    ]),
    ('the year, in the printed book', [
        (BOOK, rf'What the difference buys.*?a month, or\s*{MONEY} a year'),
        (README, rf'Saving, with everything counted.*?&mdash; {MONEY} a year'),
    ]),
    # WHAT THE BILL BECOMES. This one is here because v6.1.1 shipped with the
    # same quantity carrying two labels on one page: the cost page's hero
    # called $22,776 "Owned, a month" while its own comparison table, four
    # hundred pixels lower, put the owned column's total a month at $37,420.
    # Both were right. They are different quantities - one is the bill line
    # after the move with the extra ops time folded in, the other is the whole
    # monthly cost with the base salary on top - and only the label was wrong.
    # A reader checking the arithmetic on the page that boasts its arithmetic
    # is checkable found two answers. So the delta figure is now named for what
    # it is in all three artefacts, and named identically, which is a thing a
    # regex can hold.
    ('what the bill becomes', [
        (SITE / 'index.html', rf'class="tot"><dt>What the bill becomes</dt>\s*<dd>{MONEY}'),
        (SITE / 'cost.html',
         rf'fig-n">{MONEY}</b><span class="lbl">What the bill becomes'),
        (BOOK, rf'Those three are <b>{MONEY}</b>\s+a month'),
    ]),
    ('person-days', [
        (SITE / 'index.html', rf'The labour is about {PCT} person-days'),
        (README, rf'\| Work \| {PCT} person-days \|'),
        (EPUB_COSTS, rf'reference plan estimates {PCT} person-days'),
    ]),
    ('weeks end to end', [
        (SITE / 'index.html', rf'engineers it lands in roughly {PCT} weeks'),
        (README, rf'End to end, two engineers \| {PCT} weeks'),
        (EPUB_COSTS, rf'across {PCT} weeks with two engineers'),
    ]),
]

for key, label in [('cloud', 'Cloud'), ('rented', 'Rented metal'), ('owned', 'Colocation')]:
    CHECKS.append((f'{label}, five years', [
        (EPUB_COSTS, rf'id="cash-{key}-total">{MONEY}<'),
        (SITE / 'cost.html', rf'<th scope="row">{label}</th>.*?'
         rf'<td data-h="Total over \d+ years">{MONEY}<'),
        (BOOK, rf'<tr><th>{label}</th><td>[^<]*</td><td>[^<]*</td><td>{MONEY}<'),
    ]))


def find(path, pattern):
    if '.epub/' in str(path):
        archive, member = str(path).split('.epub/', 1)
        try:
            with zipfile.ZipFile(archive + '.epub') as z:
                text = z.read(member).decode('utf-8')
        except (FileNotFoundError, zipfile.BadZipFile, KeyError):
            return None, f'{path.name} not built in EPUB'
    else:
        if not path.exists():
            return None, f'{path.name} not built'
        text = path.read_text(encoding='utf-8')
    m = re.search(pattern, text, re.S)
    if not m:
        return None, f'not found in {path.name}'
    return m.group(1).replace(',', ''), None


def main():
    if not SITE.exists():
        sys.exit('agree: no site/ - run `make site` first')
    problems, checked = check_content(), 0
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
