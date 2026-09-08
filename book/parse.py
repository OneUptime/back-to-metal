"""Markdown Move files -> structured data. The single reader for every output.

`moves/NN-slug.md` is the source of truth for the book, the website, the EPUB and
the covers. Nothing downstream reads the markdown itself; everything reads what
this returns, so the contract lives here and in verify.py and nowhere else.
"""
import re, html, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOVES = ROOT / 'moves'

# The five Stages. `key` is the CSS/HTML handle, `color` prints and `tint` is the
# opaque panel behind it - opaque because a KDP interior carries no alpha, so a
# tint is a colour rather than a colour at 12%. See flatten.py.
#
# `dark` is the same signal lifted off a near-black ground. It is not a
# decoration: `color` is chosen to sit on paper, and each measure sits between
# 2.2:1 and 3.6:1 against the website's dark background, which is below the 3:1
# floor for a graphic and nowhere near the 4.5:1 a numeral set in it needs. Both
# hexes are the Stage; which one is correct depends on what is behind it, so
# both live here rather than one of them living in a stylesheet.
#
# The Stage names are verbs, not nouns. An earlier edition of this book named
# its Parts after the layers of the system - Iron, Site, Cluster, Platform -
# which is how an architect thinks about an estate and not how somebody halfway
# through the work thinks about their week. "Stage 3 - Build" answers "where am
# I" without anybody having to hold a system diagram in their head. `doing` is
# the whole instruction, `stage` is the number, and `done` is how you know you
# have finished it.
# The `dark` hexes were respaced in 4.0.0. They were chosen one at a time
# against a near-black ground and, seen together in the header's spectrum bar
# and on the front page's twenty, they read as five greys rather than as five
# colours - which is the whole job of a Stage colour. Each is now further from
# its neighbours and from the accent: the nearest pair in the whole palette is
# Run against the accent at a CIE distance of 50, where about 10 is the point
# two colours stop being mistakable. Every one is still 7.3:1 or better against
# both the page and the hover fill.
LAYERS = {
    'Decide':  dict(key='decide',  color='#474F57', dark='#C6CBCF', tint='#ECEEF0', label='Decide',
                    part='I',    roman='Stage 1',  stage=1,
                    doing='Work out whether to do it at all',
                    done='You know what you spend, what you would spend instead, '
                         'and whether it is worth it.'),
    'Buy':     dict(key='buy',     color='#8A6112', dark='#E0A63F', tint='#F4EEE1', label='Buy',
                    part='II',   roman='Stage 2',  stage=2,
                    doing='Order the hardware and sign the space',
                    done='The machines are on order and the cage is signed.'),
    'Build':   dict(key='build',   color='#1F4E79', dark='#6FB2E6', tint='#E6ECF3', label='Build',
                    part='III',  roman='Stage 3',  stage=3,
                    doing='Turn the boxes into a cluster',
                    done='A cluster that could take production traffic, and never has.'),
    'Move':    dict(key='move',    color='#A32E1F', dark='#F0917A', tint='#F6E8E5', label='Move',
                    part='IV',   roman='Stage 4',  stage=4,
                    doing='Move the app, then the data',
                    done='Everything runs on your machines, and the cloud copy is still warm.'),
    'Run':     dict(key='run',     color='#14655A', dark='#5FCCAE', tint='#E3EFED', label='Run',
                    part='V',    roman='Stage 5',  stage=5,
                    doing='Cut the traffic over, and keep it alive',
                    done='Users reach your machines, you can carry it at 03:00, '
                         'and the cloud bill is zero.'),
}
# The order the Stages appear in, and therefore the order the numbering runs in.
# It is the order the work actually happens in: you cannot buy against numbers
# you have not measured, rack machines you have not ordered, or move a database
# onto a cluster that does not exist yet.
ORDER = ['Decide', 'Buy', 'Build', 'Move', 'Run']

RISKS = ['Low', 'Medium', 'High']

# The dial on every Move page reads the cutover against this cap, the way the
# cookbook it is modelled on reads a recipe against twenty minutes. An hour is
# the point past which a cutover stops being a window and becomes an outage.
CUTOVER_CAP = 60

SECTIONS = ['Leaving from', 'Why this works', 'Before you start', 'The runbook',
            "Operator's notes", 'Rollback', 'The numbers', 'What you can turn off']

# The three origins, in this order, on every Move. The jobs in this book are the
# same whichever cloud you are leaving; what differs is the extraction, and that
# is what this block carries. Writing three whole variants of every runbook would
# triple the book to say the same thing three times.
CLOUDS = ['AWS', 'Google Cloud', 'Azure']
CLOUD_KEY = {'AWS': 'aws', 'Google Cloud': 'gcp', 'Azure': 'azure'}
CLOUD_SHORT = {'AWS': 'AWS', 'Google Cloud': 'Google', 'Azure': 'Azure'}

NOTE_LABELS = ['Swap', 'Do it faster', 'Watch out', 'Leftovers']


def inline(s):
    """Markdown inline -> HTML. Bold, italic and `code`, and nothing else."""
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
    return s


def section(text, name):
    m = re.search(r'^## ' + re.escape(name) + r'\s*$(.*?)(?=^## |\Z)', text, re.M | re.S)
    return m.group(1).strip() if m else ''


def money(s):
    """'$2,840/mo' -> 2840.0. Returns None on anything it cannot read."""
    m = re.search(r'\$\s*([\d,]+(?:\.\d+)?)', s or '')
    return float(m.group(1).replace(',', '')) if m else None


def parse(path):
    t = Path(path).read_text(encoding='utf-8')
    r = {'file': Path(path).name}

    h1 = re.search(r'^# (\d+) · (.+)$', t, re.M)
    r['num'], r['title'] = h1.group(1), h1.group(2).strip()

    meta = re.search(
        r'\*\*Layer:\*\* (.+?) · \*\*Leaving:\*\* (.+?) · \*\*Risk:\*\* (.+?)'
        r' · \*\*Cutover:\*\* (.+?) · \*\*Reversible:\*\* (.+?)\s*$', t, re.M)
    r['layer'], r['leaving'], r['risk'], r['cutover_s'], r['reversible'] = \
        [g.strip() for g in meta.groups()]
    r['cutover'] = int(re.match(r'(\d+)', r['cutover_s']).group(1))
    r['l'] = LAYERS[r['layer']]
    r['oneway'] = r['reversible'].strip().lower() in ('no', 'none')

    r['hook'] = re.search(r'^> (.+)$', t, re.M).group(1).strip()
    r['why'] = ' '.join(section(t, 'Why this works').split())

    # ---- Leaving from: one line per cloud, service then the thing that differs
    origins = []
    for line in section(t, 'Leaving from').split('\n'):
        om = re.match(r'^- \*\*(.+?):\*\*\s*(.+?)\s+\u2014\s+(.+)$', line.strip())
        if om:
            cloud, service, note = (g.strip() for g in om.groups())
            origins.append({'cloud': cloud, 'key': CLOUD_KEY.get(cloud, ''),
                            'short': CLOUD_SHORT.get(cloud, cloud),
                            'service': service, 'note': note})
    r['origins'] = origins
    r['services'] = [o['service'] for o in origins]

    # ---- Before you start: grouped exactly as the cookbook groups ingredients
    groups, cur = [], {'name': None, 'items': []}
    for line in section(t, 'Before you start').split('\n'):
        line = line.strip()
        if not line:
            continue
        gm = re.match(r'^\*\*(.+?)\*\*$', line)
        if gm:
            if cur['items']:
                groups.append(cur)
            cur = {'name': gm.group(1), 'items': []}
        elif line.startswith('- '):
            cur['items'].append(line[2:].strip())
    if cur['items']:
        groups.append(cur)
    r['pre_groups'] = groups
    r['pre_count'] = sum(len(g['items']) for g in groups)

    r['steps'] = [re.sub(r'^\d+\.\s*', '', s).strip()
                  for s in re.findall(r'^\d+\.\s+.+$', section(t, 'The runbook'), re.M)]

    notes = []
    for line in section(t, "Operator's notes").split('\n'):
        nm = re.match(r'^- \*\*(.+?):\*\*\s*(.+)$', line.strip())
        if nm:
            notes.append((nm.group(1), nm.group(2)))
    r['notes'] = notes

    r['rollback'] = ' '.join(section(t, 'Rollback').split())

    # ---- The numbers: a fixed five-cell strip, the macro strip's analogue
    # Six cells: | Was | Now | Saved | Cutover | Effort | Wait |
    #
    # `Wait` is the one that is easy to leave out and expensive to omit. Effort
    # is somebody's labour; wait is calendar time that has to pass before the
    # next Move can start, and they are not the same thing. A thirty-day
    # sampling window is four days of work and a month of waiting; a circuit
    # order is a week of work and six weeks of waiting. A schedule built from
    # labour alone starts the next Move on day five and under-forecasts the
    # programme by quarters at exactly the points where being early is most
    # expensive. See roadmap.py, which adds wait to the critical path and not to
    # the person-day budget.
    nums = re.search(
        r'\|\s*(\$[\d,]+(?:\.\d+)?(?:/mo)?|—)\s*\|\s*(\$[\d,]+(?:\.\d+)?(?:/mo)?|—)\s*'
        r'\|\s*([\-−]?\d+%|—)\s*\|\s*(\d+ min)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|',
        section(t, 'The numbers'))
    r['figures'] = [g.strip() for g in nums.groups()]
    r['was'], r['now'] = money(r['figures'][0]), money(r['figures'][1])

    r['turnoff'] = ' '.join(section(t, 'What you can turn off').split())
    r['chars'] = len(t)
    return r


def load_all():
    paths = sorted(glob.glob(str(MOVES / '*.md')),
                   key=lambda f: int(Path(f).name.split('-', 1)[0]))
    return [parse(p) for p in paths]


def by_layer(moves):
    return {k: [m for m in moves if m['layer'] == k] for k in ORDER}


if __name__ == '__main__':
    ms = load_all()
    print(len(ms), 'moves parsed')
    for m in ms[:2] + ms[-1:]:
        print(m['num'], m['title'], '|', m['layer'], '| pre', m['pre_count'],
              '| steps', len(m['steps']), '| notes', len(m['notes']),
              '| figures', m['figures'], '| chars', m['chars'])
    if ms:
        print('max chars:', max(m['chars'] for m in ms), 'min:', min(m['chars'] for m in ms))
        print('max prerequisites:', max(m['pre_count'] for m in ms))
