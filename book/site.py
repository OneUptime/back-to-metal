"""Generate the website from the same Move files that make the book.

Five pages and one page per Move. The reader is an engineer with a cloud
bill and two colleagues, and they arrive wanting three things: what is this,
what does it cost, and what do I do next. So there is a page for each, plus the
page you have to read before touching anything and the page that says who wrote
it. Everything else the previous edition had - a left rail, a sticky chrome, a
spine, a jump box, seven stage pages, a dependency planner - was an instrument
for somebody running a four-year programme, and this book is half a year long.

The one mechanic that spans every page is the `next` link in the header: the
lowest-numbered Move the reader has not ticked. The build renders Move 01 into
it, which is the correct answer for every reader on a first visit, so the site
is legible, correct and navigable with no script at all.

Output lands in site/ as plain files - no server, no build step, no external
request. The fonts and the Stage colours are written into the stylesheet, so
the directory drops onto any static host unchanged and works from a file:// URL.
"""
import base64, html, json, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from parse import load_all, LAYERS, ORDER, inline
from icons import risk_bars
from deps import needs as dep_needs, unlocks as dep_unlocks
from kit import SHELVES, RULES, KIT, REFERENCE, HOMELAB, HOMELAB_KIT, PLATFORM_SCOPE, COST_SCOPE
from rollback_data import intro as rb_intro, POINTS as RB_POINTS, DISCLAIMER as RB_DISC
from equivalents import ROWS as EQ_ROWS, CLOUDS as EQ_CLOUDS
from symptoms import SYMPTOMS
from version import VERSION
import roadmap as RM
import costs as COSTS
import imprint as IMP
import mission as MISSION
import why as WHY
import worksheets as WS

SITE = ROOT / 'site'
ASSETS = SITE / 'assets'
NM = ROOT / 'node_modules'

PDF_NAME = IMP.PDF_NAME
EPUB_NAME = IMP.EPUB_NAME
PDF_SRC = ROOT / 'dist' / PDF_NAME
EPUB_SRC = ROOT / 'dist' / EPUB_NAME
GH_URL = f'https://{IMP.REPO}'

# The crew the site quotes its schedule for. Two, because that is who this
# edition is written for: a platform of two or three engineers, one of whom
# still has a day job. The other two are drawn only as a comparison, so a
# reader can see what a third pair of hands actually buys - which is less than
# people expect, because the long pole is lead time and not labour.
DEFAULT_CREW = 2
CREWS = (1, 2, 3)

# The width of the full-bleed track, in the same units the drawings are authored
# in: `--page` minus two gutters, and the number style.css computes its ledger
# tracks from (544 + 96 + 416). The roadmap used to be authored at 1180 and set
# to width:100%, so it scaled to 0.895 in this track and its own axis labels
# rendered at 8.95px - under --t-fine, the smallest size the type scale admits.
# roadmap.py keeps its 1180 default, so the printed drawing is untouched.
SITE_TRACK = 1056

esc = lambda s: html.escape(str(s), quote=False)
attr = lambda s: html.escape(str(s), quote=True)
b64 = lambda p: base64.b64encode(Path(p).read_bytes()).decode()
mny = lambda v: f'${v:,.0f}'


def slug(m):
    return re.sub(r'[^a-z0-9]+', '-', m['title'].lower()).strip('-')


def page(m):
    """The Move's filename. Numbered as well as named, so a URL sorts, and so
    `m/16.html` can redirect to something without guessing at the title."""
    return f'{m["num"]}-{slug(m)}.html'


def pdf_pages():
    if not PDF_SRC.exists():
        return None
    counts = [int(m) for m in re.findall(rb'/Count\s+(\d+)', PDF_SRC.read_bytes())]
    return max(counts) if counts else None


def fonts_css():
    """Archivo and JetBrains Mono, embedded. Two families: one carries every word,
    the other every number. The 'standard' cut of Archivo is the one with the
    width axis the display voice is built on.

    The italic cut is not embedded. It is 130 KB of a render-blocking stylesheet
    and the site sets nothing in it - the one italic on the page is `<em>` inside
    the wordmark, which is coloured rather than sloped."""
    AR = NM / '@fontsource-variable/archivo/files'
    JB = NM / '@fontsource-variable/jetbrains-mono/files'
    css = (f"@font-face{{font-family:'Archivo';src:url(data:font/woff2;base64,"
           f"{b64(AR / 'archivo-latin-standard-normal.woff2')}) "
           f"format('woff2-variations');font-weight:100 900;font-stretch:62% 125%;"
           f"font-style:normal;font-display:swap}}\n")
    css += (f"@font-face{{font-family:'JetBrains Mono';src:url(data:font/woff2;base64,"
            f"{b64(JB / 'jetbrains-mono-latin-wght-normal.woff2')}) "
            f"format('woff2-variations');font-weight:100 800;font-style:normal;"
            f"font-display:swap}}\n")
    return css


def parts_css():
    """The five Stage colours, as attribute rules rather than inline hexes.

    `parse.LAYERS` is the single source and carries three hexes a Stage:
    `color` for paper, `dark` for a near-black ground, `light` for this one.
    The screen is light now, so the screen takes `light` - and there is no
    print block, because the two grounds are near enough that a second palette
    would be two sets of numbers to keep at contrast rather than one.

    DO NOT point the screen at `color`. Measured on #FBF9F4 the paper set
    clears AA, but paper Buy sits CIEDE2000 6.16 from the money colour and
    paper Decide 12.67 from paper Build - both of the collisions 6.0.0
    removed. That is what the `light` key is for.

    Inlining a hex into a `style="--c:#1F4E79"` on every coloured element is
    what the site used to do, and it painted Stage signals at 2.2:1 to 3.6:1
    on a ground they were never chosen for."""
    def block(key):
        return '\n'.join(f'[data-part={LAYERS[k]["key"]}]{{--c:{LAYERS[k][key]}}}'
                          for k in ORDER)

    def spectrum(key):
        """All five Stages at once, as hard-edged bands across one gradient.

        The header wears it along its bottom edge and the footer along its
        top, so a page is a spread with the book's colours on both edges. It
        is the only place on the site where all five appear together - which
        is what lets a reader read a Stage colour as one of a set rather than
        as an arbitrary hue on a rule. Hard stops, not a blend: these are five
        categories and a gradient between them would imply a scale."""
        n = len(ORDER)
        stops = []
        for i, k in enumerate(ORDER):
            c = LAYERS[k][key]
            stops.append(f'{c} {i / n * 100:.4g}%')
            stops.append(f'{c} {(i + 1) / n * 100:.4g}%')
        return f'--spectrum:linear-gradient(90deg,{",".join(stops)})'

    return (
        '\n/* The five Stages, written by site.py out of parse.LAYERS. The screen\n'
        '   is paper-coloured, so it takes the `light` hex, and paper takes the\n'
        '   same one - one ground, one palette, one set of numbers to keep. */\n'
        + block('light') + '\n'
        + ':root{' + spectrum('light') + '}\n')


# ------------------------------------------------------------- the reveal list
# THE ONE COPY. This list used to live twice - once as a selector list in
# style.css and once as a string in app.js - and the two had to agree, because
# a selector added to the stylesheet and not to the script leaves an element at
# opacity 0 for ever. So the build owns it and writes both.
#
# WHAT IS AND IS NOT ON IT. Only structure arrives: headings, figure strips,
# rows, tables, charts, controls. Running prose is not on this list and must
# never be added to it. A paragraph that is invisible until it is scrolled to
# is a paragraph withheld from somebody reading fast, and this is a book about
# doing a thing rather than a page about a product - the reader is trying to
# find out what a Move costs, not to be shown around.
#
# It is also a list of LEAVES: a reveal nested inside another reveal adds the
# two offsets together and reads as a stumble, which is why `.stage-head` is
# here and `.stage` is not.
RISE = [
    '.sect', '.figs', '.summary', '.twenty', '.prog', '.prog-bar',
    '.cta', '.actions', '.cost-key',
    '.stage-head', '.mv>li', '.ck', '.symp li', '.pt', '.rules>li',
    '.shelf', '.dl', '.tablewrap', '.cost', '.rm', '.perm', '.cmp',
    '.notes>div', '.pre-g', '.mf', '.colo',
]


def rise_css():
    """The hidden state, and nothing else - the transition that undoes it and
    the failsafe that guarantees it are both in style.css, where the rest of
    the motion system is."""
    sel = ',\n    '.join(RISE)
    return (
        '\n/* The reveal list, written by site.py out of RISE so the stylesheet\n'
        '   and app.js cannot hold different opinions about what is hidden.\n'
        '   `:where()` keeps this at the specificity of `html.rise` alone, so\n'
        '   the `.in` rule in style.css outranks it. */\n'
        '@media (prefers-reduced-motion:no-preference){\n'
        f'  html.rise :where({sel}){{\n'
        '    opacity:0;transform:translateY(14px);\n'
        '    transition:opacity var(--t-rise) var(--e-out),\n'
        '               transform var(--t-rise) var(--e-out)}\n'
        '}\n')


# ------------------------------------------------------------------ the shell
# Five items, in the order somebody asks the questions. No rail, no spine, no
# jump box: with twenty Moves in a fixed order the order IS the navigation, and
# a nav that fits on one line of a phone does not need a disclosure to hide in.
NAV = [
    ('index.html', 'The guide'),
    ('cost.html', 'What it costs'),
    ('checklist.html', 'Your checklist'),
    ('start.html', 'Before you start'),
    ('about.html', 'About'),
]

# FIVE, AND IT HAS TO BE FIVE. A sixth entry - an in-page anchor to the case
# for leaving - was the difference between a header on one row and a header on
# two: the bar is capped at 1056px and its children needed 1114, so it wrapped
# at every desktop width from 1280 to 1920 and put the `next` link bottom left,
# under the wordmark, with its own divider rule hanging off nothing. The anchor
# is not a page and it lives in the footer, which is where the second tier goes.

# The footer's page columns. NAV is what the site IS; this is the site GROUPED,
# and the grouping is the two questions the pages answer - is this worth doing,
# and how do I start. The three front-page section anchors live here and only
# here: index.html is twelve screens tall, and #plan, #where and #how-long are
# reachable from nothing else on the site. The assert makes a NAV entry nobody
# placed a build error rather than a link the footer quietly drops.
FOOT_PAGES = [
    ('Is it worth it', [('index.html#why',      'Why leave'),
                        ('cost.html',           'What it costs'),
                        ('index.html#how-long', 'How long it takes')]),
    ('The plan',       [('index.html',          'The whole guide'),
                        ('index.html#plan',     'The whole plan'),
                        ('index.html#where',    'Start where it hurts')]),
    ('Doing it',       [('checklist.html',      'Your checklist'),
                        ('start.html',          'Before you start'),
                        ('about.html',          'About')]),
]
_placed = {h for _, rows in FOOT_PAGES for h, _ in rows}
assert _placed >= {h for h, _ in NAV}, \
    'FOOT_PAGES must place every NAV entry: ' + str({h for h, _ in NAV} - _placed)


def theme(var):
    """One token, read off the line the browser will read.

    `<meta name="theme-color">` lives in the head and cannot reference a custom
    property, so this is the one place on the site where a colour has to leave
    the stylesheet. It leaves by being READ rather than by being typed a second
    time: the head used to carry `#0C0F11` as a literal, which is how a mobile
    browser ends up painting a near-black band over a paper page and why the
    first thing a phone reader sees is the one part of the design that did not
    get the memo."""
    css = (HERE / 'web' / 'style.css').read_text(encoding='utf-8')
    m = re.search(rf'--{var}:\s*(#[0-9A-Fa-f]{{3,8}})', css)
    assert m, f'style.css no longer defines --{var}'
    return m.group(1)


def shell(title, body, depth=0, desc=''):
    """The document. One stylesheet, and two scripts: the corpus of Moves, then
    the behaviour that reads it. `app.js` is deferred rather than inlined
    mid-body because nothing above the fold now depends on it - the header's
    next link is already correct in the HTML.

    The one inline script is the reveal's dead man's handle. It puts `rise` on
    the root element, which is the only thing that lets the stylesheet hide
    anything, and it immediately arms a two-second timer to take it off again.
    app.js clears that timer as its first act. So the hidden state exists only
    while a script that can undo it is known to be running: if app.js 404s, is
    blocked, or throws on the way in, the timer fires and the reader gets the
    whole page. Written into the head rather than the stylesheet because it has
    to be true before the first paint, or the reveal is a flash instead."""
    up = '../' * depth
    v = f'?v={VERSION}'
    js = ''.join(f'\n<script src="{up}assets/{s}{v}" defer></script>'
                 for s in ('moves-index.js', 'app.js'))
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{attr(desc)}">
<meta name="theme-color" content="{theme('bg')}">
<link rel="stylesheet" href="{up}assets/style.css{v}">
<!-- The favicon is DELIBERATELY the inverse of the page: a dark tile stands out
     in a light tab strip, and a paper-coloured one would disappear into it. The
     hex is the dark edition's ground, kept on purpose - do not "fix" it. -->
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%230C0F11'/%3E%3Crect x='2' y='3' width='12' height='2.6' fill='%23fff'/%3E%3Crect x='2' y='6.7' width='8' height='2.6' fill='%23fff'/%3E%3Crect x='2' y='10.4' width='4.5' height='2.6' fill='%23fff'/%3E%3C/svg%3E">
<script>var d=document.documentElement;d.className='js rise';
window.BTM_RISE_T=setTimeout(function(){{d.classList.remove('rise')}},2000)</script>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
<div class="rail" id="rail" aria-hidden="true"></div>
{body}{js}
</body>
</html>"""


def bar(depth, first, active=''):
    """The header: a wordmark, five links, and the next Move.

    It IS sticky, and for two editions this docstring said it was not. Sticky
    chrome on a page somebody reads for twenty minutes was the argument
    against; the answer is that this is twenty-five pages in a fixed order, the
    header carries the one thing that knows where the reader is in them, and
    somebody four screens down a Move page had to go back to the top to use it.
    It pays for the space by halving its padding once the masthead is behind
    it, and on a phone it folds the nav row away entirely."""
    up = '../' * depth
    links = ''.join(
        f'<a href="{up}{h}"' + (' class="on" aria-current="page"' if h == active else '')
        + f'>{esc(t)}</a>' for h, t in NAV)
    return (f'<header class="bar"><div class="bar-in">'
            f'<a class="wm" href="{up}index.html">{IMP.wordmark_html(sep=" ")}</a>'
            f'<nav class="nav" aria-label="Sections">{links}</nav>'
            f'<a class="next" id="next" href="{up}m/{page(first)}">'
            f'<span class="lbl">Next</span>'
            f'<b class="next-n">{first["num"]}</b>'
            f'<span class="next-t">{esc(first["title"])}</span>'
            f'</a></div></header>')


def foot(depth=0):
    """The colophon: a directory, a sign-off and a licence strip, on the full
    page rather than stacked in the account measure.

    It is built out of objects the reader has already met higher up - the ruled
    link column is the shelf from the kit list, the labelled strip along the
    foot is the colophon from the about page - because a footer that invents
    its own layout is the part of a document that most looks like it was added
    last.

    Four things have to survive any change here. Every page and every
    front-page section is reachable from the bottom of every page. Both
    editions are downloadable and say so in mono, rather than presenting as a
    seventh page the way `PDF` did in a flat run of nine identical links. The
    safety page is linked as an instruction and not as one entry in a list.
    And the OneUptime interest is declared beside the byline that creates it -
    see imprint.DISCLOSURE and AGENTS.md; the two travel together."""
    up = '../' * depth

    def row(href, text, tag='', dl=False):
        t = f'<span class="ftag">{esc(tag)}</span>' if tag else ''
        return (f'<li><a href="{href}"{" download" if dl else ""}>'
                f'<span class="ftxt">{esc(text)}</span>{t}</a></li>')

    def col(head, rows):
        return (f'<div class="fcol"><h2 class="lbl">{esc(head)}</h2>'
                f'<ul>{"".join(rows)}</ul></div>')

    cols = [col(h, [row(up + p_, txt) for p_, txt in rows]) for h, rows in FOOT_PAGES]
    book = []
    if PDF_SRC.exists():
        book.append(row(up + PDF_NAME, 'The print interior', 'PDF', dl=True))
    if EPUB_SRC.exists():
        book.append(row(up + EPUB_NAME, 'The Kindle edition', 'EPUB', dl=True))
    book.append(row(GH_URL, 'The Moves and the typesetter', 'GITHUB'))
    cols.append(col('Take it with you', book))

    return (
        f'<footer class="foot"><div class="foot-in">'
        f'<nav class="foot-dir" aria-label="Everything on this site">'
        f'{"".join(cols)}</nav>'
        f'<div class="foot-say">'
        f'<p class="foot-note">Every Move records an estimated cutover in minutes '
        f'of user-visible downtime, its risk and the conditions for rollback. '
        f'The schedule is computed from effort, calendar waits and dependencies. '
        f'Prices combine dated cloud list rates and illustrative hardware, '
        f'facility and staffing allowances. Savings are model results, '
        f'not quotations for a particular estate.</p>'
        f'<p class="foot-go"><a href="{up}start.html">Read the safety page before '
        f'running anything</a></p></div>'
        f'<div class="foot-imp">'
        f'<a class="by" href="https://{IMP.ONEUPTIME_SITE}">'
        f'<img src="{up}assets/oneuptime.svg" alt="OneUptime" width="160" height="32">'
        f'<span>{esc(IMP.BYLINE)}</span></a>'
        f'<p class="foot-fine">'
        f'<a href="https://{IMP.ONEUPTIME_SITE}">{IMP.ONEUPTIME_SITE}</a> is an '
        f'open-source platform for uptime, incidents, on-call and status pages. '
        f'It is recommended in Stage 5, and the interest is declared on the '
        f'<a href="{up}about.html">about page</a>.</p></div>'
        f'<dl class="colo foot-colo">'
        f'<div><dt class="lbl">Software</dt><dd>MIT</dd></div>'
        f'<div><dt class="lbl">Text</dt><dd>CC BY 4.0</dd></div>'
        f'<div><dt class="lbl">Version</dt><dd>v{VERSION}</dd></div>'
        f'</dl></div></footer>')


# The ink the vendored mark ships in, which is what a paper page wants.
LOGO_INK = '#121212'


def write_logo():
    """OneUptime's own mark, vendored and copied through unchanged.

    It is a file rather than inline markup because it is twenty kilobytes of
    traced paths and there are twenty-five pages: inlined it would cost half a
    megabyte to say the same thing twenty-five times, where a file is fetched
    once and cached. Same origin, so the rule about making no external request
    still holds - the site drops onto a static host and works from file://.

    The dark edition recoloured the wordmark to #E9EDEF so it would read on a
    near-black ground. On this one that measures 1.18:1 and the publisher's own
    name is a blank in the footer of all twenty-five pages - and nothing would
    have caught it, because the mark is an <img> and the contrast gate only
    walks text. Nothing is recoloured now.

    The mark's green is not touched either. It is 1.67:1 here and it will look
    pale, but a brand mark is exempt from the text rule and repainting somebody
    else's mark to suit your page is the wrong repair.
    """
    svg = (HERE / 'web' / 'oneuptime.svg').read_text(encoding='utf-8')
    assert LOGO_INK in svg, 'the vendored mark no longer carries the ink we check'
    (ASSETS / 'oneuptime.svg').write_text(svg, encoding='utf-8')


def moves_index_js(moves):
    """The corpus every script on the site works from.

    One row per Move: `[num, slug, title, effortDays, was, now]`. `slug` is the
    page's own basename, number included, so a link is `'m/' + slug + '.html'`
    and there is no filename convention encoded in two places. The effort and
    the two prices are here so the checklist's live arithmetic runs off the
    numbers the build computed rather than a second set typed into JavaScript -
    a Move whose figures change moves the summary panel with it.

    It is a script rather than JSON in the markup because it is fetched once and
    cached across the whole site, and because a `<script src>` still resolves
    from a file:// URL where a fetch does not."""
    # `was` and `now` stay null when the Move does not state them. Flattening a
    # missing half to zero would make Move 07 - which states a Now and no Was,
    # because the cage adds a cost rather than removing one - read as a saving
    # of minus $1,400, and any future Move that stated a Was and no Now would
    # read as saving the whole of it. A null is a Move whose trade is somewhere
    # else on the bill, and the script has to be able to tell the difference.
    rows = [[m['num'], page(m)[:-5], m['title'], RM.effort_days(m),
             m['was'], m['now']] for m in moves]
    return ('window.BTM_MOVES=' + json.dumps(rows, separators=(',', ':')) + ';\n'
            + 'window.BTM_RISE_SEL=' + json.dumps(','.join(RISE)) + ';\n')


# ---------------------------------------------------------------- the numbers
def totals(moves):
    """Every figure any page quotes, computed once.

    Nothing here is written into prose anywhere. The pages interpolate this
    dict, so a Move added, removed or re-costed moves every sentence that
    mentions a total, in the same way mission.py takes the count as an
    argument rather than spelling it out."""
    R = REFERENCE
    sched = RM.schedule(moves, DEFAULT_CREW)
    # Only the Moves that state both halves of the trade can contribute to a
    # saving. A Move with an em dash in either cell is not a zero, it is a Move
    # whose saving is somewhere else on the bill.
    priced = [m for m in moves if m['was'] is not None and m['now'] is not None]

    # WHAT YOU GO ON PAYING. The Now column of those same Moves, summed, and
    # the single line the comparison used to leave out: Move 04's content
    # network, outbound mail and edge scrubbing, which it explicitly tells the
    # reader to write in as permanent, plus the residue five other Moves keep -
    # archived object storage, a registry, a queue, off-site backup. Every
    # dollar of it is inside the before-state on the left, so leaving it out of the
    # after-state overstated the saving by exactly this much.
    #
    # It comes off the priced Moves rather than off every Move, and that is
    # load-bearing rather than incidental. A Move whose Now is part of the
    # OWNED SITE - Move 07's rack, at $4,500 - states no Was, because there was
    # nothing there before to state, and site_month() already carries it. So
    # the rule is: a Move that states both halves is trading one bill for a
    # smaller bill, and the smaller bill is retained; a Move that states only a
    # Now is buying something the model already counts. Anything added later
    # that breaks that rule has to be counted by hand here.
    retained = sum(m['now'] for m in priced)

    owned = COSTS.owned_month(R['nodes'], R['spares'], retained)
    dedicated = COSTS.dedicated_month(R['nodes'] + R['spares'], retained)

    # ROUND ONCE, HERE, AND MAKE EVERY TOTAL THE SUM OF THE ROUNDED PARTS.
    # Every figure on this site is printed to the nearest dollar, and a column
    # of rounded parts under a rounded total does not add up: $3,235 + $7,917 +
    # $2,310 is $13,462 and the total printed $13,461. A reader doing exactly
    # what costs.py's docstring invites - checking the arithmetic - found the
    # first sum they tried was a dollar out, on a page whose whole argument is
    # that other people's comparisons are sloppy. So the parts are the truth
    # and the total is their sum, everywhere, including the year and the
    # percentage.
    def dollars(c):
        i, pp, k = (round(c['infrastructure']), round(c['people']),
                    round(c['retained']))
        return {'infrastructure': i, 'people': pp, 'retained': k,
                'total': i + pp + k}

    owned, dedicated = dollars(owned), dollars(dedicated)

    # BOTH COLUMNS CARRY THEIR OWN PEOPLE. The saving is a delta and is
    # unchanged by this - a delta is a delta - but the percentage is not, and
    # the old denominator was a cloud bill with the salary taken out of it
    # sitting beside an owned column with the salary left in. Two numbers are
    # quoted now because two are true: `pct` is the honest total-cost figure
    # with the salary on both sides, and `pct_infra` is the infrastructure
    # line alone, which is what every other comparison in the world quotes and
    # what the reader will have been shown by somebody else.
    cloud_people = round(COSTS.cloud_people_month())
    cloud_total = COSTS.BILL_MONTH + cloud_people
    save = cloud_total - (owned['total'] + cloud_people)
    infra_save = COSTS.BILL_MONTH - (owned['infrastructure'] + owned['retained'])
    return {
        'n': len(moves),
        'stages': RM.stages(moves, sched),
        'days': sum(RM.effort_days(m) for m in moves),
        'weeks': sched['weeks'],
        'critical_weeks': RM.critical_path(moves)['days'] / RM.WEEK,
        'crew_weeks': {w: RM.schedule(moves, w)['weeks'] for w in CREWS},
        'bill': COSTS.BILL_MONTH,
        'owned': owned,
        'dedicated': dedicated,
        'retained': retained,
        'save': save,
        'year': save * 12,
        'five_year': COSTS.five_year(R['nodes'], R['spares'], retained),
        'cloud_people': cloud_people,
        'cloud_total': cloud_total,
        'infra_save': infra_save,
        'pct': save / cloud_total * 100 if cloud_total else 0,
        'pct_infra': infra_save / COSTS.BILL_MONTH * 100 if COSTS.BILL_MONTH else 0,
        'zero': sum(1 for m in moves if m['cutover'] == 0),
        'cutover': sum(m['cutover'] for m in moves),
        'oneway': sum(1 for m in moves if m['oneway']),
        'stated': sum(m['was'] - m['now'] for m in priced),
    }


# ----------------------------------------------------------- shared fragments
def downtime(m):
    return 'no downtime' if not m['cutover'] else f'{m["cutover"]} min down'


def back_out(m):
    return 'Cannot be undone' if m['oneway'] else m['reversible']


def figs(items):
    """The four-across figures strip. `items` is (value, label)."""
    return '<div class="figs">' + ''.join(
        f'<div class="fig"><b class="fig-n">{v}</b><span class="lbl">{esc(k)}</span></div>'
        for v, k in items) + '</div>'


def twenty(moves):
    """The whole book as twenty bars, one per Move, each as tall as its own
    effort figure and painted in its Stage's colour.

    It is two things at once and that is why it earns the space: a table of
    contents you can click, and the shape of the work - where the heavy days
    are, and that they are in the middle rather than at the start where a
    reader braced for a hard beginning expects them. The heights come from the
    same numbers strips the schedule is computed from, so it cannot drift from
    the roadmap further down the page.

    With no stylesheet and no script it is a row of twenty numbered links,
    which is a table of contents, which is what it was.
    """
    top = max(RM.effort_days(m) for m in moves) or 1
    cells = []
    for i, m in enumerate(moves):
        first = i and m['layer'] != moves[i - 1]['layer']
        cells.append(
            f'<a class="tw{" first" if first else ""}" data-part="{m["l"]["key"]}" '
            f'href="m/{page(m)}" style="--h:{RM.effort_days(m) / top:.3f};--i:{i}" '
            f'aria-label="Move {m["num"]} \u00b7 {attr(m["title"])}, '
            f'{attr(m["figures"][4])}" title="{attr(m["title"])}">'
            f'<i></i><b>{m["num"]}</b></a>')
    return (f'<nav class="twenty" aria-label="Every Move">{"".join(cells)}</nav>'
            f'<p class="twenty-k">One bar a Move, as tall as the days it takes, '
            f'in the colour of its stage.</p>')


def hero_index(T, first):
    """The front page above the fold: the masthead on the left, and on the
    right THE BALANCE - the subtraction this book performs, shown once.

    What was here was a four-across strip setting 20 / 80 / 32 / 56% at one
    size in one colour: four equal figures on a page whose argument is one
    figure. Three of them are context and the fourth is the claim, and giving
    them the same weight is how a reader ends up reading twenty row titles to
    find out what is being asserted.

    It is a ledger, read top to bottom as a subtraction rather than left to
    right as four unrelated facts, and it adds up - the parts are the rounded
    parts the cost page prints, and the total is their sum. Every figure
    interpolates T, so a re-costed Move moves the front page.
    """
    return f"""
<section class="hero led">
  <div class="acct">
    <h1 class="d mast">{IMP.wordmark_html(sep='<br>')}</h1>
    <p class="open">{T['n']} Moves that take a company off AWS, Google Cloud or
      Azure and onto dedicated servers you rent or own in colocation.</p>
    <p class="sub">Written for a company whose platform is two or three
      engineers' work and whose cloud bill is around {mny(T['bill'])} a month.
      Keep the team, bring your platform skills, and let remote hands handle the
      physical work. Rent to preserve cash; colocate to own the capacity.</p>
    <p class="cta"><a class="btn" href="m/{page(first)}">Start at Move
      {first['num']}</a> <a class="btn ghost" href="#why">The case for
      leaving</a></p>
  </div>
  <aside class="amt bal" aria-label="The bill, before and after">
    <p class="lbl">The bill, a month</p>
    <dl class="bal-l">
      <div><dt>Cloud infrastructure</dt><dd class="was">{mny(T['bill'])}</dd></div>
      <div><dt>Machines you own</dt><dd>{mny(T['owned']['infrastructure'])}</dd></div>
      <div class="ops-row" data-tooltip><dt>Additional ops cost
        <button class="ops-help-trigger" type="button" hidden
          aria-label="Why this additional ops cost?" aria-expanded="false"
          aria-controls="ops-cost-note" aria-describedby="ops-cost-note">?</button>
        <span class="ops-help-note" id="ops-cost-note" role="tooltip">
          The model assumes your existing cloud ops engineers transition to
          running the on-premises platform, with no additional permanent hires.
          The colo facility&rsquo;s remote hands can handle physical tasks such
          as cabling and drive swaps; their cost is already included in
          infrastructure. On-premises operations roles can cost less than cloud
          specialist roles, offering further salary savings. To keep the estimate
          conservative, this model retains the same staffing cost and counts
          none of those potential savings.
        </span></dt><dd>{mny(T['owned']['people'])}</dd></div>
      <div><dt>Still somebody else&rsquo;s invoice</dt>
        <dd>{mny(T['owned']['retained'])}</dd></div>
      <div class="tot"><dt>What the bill becomes</dt>
        <dd>{mny(T['owned']['total'])}</dd></div>
    </dl>
    <p class="bal-t"><span class="lbl">Saved a month</span>
      <b class="bal-n">{mny(T['save'])}</b></p>
    <p class="bal-y">{mny(T['year'])} a year &middot; {T['pct']:.0f} per cent, with
      {mny(T['cloud_people'])} of salary counted on both sides.
      <a class="mg-x" href="cost.html">How the figure is built &rarr;</a></p>
  </aside>
</section>"""


def hero(title, lede, sub='', display='page', extra=''):
    return (f'<section class="hero"><h1 class="d {display}">{title}</h1>'
            f'<p class="lede">{lede}</p>'
            + (f'<p class="sub">{sub}</p>' if sub else '') + extra + '</section>')


def band(bid, heading, inner, margin='', full=''):
    """A section, on the ledger grid.

    `inner` is the account - the argument. `margin` is what the argument is
    about: figures, a Stage key, a cross-reference, a note that used to
    interrupt the prose. `full` is anything that has earned the whole width -
    a chart, a table, the twenty - and breaks both tracks.

    A section with nothing for the margin collapses to one column and says so
    with `.solo`, because a page of pure argument is allowed to be one column
    and a ruled-off empty gutter is not.
    """
    solo = '' if margin else ' solo'
    return (f'<section class="band led{solo}" id="{bid}">'
            f'<h2 class="d sect">{esc(heading)}</h2>'
            f'<div class="acct">{inner}</div>'
            + (f'<aside class="amt">{margin}</aside>' if margin else '')
            + (f'<div class="full">{full}</div>' if full else '')
            + '</section>')


def stage_key(moves):
    """The five Stages, together, with their Move ranges. Shown together they
    are five colours; met one at a time on a rule they are five greys."""
    out = []
    for k in ORDER:
        rows = [m for m in moves if m['layer'] == k]
        if not rows:
            continue
        info = LAYERS[k]
        out.append(f'<li data-part="{info["key"]}"><i></i>{esc(info["label"])}'
                   f'<b>{rows[0]["num"]}&ndash;{rows[-1]["num"]}</b></li>')
    return f'<ul class="key" aria-label="The five stages">{"".join(out)}</ul>'


def mg_note(label, body):
    """A margin note. The callouts that used to interrupt the account."""
    return (f'<div class="mg-note"><span class="lbl">{esc(label)}</span>{body}</div>')


# ------------------------------------------------------------- 1. the guide
def why_facts(T):
    """Every figure the case-for-leaving section quotes, computed here so it
    cannot drift from the cost page - they are literally the same numbers."""
    FY = COSTS.five_year(REFERENCE['nodes'], REFERENCE['spares'], T['retained'])
    own = FY['rows'][2]
    return {
        'five_year_saved': mny(own['saved']),
        'five_year_pct': f'{own["pct"]:.0f}',
        'egress_100tb': mny(COSTS.egress_month(100)),
        'weeks': f'{T["weeks"]:.0f}',
        'days': f'{T["days"]:.0f}',
        'cloud_hours': COSTS.PEOPLE['cloud_ops_hours_month'],
        'retained': mny(T['retained']),
    }


def why_section(T):
    """The case for leaving: what you gain, what it costs, and when not to.

    The three lists are one component - an ordinal, a heading, a paragraph -
    which is the same shape the safety page's points and the rules use, so a
    reader who has met one has met all three."""
    f = why_facts(T)
    # Every claim carries the test that would disprove it. That is what keeps
    # this section from being an advertisement: a page that tells the reader
    # how to prove it wrong is not selling them anything, and this audience
    # believes a falsifiable claim and distrusts a confident one.
    gains = ''.join(
        f'<li class="pt"><b class="n">{i + 1:02d}</b><div>'
        f'<h3>{esc(h)}</h3><p>{inline(b)}</p>'
        f'<p class="chk"><span class="lbl">Check it</span>{inline(c)}</p>'
        f'</div></li>'
        for i, (h, b, c) in enumerate(WHY.gains(f)))
    ours = ''.join(
        f'<li><b>{esc(n)}</b><span>{esc(t)}</span></li>' for n, t in WHY.OURS)
    costs = ''.join(
        f'<li class="pt"><b class="n">{i + 1:02d}</b><div>'
        f'<h3>{esc(h)}</h3><p>{inline(b)}</p></div></li>'
        for i, (h, b) in enumerate(WHY.costs(f)))
    stay = ''.join(f'<li>{inline(x)}</li>' for x in WHY.STAY)
    return (
        f'<p class="lede">{inline(WHY.lede(f))}</p>'
        f'<h3 class="d sub-h">{esc(WHY.OURS_HEADING)}</h3>'
        f'<ul class="ours">{ours}</ul>'
        f'<p class="note">{esc(WHY.OURS_NOTE)}</p>'
        f'<ol class="pts">{gains}</ol>'
        f'<h3 class="d sub-h">{esc(WHY.COSTS_HEADING)}</h3>'
        f'<p>{esc(WHY.COSTS_LEDE)}</p>'
        f'<ol class="pts">{costs}</ol>'
        f'<h3 class="d sub-h">{esc(WHY.STAY_HEADING)}</h3>'
        f'<ul class="onramp stay">{stay}</ul>'
        f'<p class="callout">{esc(WHY.CLOSER)}</p>')


def build_index(moves, T):
    by = {m['num']: m for m in moves}
    first = moves[0]

    # The whole plan, on one page. Stage by stage, and every Move a link with
    # the three facts that decide whether it is this week's job: what it costs
    # in labour, how badly it can go, and whether anybody notices.
    blocks = []
    for k in ORDER:
        rows = [m for m in moves if m['layer'] == k]
        if not rows:
            continue
        info = LAYERS[k]
        items = ''.join(
            f'<li><a href="m/{page(m)}">'
            f'<b class="mv-n">{m["num"]}</b>'
            f'<span class="mv-t">{esc(m["title"])}</span>'
            f'<span class="mv-h">{inline(m["hook"])}</span>'
            f'<span class="mv-f"><i><span>Effort</span> <b>{esc(m["figures"][4])}</b></i> '
            f'<i><span>Risk</span> <b>{esc(m["risk"])}</b></i> '
            f'<i><span>Cutover</span> <b>{downtime(m)}</b></i></span></a></li>' for m in rows)
        blocks.append(
            f'<li class="stage" data-part="{info["key"]}">'
            f'<div class="stage-head">'
            f'<span class="lbl">{esc(info["roman"])}</span>'
            f'<h3 class="d">{esc(info["label"])}</h3>'
            f'<p class="stage-do">{esc(info["doing"])}</p>'
            f'<p class="stage-done"><span class="lbl">Done when</span> '
            f'{esc(info["done"])}</p></div>'
            f'<ol class="mv">{items}</ol></li>')

    # The symptom index, whole. It used to be a page of its own reached from a
    # footer; it is six lines of markup and it is how the question actually
    # arrives, so it belongs where the reader lands.
    symps = ''.join(
        f'<li><span class="symp-q">{esc(q)}</span><span class="symp-a">'
        + ' '.join(f'<a href="m/{page(by[n])}" aria-label="Move {n} &middot; '
                   f'{attr(by[n]["title"])}">{n}</a>'
                   for n in ns.split() if n in by)
        + '</span></li>' for q, ns in SYMPTOMS)

    # Said only when there is something to say: an edition in which every Move
    # can be undone should not print a nought and make the reader wonder.
    oneway_line = (f', and {T["oneway"]} of them cannot be undone'
                   if T['oneway'] else ', and every one of them can be undone')
    # THE LIST IS NOT PROSE, so it does not live in the account. Twenty rows of
    # number, title, hook and three mono facts is a datasheet - the same class of
    # object as the twenty and the roadmap, and both of those already take the
    # full track. Set in the 544px account under a 1056px rule it was half a
    # page wide, and its own hook column resolved to LITERALLY ZERO pixels at
    # every desktop width: one of the three facts the site's primary navigation
    # carries was invisible, while its three clamped empty lines still set the
    # height of all twenty rows.
    #
    # The strip goes first. It is the one-screen picture of what the list says at
    # length, and it used to render three thousand pixels BELOW the detail it
    # introduces, with its own colour key another three thousand above that.
    plan_full = twenty(moves) + f'<ol class="stages">{"".join(blocks)}</ol>'

    crews = ', '.join(
        f'{w} engineer{"" if w == 1 else "s"} about {T["crew_weeks"][w]:.0f} weeks'
        for w in CREWS if w in T['crew_weeks'])

    body = f"""{bar(0, first, 'index.html')}
<main id="main" class="shell">
{hero_index(T, first)}

{band('plan', 'The whole plan, on one page',
      f'<p>{len(T["stages"])} stages, run in order, and every dependency points at a '
      f'lower number. '
      f'{T["zero"]} of the {T["n"]} Moves plan for zero downtime; the reference '
      f'cutovers total {T["cutover"]} minutes{oneway_line}. These estimates depend '
      f'on each Move\'s prerequisites and a timed rehearsal.</p>',
      margin=stage_key(moves)
      + mg_note('The shape of it',
                'Data handoffs and the final edge change need measured windows. '
                'VM migrations and services that cannot meet a zero-downtime '
                'Move\'s conditions need separately priced and rehearsed plans.'),
      full=plan_full)}

{band('where', 'Start where it hurts',
      f'<p>Nobody sits down at nine in the morning thinking in stages. Find the line '
      f'that sounds like your week and go straight to the Move.</p>',
      margin=mg_note('If none of these is you',
                     f'That is an answer too. Move 03 gives you permission to do the '
                     f'arithmetic and stop. Finish the sampling window before '
                     f'committing money; a decision to stay avoids running two '
                     f'estates without a defensible saving.'),
      full=f'<ul class="symp">{symps}</ul>')}

{band('why', WHY.HEADING, why_section(T),
      margin=f'<p class="lbl">What is at stake</p>'
      f'<dl class="bal-l">'
      f'<div><dt>Over five years</dt><dd>{mny(T["five_year"]["rows"][2]["saved"])}</dd></div>'
      f'<div><dt>Additional ops hours</dt>'
      f'<dd>{COSTS.PEOPLE["owned_ops_hours_month"] - COSTS.PEOPLE["cloud_ops_hours_month"]}</dd></div>'
      f'<div><dt>Days of work</dt><dd>{T["days"]:.0f}</dd></div>'
      f'</dl>'
      + mg_note('Two routes to metal',
                'Rent dedicated servers to preserve cash, or colocate hardware you '
                'own. <a href="cost.html">Compare the purchase costs and monthly '
                'bills &rarr;</a>'))}

{band('how-long',
      'How long it takes',
      f'<p>The labour is about {T["days"]:.0f} person-days. With {DEFAULT_CREW} '
      f'engineers it lands in roughly {T["weeks"]:.0f} weeks, and the shortest it '
      f'could possibly take, with as many people as you care to put on it, is '
      f'{T["critical_weeks"]:.0f} weeks under these estimates. Limited staffing adds '
      f'contention for engineers. Even unlimited staffing cannot remove the ordered '
      f'work, circuit orders, hardware lead times and observation windows on the '
      f'critical path. Calendar waits consume no engineer-days.</p>'
      ,
      margin=f'<p class="lbl">However many people you put on it</p>'
      f'<dl class="bal-l">'
      + ''.join(f'<div><dt>{w} engineer{"" if w == 1 else "s"}</dt>'
                f'<dd>{T["crew_weeks"][w]:.0f} wk</dd></div>'
                for w in CREWS if w in T['crew_weeks'])
      + f'<div class="tot"><dt>Unlimited</dt>'
        f'<dd>{T["critical_weeks"]:.0f} wk</dd></div></dl>'
      + mg_note('Why it barely moves',
                'Extra engineers help where independent work can overlap. They '
                'cannot remove procurement or observation waits, or start a '
                'dependent Move before its prerequisites finish.'),
      full=RM.svg(moves, DEFAULT_CREW, w=SITE_TRACK, href=lambda m: 'm/' + page(m))
      + f'<p class="note">One bar per Move, drawn from each Move&rsquo;s own effort '
        f'figure and the dependency graph rather than from a plan somebody typed. The '
        f'outlined bars are the critical path.</p>')}
</main>
{foot(0)}"""
    (SITE / 'index.html').write_text(shell(
        f'{IMP.TITLE} \u2014 the whole plan', body, 0,
        f'{T["n"]} Moves in five stages that take a company off AWS, Google Cloud or '
        f'Azure and onto hardware it owns.'), encoding='utf-8')


# ------------------------------------------------------------ 2. what it costs
def cost_bars(rows, unit='a month'):
    """Three totals, one scale, drawn rather than charted.

    The point is a comparison a reader can check in their head, so there are no
    gridlines, no axis and no legend inside the drawing. Each bar is two
    segments - the metal, then the salaried time - because the salary is the
    whole argument and hiding it inside a total is what makes a repatriation
    look better on a slide than it turns out to be.

    THREE SEGMENTS, not two: the metal, the salaried time, and what stays on
    somebody else's invoice whatever you do. The third one is the one this
    chart used to omit, and omitting it is how a comparison flatters itself.

    THE DATUM is the first row, and it is what this chart is for. A dashed rule
    stands at today's bill and runs the height of the drawing, and every row
    below it carries a measured gap from where its bar stops to where that rule
    is, labelled with what the gap is worth. Three bars of different lengths
    ask the reader to do the subtraction; a bar, a gap and a figure in the gap
    have already done it. It is also the honest way round: the gap is drawn as
    an absence rather than as a fourth bar of "savings", because a saving is
    not a thing you have, it is a thing you have stopped paying for.

    Colours come from CSS rather than from here: the site has a dark theme and a
    hex written into an SVG cannot follow it."""
    if not rows:
        return ''
    W, PAD, ROW, BAR = 700, 120, 62, 22
    top = max(sum(r[1:]) for r in rows) or 1
    scale = (W - PAD) / top
    datum = sum(rows[0][1:])                 # the first row IS the comparison
    dx = datum * scale
    H = len(rows) * ROW
    out = []

    # The datum rule first, so every bar and every figure sits on top of it.
    out.append(f'<line class="cost-d" x1="{dx:.1f}" y1="6" x2="{dx:.1f}" y2="{H - 10}"/>')

    for k, row in enumerate(rows):
        label, infra, people = row[0], row[1], row[2]
        kept = row[3] if len(row) > 3 else 0
        y = k * ROW
        wi, wp, wk = infra * scale, people * scale, kept * scale
        end = wi + wp + wk
        gap = dx - end
        # `--i` is the row's place in the chart, and the only thing the
        # stylesheet needs in order to draw the bars in reading order
        # rather than all at once. It is a number, not a duration: the
        # timing belongs in the CSS with the rest of the timing.
        out.append(f'<text class="cost-l" x="0" y="{y + 11}">{esc(label)}</text>')
        # THE TWO SEGMENTS ARE ONE GROUP, and the group is what the
        # stylesheet grows. Scaling each rect from its own left edge
        # tears the bar: the salaried segment starts at x=wi, so while
        # the metal segment is still short the two of them are drawing
        # with a widening gap between them, for the whole of the
        # animation. One group, one transform, and the segments keep
        # their relationship at every frame of it.
        out.append(f'<g class="cost-bar" style="--i:{k}">')
        out.append(f'<rect class="cost-i" x="0" y="{y + 20}" '
                   f'width="{wi:.1f}" height="{BAR}"/>')
        if wp > 0:
            out.append(f'<rect class="cost-p" x="{wi:.1f}" '
                       f'y="{y + 20}" width="{wp:.1f}" height="{BAR}"/>')
        if wk > 0:
            out.append(f'<rect class="cost-k" x="{wi + wp:.1f}" '
                       f'y="{y + 20}" width="{wk:.1f}" height="{BAR}"/>')
        out.append('</g>')
        out.append(f'<text class="cost-v" style="--i:{k}" x="{end + 9:.1f}" '
                   f'y="{y + 36}">{mny(infra + people + kept)}</text>')
        # The gap, and what it is worth. Only where there is room to set the
        # figure without it colliding with the total it is measured from:
        # a label that overlaps the number it explains explains nothing.
        if gap > 150:
            saved = datum - (infra + people + kept)
            out.append(f'<rect class="cost-g" style="--i:{k}" x="{end:.1f}" '
                       f'y="{y + 20}" width="{gap:.1f}" height="{BAR}"/>')
            out.append(f'<text class="cost-s" style="--i:{k}" x="{dx - 9:.1f}" '
                       f'y="{y + 36}">&#8722;{mny(saved)} {esc(unit)}</text>')

    lab = '; '.join(f'{r[0]}, {mny(sum(r[1:]))}' for r in rows)
    return (f'<svg class="cost" viewBox="0 0 {W} {H}" width="100%" '
            f'style="height:auto;display:block" role="img" aria-label="Cost '
            f'{esc(unit)} compared against {mny(datum)}: {lab}">'
            f'{"".join(out)}</svg>')


def fy_table(fy):
    """The five-year comparison. Capital on its own line, because that is the
    line a founder actually argues about, and a residual column because every
    rent-versus-buy comparison that omits it is answering a different question
    from the one it printed."""
    heads = ['', 'Capital, day one', 'Running, a month',
             f'Total over {fy["months"] // 12} years', 'Against the cloud']
    body = []
    for r in fy['rows']:
        cap = mny(r['capex']) if r['capex'] else '&mdash;'
        against = ('&mdash;' if not r['saved']
                   else f'{mny(r["saved"])} <i>({r["pct"]:.0f}%)</i>')
        body.append(
            f'<tr{" class=" + chr(34) + "save" + chr(34) if r["key"] == "owned" else ""}>'
            f'<th scope="row">{esc(r["label"])}</th>'
            f'<td data-h="{attr(heads[1])}">{cap}</td>'
            f'<td data-h="{attr(heads[2])}">{mny(r["month"])}</td>'
            f'<td data-h="{attr(heads[3])}">{mny(r["total"])}</td>'
            f'<td data-h="{attr(heads[4])}">{against}</td></tr>')
    return ('<div class="tablewrap" tabindex="0" role="region" aria-label="Five years, '
            'three ways, a scrollable table"><table class="cmp fy"><thead><tr>'
            + ''.join(f'<th scope="col">{esc(h)}</th>' for h in heads)
            + f'</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


def build_cost(moves, T):
    by = {m['num']: m for m in moves}
    first = moves[0]
    owned, ded, bill = T['owned'], T['dedicated'], T['bill']
    FY = COSTS.five_year(REFERENCE['nodes'], REFERENCE['spares'], T['retained'])

    heads = ['Cloud now', 'Own the machines', 'Rent the machines by the month']
    cloud_people = round(COSTS.cloud_people_month())
    cloud_total = bill + cloud_people
    cmp_rows = [
        ('Infrastructure', '', [mny(bill), mny(owned['infrastructure']),
                                mny(ded['infrastructure'])]),
        # The cloud's people cost is NOT nought and this cell used to say
        # "Already in the bill", which claimed it was. An AWS invoice bills for
        # machines. Somebody still upgrades the managed cluster, rotates the
        # credentials, chases the bill and carries the pager, and leaving that
        # off the left-hand column while charging the right-hand column for its
        # own people is the mirror of the error this book argues against.
        ('People', 'people', [mny(COSTS.cloud_people_month()),
                              mny(COSTS.cloud_people_month() + owned['people']),
                              mny(COSTS.cloud_people_month() + ded['people'])]),
        # A row label goes through esc(), so it is written with a real
        # apostrophe rather than an entity - an entity here arrives on the
        # page spelled out, which is how it shipped for exactly one build.
        ("Still on somebody else's invoice", 'kept',
         ['Already in the bill', mny(owned['retained']), mny(ded['retained'])]),
        # EVERY COLUMN IS THE SUM OF ITS OWN ROWS. The cloud column carries its
        # people now, so its total is the bill PLUS them - printing the bill
        # here would put the bare bill under a column whose visible rows come
        # to more than it, which is the sloppiness this page accuses other
        # people of.
        ('Total a month', 'tot',
         [mny(cloud_total),
          mny(owned['infrastructure'] + cloud_people + owned['people']
              + owned['retained']),
          mny(ded['infrastructure'] + cloud_people + ded['people']
              + ded['retained'])]),
        ('Saved a month', 'save',
         ['&mdash;',
          mny(cloud_total - (owned['infrastructure'] + cloud_people
                             + owned['people'] + owned['retained'])),
          mny(cloud_total - (ded['infrastructure'] + cloud_people
                             + ded['people'] + ded['retained']))]),
    ]
    cmp_html = (
        '<table class="cmp"><thead><tr><th scope="col"></th>'
        + ''.join(f'<th scope="col">{esc(h)}</th>' for h in heads)
        + '</tr></thead><tbody>'
        + ''.join(
            f'<tr{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>'
            f'<th scope="row">{esc(label)}</th>'
            + ''.join(f'<td data-h="{attr(heads[i])}">{v}</td>'
                      for i, v in enumerate(vals)) + '</tr>'
            for label, cls, vals in cmp_rows)
        + '</tbody></table>')

    # Where the money goes: every Move, in book order, with the slice of the
    # bill it takes off.
    #
    # The rows sum to MORE than the headline saving, and should. This comment
    # said "less" for two editions and the prose eighty lines down said "more",
    # which is how a comment starts lying to the next person: these are LINE
    # savings, taken before the salaried time, before the whole cost of running
    # your own site, and before the retained lines the comparison puts back.
    # Some Moves buy safety rather than money and say so with an em dash; Move
    # 04 is the one that states a real zero, because it trades $1,400 for the
    # same $1,400 on purpose.
    perm_rows, tw, tn = [], 0.0, 0.0
    for m in moves:
        if m['was'] is not None and m['now'] is not None:
            tw, tn = tw + m['was'], tn + m['now']
            cells = (f'<td class="perm-v">{mny(m["was"])}</td>'
                     f'<td class="perm-v">{mny(m["now"])}</td>'
                     f'<td class="perm-v">{mny(m["was"] - m["now"])}</td>')
        else:
            cells = ('<td class="perm-v">&mdash;</td><td class="perm-v">&mdash;</td>'
                     '<td class="perm-v">&mdash;</td>')
        perm_rows.append(
            f'<tr data-part="{m["l"]["key"]}"><td class="perm-n">'
            f'<a href="m/{page(m)}">{m["num"]}</a></td>'
            f'<td class="perm-t">{esc(m["title"])}</td>{cells}</tr>')
    perm = (
        '<table class="perm"><thead><tr><th scope="col">Move</th>'
        '<th scope="col">Title</th><th scope="col">Was</th><th scope="col">Now</th>'
        '<th scope="col">Saved</th></tr></thead>'
        f'<tbody>{"".join(perm_rows)}</tbody>'
        f'<tfoot><tr><th scope="row" colspan="2">Every Move that states both</th>'
        f'<td class="perm-v">{mny(tw)}</td><td class="perm-v">{mny(tn)}</td>'
        f'<td class="perm-v">{mny(tw - tn)}</td></tr></tfoot></table>')

    eq_heads = list(EQ_CLOUDS) + ['What you run instead']
    eq_rows = ''.join(
        f'<tr{" class=" + chr(34) + "keep" + chr(34) if r[3].lower().startswith("keep paying") else ""}>'
        + ''.join(f'<td data-h="{attr(eq_heads[i])}">{esc(r[i])}</td>' for i in range(3))
        + f'<td class="eq-yours" data-h="{attr(eq_heads[3])}">{esc(r[3])}'
        + (f' <a href="m/{page(by[r[4]])}">{r[4]}</a>' if r[4] and r[4] in by else '')
        + '</td></tr>' for r in EQ_ROWS)
    eq = ('<div class="tablewrap" tabindex="0" role="region" aria-label="What replaces '
          'what, a scrollable table"><table class="eq"><thead><tr>'
          + ''.join(f'<th scope="col">{esc(h)}</th>' for h in eq_heads)
          + f'</tr></thead><tbody>{eq_rows}</tbody></table></div>')

    body = f"""{bar(0, first, 'cost.html')}
<main id="main" class="shell">
{hero('What it costs',
      f'{mny(bill)} a month becomes {mny(owned["total"])}, with the same operations '
      f'hours. That saves {mny(T["year"])} a year, or {T["pct"]:.0f} per cent of everything '
      f'you spend on it now, with {mny(T["cloud_people"])} of salary counted on both sides.',
      f'The reference build is {REFERENCE["nodes"]} machines and {REFERENCE["spares"]} '
      f'spares, in one colocation rack. Prices are dated model assumptions. Compare '
      f'your own cloud rate and provider quotes, with the existing team in every column. '
      f'{COST_SCOPE}',
      'page',
      figs([(mny(bill), 'Cloud, a month'),
            (mny(owned['total']), 'What the bill becomes'),
            (mny(T['year']), 'Saved a year'),
            (f'{T["pct"]:.0f}%', 'Off what you pay now')]))}

{band('compare', 'The comparison, with the salary in it',
      f'<p>The reference model keeps the existing operations team, monthly hours '
      f'and salary in every column, so additional staffing cost is '
      f'{mny(owned["people"])} for colocation and {mny(ded["people"])} for rented metal. '
      f'Cloud ops engineers transition into on-prem '
      f'ops: deployment, monitoring, patching and recovery remain their work. '
      f'Colocation remote hands handles contracted physical tasks, already priced '
      f'in the facility bill; rented-metal providers include hardware maintenance '
      f'in their support agreement.</p>'
      f'<p>On-premises operations roles can cost less than cloud specialist roles, '
      f'offering further salary savings. The figures here keep the existing salary '
      f'cost and count none of those potential savings. Migration effort is '
      f'budgeted separately. Use your actual staffing plan, local pay rates, '
      f'measured hours and support quotes to price any recurring difference.</p>'
      ,
      margin=mg_note('The people row',
                     f'This is the full existing salary cost, not an additional '
                     f'hire. All three columns budget '
                     f'{COSTS.PEOPLE["cloud_ops_hours_month"]} hours a month, or '
                     f'{mny(COSTS.cloud_people_month())}. The team transitions '
                     f'from cloud operations to running the on-premises platform.')
      + mg_note('Remote hands at the rack',
                'Disk swaps, cabling and power cycles can be carried out by the '
                'facility team under your runbooks. Agree coverage, response times '
                'and charges in the contract. Your engineers remain responsible '
                'for the platform and application. '
                '<a href="https://docs.equinix.com/smart-hands/">Example: Equinix '
                'Smart Hands scope &rarr;</a>')
      ,
      full=cmp_html
      + f'<p class="cost-key"><span><i class="k-i"></i>Infrastructure</span> '
        f'<span><i class="k-p"></i>Salaried time</span> '
        f'<span><i class="k-k"></i>Still rented</span></p>'
      + cost_bars([('Cloud now', bill, cloud_people, 0),
                   ('Own the machines', owned['infrastructure'],
                    cloud_people + owned['people'], owned['retained']),
                   ('Rent by the month', ded['infrastructure'],
                    cloud_people + ded['people'], ded['retained'])]))}

{band('five-years', 'Five years, three ways',
      f'<p>A month is the wrong window for this decision. Owning is capital on day one '
      f'and cheap running afterwards; renting is no capital and dearer running; the cloud '
      f'is no capital and dearest running. Compared a month at a time the capital either '
      f'vanishes into an amortisation line or sits there looking like the whole story, '
      f'and neither is what somebody signing the cheque is choosing between. So here is '
      f'the life of one generation of machines, with the salary counted on all three '
      f'sides and the capital on the line where it actually happens. These '
      f'steady-state totals exclude transition labour, overlapping cloud bills, '
      f'financing and taxes.</p>'
      ,
      margin=mg_note('Choose the cash flow',
                     'Rented metal preserves the cash you would spend buying '
                     'servers. Colocation trades that purchase for lower running '
                     'costs and ownership of the fleet. Both use the same operations '
                     'hours and salary here; potential staffing savings are '
                     'excluded. Let your runway, workload and provider quotes '
                     'decide which route fits.')
      + mg_note('The residual', 'After sixty months the '
      f'owned machines remain yours. The model credits a residual value of '
      f'{FY["rows"][2]["residual"] / FY["rows"][2]["capex"] * 100:.0f} per cent of the purchase '
      f'price; actual resale value and useful life will vary. The table includes '
      f'that credit as well as the different running costs, so compare both with '
      f'the quotes you receive.'),
      full=fy_table(FY)
      + cost_bars([('Cloud', FY['rows'][0]['total'], 0, 0),
                   ('Rented metal', FY['rows'][1]['total'], 0, 0),
                   ('Colocation', FY['rows'][2]['total'], 0, 0)],
                  unit=f'over {FY["months"] // 12} years'))}

{band('where-money', 'Where the money goes',
      f'<p>One row per Move, in the order you run them. Some Moves buy safety rather '
      f'than money and say so with a dash. The rows that state both halves come to '
      f'{mny(tw - tn)} a month, which is more than the {mny(T["save"])} at the top of '
      f'this page: these are line savings, taken before the salaried time and before '
      f'the whole cost of running your own site, both of which the comparison above '
      f'puts back in. The Now column of this table is the {mny(tn)} that stays on '
      f'somebody else&rsquo;s invoice, and it is the third row up there.</p>',
      margin=f'<p class="lbl">The Now column</p><dl class="bal-l">'
             f'<div><dt>Still somebody else&rsquo;s invoice</dt>'
             f'<dd>{mny(tn)}</dd></div>'
             f'<div class="tot"><dt>Line savings, added up</dt>'
             f'<dd>{mny(tw - tn)}</dd></div></dl>'
             + mg_note('Where it goes next',
                       f'That {mny(tn)} is the third row of the comparison above, '
                       f'and it is the one line this book tells you to keep '
                       f'paying for ever.'),
      full=perm)}

{band('replaces', 'What replaces what',
      f'<p>Find the row you are paying for, then read the Move. Where the last column '
      f'says keep paying, that is a conclusion rather than a gap: a content delivery '
      f'network, scrubbing capacity at the edge and outbound mail deliverability are '
      f'businesses somebody else already runs better than you will.</p>',
      margin=mg_note('Services retained',
                     f'{mny(T["retained"])} a month in the reference after state. '
                     f'This includes Move 04\'s edge and mail services plus '
                     f'archives, backups and other services kept by later Moves.'),
      full=eq)}

{band('onramp', 'Before you sign anything',
      f'<p>Almost nobody should sign a facility contract before they have run this '
      f'stack once. {HOMELAB["nodes"]} refurbished machines on a managed switch under a '
      f'desk cost about {mny(COSTS.homelab_capex())} once and '
      f'{mny(COSTS.homelab_month())} a month in electricity, and they run the whole of '
      f'the platform at lab scale. It saves nothing, and that is not what it is for: it is the '
      f'smallest bet that tells you whether the rest of this book is for you.</p>'
      f'<p class="note">Figures on this page combine illustrative budgets with dated '
      f'cloud list prices, not quotations. Cloud prices are on-demand and undiscounted; a '
      f'reader with a commitment discount should substitute their own effective rate, '
      f'and check the region, service tier and free allowances.</p>'
      f'<p class="callout"><span class="lbl">The rented column, with a warning</span> '
      f'The monthly rent, hardware purchase price, power and facility charges are '
      f'planning assumptions. CPU model, memory, traffic allowance, region and '
      f'support terms can change the comparison. Get matching quotes before you let this '
      f'column decide anything &mdash; Move 07 step 6 is where to do it.</p>',
      margin=f'<p class="lbl">Under a desk</p><dl class="bal-l">'
      f'<div><dt>Machines</dt><dd>{HOMELAB["nodes"]}</dd></div>'
      f'<div><dt>Cores each</dt><dd>{HOMELAB["cores_per_node"]}</dd></div>'
      f'<div><dt>Once</dt><dd>{mny(COSTS.homelab_capex())}</dd></div>'
      f'<div class="tot"><dt>A month, in power</dt>'
      f'<dd>{mny(COSTS.homelab_month())}</dd></div></dl>'
      + mg_note('What it cannot teach you',
                'The cage. One power feed, one switch, no cross-connect, and '
                'nobody else in the room at two in the morning.'))}
</main>
{foot(0)}"""
    (SITE / 'cost.html').write_text(shell(
        f'What it costs \u2014 {IMP.TITLE}', body, 0,
        f'The arithmetic: {mny(bill)} a month on the cloud becomes {mny(owned["total"])} '
        f'on machines you own, with the salary counted on both sides.'), encoding='utf-8')


# ------------------------------------------------------------- 3. the checklist
def build_checklist(moves, T):
    first = moves[0]

    # One segment per Move, carrying its own number and Stage, so the bar can be
    # painted from the ticks alone rather than from a count the page also has to
    # keep. It reads zero in the HTML, which is true for every first visit.
    segs = ''.join(f'<i data-n="{m["num"]}" data-part="{m["l"]["key"]}"></i>'
                   for m in moves)

    blocks = []
    for k in ORDER:
        rows = [m for m in moves if m['layer'] == k]
        if not rows:
            continue
        info = LAYERS[k]
        cks = ''.join(
            f'<label class="ck" data-part="{info["key"]}">'
            f'<input type="checkbox" class="ck-box" data-n="{m["num"]}" '
            f'aria-label="Mark Move {m["num"]}, {attr(m["title"])}, as done">'
            f'<b class="ck-n">{m["num"]}</b>'
            f'<a class="ck-t" href="m/{page(m)}">{esc(m["title"])}</a>'
            f'<span class="ck-f"><i>{esc(m["figures"][4])}</i><i>{esc(m["risk"])}</i>'
            f'<i>{downtime(m)}</i><i>{esc(back_out(m))}</i></span></label>'
            for m in rows)
        # The four figures are the only quantitative content on this page and
        # they were unlabelled: nothing said the third value was downtime or the
        # fourth reversibility. One heading row a Stage, on the same four tracks
        # the rows use, so the columns are named where they are read.
        head = ('<div class="ck-hd" aria-hidden="true">'
                '<span></span><span></span><span></span>'
                '<span class="ck-f lbl"><i>Effort</i><i>Risk</i><i>Downtime</i>'
                '<i>Back out</i></span></div>')
        blocks.append(
            f'<section class="stage" data-part="{info["key"]}">'
            f'<div class="stage-head"><span class="lbl">{esc(info["roman"])}</span>'
            f'<h2 class="d">{esc(info["label"])}</h2>'
            f'<p class="stage-do">{esc(info["doing"])}</p>'
            f'<p class="stage-done"><span class="lbl">Done when</span> '
            f'{esc(info["done"])}</p></div>{head}{cks}</section>')

    # The summary is rendered correct for nothing ticked and updated in place
    # afterwards. Every number in it is one the build already computed, so the
    # zero-tick state and the script agree by construction.
    summary = (
        '<div class="summary" id="summary">'
        f'<div class="sum"><b id="s-left">{T["n"]}</b>'
        f'<span class="lbl">Moves left</span></div>'
        f'<div class="sum"><b id="s-days">{T["days"]:.0f}</b>'
        f'<span class="lbl">Days of work left</span></div>'
        # Weeks of LABOUR, not the elapsed schedule. Ticking a Move removes
        # somebody's days from the pile; it does not shorten a circuit order or
        # a thirty-day window, and the elapsed figure on the front page is
        # mostly made of those. A counter that fell as you ticked would be
        # promising an end date that ticking cannot move.
        f'<div class="sum"><b id="s-weeks">'
        f'{T["days"] / DEFAULT_CREW / RM.WEEK:.0f}</b>'
        f'<span class="lbl">Weeks of work left, {DEFAULT_CREW} engineers</span></div>'
        f'<div class="sum"><b id="s-save">{mny(T["stated"])}</b>'
        f'<span class="lbl">A month still on the table</span></div>'
        '</div>')

    # Named only when there is something to name. An edition in which nothing is
    # one-way would otherwise print "which of the 0 Moves you cannot undo".
    oneway_note = (f' {T["oneway"]} of them cannot be undone, and the safety page says '
                   f'which.' if T['oneway'] else '')
    body = f"""{bar(0, first, 'checklist.html')}
<main id="main" class="shell">
{hero('Your checklist',
      'Work down it in order. Every dependency points at a lower number, so the order '
      'on this page is already a plan you can run.',
      'Ticks are kept in this browser and go nowhere else. Use the link button to put '
      'them in the address bar if you want to send the state to somebody.',
      'page',
      f'<div class="prog"><b id="p-done">0</b> of {T["n"]} done</div>'
      f'<div class="prog-bar" id="prog-bar" aria-hidden="true">{segs}</div>')}

{"".join(blocks)}

{summary}

<p class="actions">
  <button class="btn" type="button" id="ck-reset">Clear every tick</button>
  <button class="btn ghost" type="button" id="ck-share">Copy a link to this</button>
  <span class="lbl" id="ck-said" role="status"></span>
</p>
<p class="note">With {T["n"]} Moves in a fixed order there is nothing to plan around:
the order is the plan. What this page adds is where you got to, what is left of the
work, and what is still on the bill.{oneway_note}</p>
</main>
{foot(0)}"""
    (SITE / 'checklist.html').write_text(shell(
        f'Your checklist \u2014 {IMP.TITLE}', body, 0,
        f'All {T["n"]} Moves in order, with a tick box each and a running count of the '
        f'work and the saving left.'), encoding='utf-8')


# --------------------------------------------------------- 4. before you start
def worksheet_templates(moves):
    """The print records as copyable prompts, without storing operational data."""
    intro = (f'<p>{esc(WS.INTRO)}</p>'
             '<ul>' + ''.join(
                 f'<li><a href="#{s["id"]}">{esc(s["title"])}</a></li>'
                 for s in WS.TEMPLATES) + '</ul>')
    by_number = {m['num']: m for m in moves}
    def source(ref):
        return (f'<p class="note"><a href="m/{page(by_number[ref["move"]])}">'
                f'{esc(ref["source"])}</a></p>')
    records = []
    for sheet in WS.records(moves):
        records.append(
            f'<section id="{sheet["id"]}"><h3 class="d sub-h">{esc(sheet["title"])}</h3>'
            f'<p>{inline(sheet["purpose"]["text"])}</p>'
            + source(sheet['purpose']) + '<ul>'
            + ''.join(f'<li>{esc(label)}:</li>' for label in WS.RECORD_FIELDS)
            + '</ul><ol class="pts">'
            + ''.join(f'<li class="pt"><b class="n">{i:02d}</b><div>'
                      f'<h4>{esc(field["label"])}</h4><p>{inline(field["text"])}</p>'
                      + source(field) + '</div></li>'
                      for i, field in enumerate(sheet['fields'], 1))
            + '</ol></section>')
    return intro + ''.join(records)


def build_start(moves, T):
    first = moves[0]

    pts = ''.join(
        f'<li class="pt"><b class="n">{i + 1:02d}</b><div>'
        f'<h3>{esc(t)}</h3><p>{esc(b)}</p></div></li>'
        for i, (t, b) in enumerate(RB_POINTS))

    rules = ''.join(
        f'<li><b class="n">{i + 1:02d}</b><div>'
        f'<h3>{esc(t)}</h3><p>{esc(b)}</p></div></li>'
        for i, (t, b) in enumerate(RULES))

    # Tick boxes on a shopping list, keyed by shelf and position so a reordered
    # shelf does not silently move somebody's ticks onto different items.
    shelves = ''.join(
        f'<div class="shelf"><h3 class="d">{esc(name)}</h3><ul>' + ''.join(
            f'<li><label class="kt"><input type="checkbox" class="kt-box" '
            f'data-kit="{attr(re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"))}-{j}">'
            f'<span>{esc(i)}</span></label></li>' for j, i in enumerate(items))
        + '</ul></div>' for name, items in SHELVES)

    body = f"""{bar(0, first, 'start.html')}
<main id="main" class="shell">
{hero('Before you start',
      'Three things to read before step one: how to get back, the rules the whole book '
      'rests on, and what to buy.',
      'This is the most important page here. Everything else costs money when it goes '
      'wrong; this costs data.')}

{band('safety', 'How to get back',
      f'<p>{esc(rb_intro(T["oneway"]))}</p>'
      f'<ol class="pts">{pts}</ol>',
      margin=mg_note('What this page is not', esc(RB_DISC))
      + '<p class="mg-x-w"><a class="mg-x" href="#worksheets">'
        'Operator worksheets &rarr;</a></p>'
      + f'<p class="mg-x-w"><a class="mg-x" href="checklist.html">'
        f'Your checklist &rarr;</a></p>')}

{band('rules', 'The rules',
      f'<p>{len(RULES)} of them: the spine of the argument, and what survived being '
      f'rewritten for a company with two engineers rather than twenty.</p>'
      f'<ol class="rules">{rules}</ol>',
      margin=mg_note('They are not advice',
                     'Every one of them is enforced somewhere in the build or '
                     'stated as a precondition in a runbook. A rule nobody '
                     'checks is a preference.')
      + f'<p class="mg-x-w"><a class="mg-x" href="index.html#plan">'
        f'The whole plan &rarr;</a></p>')}

{band('kit', 'What to buy',
      f'<p>Every Move is written against one cluster, so a runbook can name a real '
      f'thing rather than a category: {REFERENCE["nodes"]} nodes and '
      f'{REFERENCE["spares"]} spare in one cage, {REFERENCE["cores_per_node"]} cores and '
      f'{REFERENCE["ram_gb_per_node"]} GB a node, on a '
      f'{REFERENCE["uplink_gbps"]} GbE uplink. Scale the numbers; do not scale away the '
      f'redundancy. Tick it off against a quote.</p>'
      f'<p>{esc(PLATFORM_SCOPE)}</p>'
      f'<div class="shelves">{shelves}</div>'
      f'<h3 class="d sub-h">On the laptop of whoever is running a Move</h3>'
      f'<ul class="tools">'
      + ''.join(f'<li>{esc(t)}</li>' for t in KIT) + '</ul>'
      f'<h3 class="d sub-h">The on-ramp, under a desk</h3>'
      f'<p>{HOMELAB["nodes"]} refurbished machines, {HOMELAB["cores_per_node"]} cores '
      f'and {HOMELAB["ram_gb_per_node"]} GB each, let you rehearse your platform for about '
      f'{mny(COSTS.homelab_capex())} once and {mny(COSTS.homelab_month())} a month in '
      f'electricity. What it cannot teach you is the cage: one power feed, one switch, '
      f'no cross-connect.</p>'
      f'<ul class="onramp">'
      + ''.join(f'<li>{esc(k)}</li>' for k in HOMELAB_KIT) + '</ul>',
      margin=f'<p class="lbl">The reference build</p><dl class="bal-l">'
      f'<div><dt>Nodes</dt><dd>{REFERENCE["nodes"]}</dd></div>'
      f'<div><dt>On the shelf</dt><dd>{REFERENCE["spares"]}</dd></div>'
      f'<div><dt>Cores a node</dt><dd>{REFERENCE["cores_per_node"]}</dd></div>'
      f'<div><dt>GB a node</dt><dd>{REFERENCE["ram_gb_per_node"]}</dd></div>'
      f'<div class="tot"><dt>Uplink</dt>'
      f'<dd>{REFERENCE["uplink_gbps"]} GbE</dd></div></dl>'
      + mg_note('Scale the numbers, not the redundancy',
                'A spare on the shelf and a second of everything that carries '
                'state are what the runbooks assume. Halve those and the '
                'rollbacks stop working.'))}
{band('worksheets', WS.HEADING, worksheet_templates(moves))}
</main>
{foot(0)}"""
    (SITE / 'start.html').write_text(shell(
        f'Before you start \u2014 {IMP.TITLE}', body, 0,
        'How to roll back, the rules the book rests on, and the reference build to '
        'quote against.'), encoding='utf-8')


# ------------------------------------------------------------------- 5. about
def build_about(moves, T):
    first = moves[0]
    pp = pdf_pages()

    # The page count is derived from the PDF and is stable; the FILE SIZE is not,
    # and it used to be printed here. Both artefacts carry a build timestamp, so
    # they are excluded from the committed-site check in CI - and a size read off
    # their bytes and written into this page walked straight past that exclusion,
    # so the check failed on a rebuild that had changed nothing. A number nobody
    # reads is not worth a red build.
    dls = []
    if PDF_SRC.exists():
        dls.append(
            f'<a class="dl" href="{PDF_NAME}" download><b class="dl-t">The print '
            f'interior</b><span class="dl-m">PDF'
            + (f' &middot; {pp} pages' if pp else '')
            + ' &middot; 8.25 x 11 in</span></a>')
    if EPUB_SRC.exists():
        dls.append(
            f'<a class="dl" href="{EPUB_NAME}" download><b class="dl-t">The Kindle '
            f'edition</b><span class="dl-m">EPUB &middot; reflowable &middot; '
            f'{T["n"]} Moves</span></a>')

    # Version, text and software are in the footer of this and every other
    # page now, so the about page states what only it can: the shape of the
    # book. Printing the same three facts twice on one screen is the thing
    # this repository's fourth gate exists to catch.
    colophon = ''.join(f'<div><dt class="lbl">{esc(k)}</dt><dd>{v}</dd></div>'
                       for k, v in [
                           ('Moves', T['n']),
                           ('Stages', len(T['stages'])),
                           ('Interior', f'{pp} pages' if pp else 'PDF')])

    body = f"""{bar(0, first, 'about.html')}
<main id="main" class="shell">
{hero(esc(' '.join(MISSION.HEADING_LINES)),
      'A handbook, not an argument. The argument has been had.',
      esc(MISSION.KICKER))}

<section class="band led" id="why">
<div class="acct prose">{''.join(
    f'<p>{p}</p>' for p in MISSION.paras(f'<a href="{GH_URL}">{IMP.REPO}</a>', T['n']))}</div>
<aside class="amt">{mg_note('The interest, declared',
  'The author founded OneUptime, which Stage 5 recommends. That is stated on '
  'the copyright page, in the colophon, in the Kindle edition and further down '
  'this page.')}</aside>
</section>

{band('download', 'Take it with you',
      f'<p>The same {T["n"]} Moves, typeset. The print interior is the one to read on '
      f'paper beside a rack; the Kindle edition reflows.</p>'
      f'<div class="dls">{"".join(dls)}</div>',
      margin=mg_note('Both editions are the same Moves',
                     'One markdown source, three renderers. Nothing is written '
                     'for the web and cut for print, or the other way round.')
      if dls else
      '<p>The print interior and the Kindle edition are built by <code>make '
      'artefacts</code> and are not in this copy of the site.</p>')}

{band('made', 'How it is made',
      f'<p>{T["n"]} markdown files are the whole book. A Python toolchain turns them '
      f'into a print interior, an EPUB and this site, and every number in any of them '
      f'&mdash; page numbers, totals, the schedule on the front page, the arithmetic '
      f'on the cost page &mdash; is derived from those files rather than typed. Two gates run '
      f'before anything is published: one checks the shape of every Move, including '
      f'that no Move which moves persistent state ships without saying how the state '
      f'comes back, and the other checks the content.</p>'
      f'<p>The most valuable contribution is a correction. If you ran a runbook and it '
      f'did not work as written, or a price is wrong for your region, that is worth an '
      f'issue on its own. <a href="{GH_URL}/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a> '
      f'has the shape a Move has to satisfy.</p>'
      f'<p class="actions"><a class="btn" href="{GH_URL}">View the repository</a> '
      f'<a class="btn ghost" href="{GH_URL}/blob/main/CONTRIBUTING.md">Add a Move</a></p>',
      margin=mg_note('The two gates',
                     'One checks the shape of every Move, including that nothing '
                     'which moves persistent state ships without saying how the '
                     'state comes back. The other checks the content. Both must '
                     'report nothing before anything is published.')
      + f'<p class="mg-x-w"><a class="mg-x" '
        f'href="{GH_URL}/blob/main/CONTRIBUTING.md">How to add a Move &rarr;</a></p>')}

{band('disclosure', 'Disclosure',
      f'<p class="callout">{esc(IMP.DISCLOSURE)}</p>')}

{band('licence', 'Two licences',
      f'<p>{esc(IMP.LICENCE)}</p>'
      f'<dl class="colo">{colophon}</dl>',
      margin=mg_note('Set in two families',
                     f'{esc(IMP.TYPE_NOTE)} Written by {esc(IMP.AUTHOR)} and '
                     f'published by {esc(IMP.PUBLISHER)}. '
                     f'{esc(IMP.DISCLAIMER)}'))}
</main>
{foot(0)}"""
    (SITE / 'about.html').write_text(shell(
        f'About \u2014 {IMP.TITLE}', body, 0,
        'Why the book exists, how it is built, where to download it, and how to '
        'correct it.'), encoding='utf-8')


# ------------------------------------------------------------------- one Move
def build_move(m, prev, nxt, by, moves, T):
    """The thing you DO comes first.

    Runbook, then what you need for it, then everything that is read rather than
    run. The previous edition put four screens of reference above the steps,
    which is the wrong way round for a page somebody has open beside a terminal.
    """
    c = m['l']
    idx = moves.index(m) + 1

    steps = ''.join(
        f'<li><span class="sn" data-step="{i + 1}">{i + 1}</span>'
        f'<div>{inline(s)}</div></li>' for i, s in enumerate(m['steps']))

    pre = ''.join(
        '<div class="pre-g">'
        + (f'<h3 class="lbl">{inline(g["name"])}</h3>' if g['name'] else '')
        + '<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in g['items'])
        + '</ul></div>' for g in m['pre_groups'])

    clouds = ''.join(
        f'<li data-cloud="{o["key"]}"><b>{esc(o["cloud"])}</b>'
        f'<span class="svc">{inline(o["service"])}</span>'
        f'<span class="dif">{inline(o["note"])}</span></li>' for o in m['origins'])

    notes = ''.join(f'<div><dt>{inline(t)}</dt><dd>{inline(b)}</dd></div>'
                    for t, b in m['notes'])

    # THREE, not six. The Move contract makes the strip six cells and forces
    # the cutover cell to equal the meta line exactly, so Cutover, Effort and
    # Wait were byte-identical to three of the six facts at the top of this
    # same page - the same figures printed twice on one screen, against the
    # rule that a figure belongs on the page whose question it answers and
    # nowhere else. What is left is the trade: what the line was, what it is,
    # and the difference. The parse contract is untouched; this is a display
    # choice, and the other three are still on the page, in the vitals.
    labels = ['Was', 'Now', 'Saved']
    nums = ('<table class="nums"><thead><tr>'
            + ''.join(f'<th scope="col">{l}</th>' for l in labels)
            + '</tr></thead><tbody><tr>'
            + ''.join(f'<td>{esc(v)}</td>' for v in m['figures'][:3])
            + '</tr></tbody></table>')

    # Six facts, always six, in a fixed order. A cell whose answer is an em dash
    # is still an answer - "no wait" is a fact about this Move - and a grid that
    # changes shape from Move to Move cannot be read at a glance.
    facts = ''.join(f'<div><dt class="lbl">{k}</dt><dd>{v}</dd></div>' for k, v in [
        ('Cutover', f'{m["cutover"]} min'),
        ('Risk', f'{esc(m["risk"])} {risk_bars(m["risk"], "currentColor", "1em")}'),
        ('Effort', esc(m['figures'][4])),
        ('Then wait', esc(m['figures'][5])),
        ('Back out', esc(back_out(m))),
        ('Leaving', esc(m['leaving'])),
    ])

    def deplinks(items, label, cls):
        if not items:
            return ''
        return (f'<p class="{cls}">{label} ' + ' '.join(
            f'<a href="{page(p)}" aria-label="Move {p["num"]} &middot; '
            f'{attr(p["title"])}">{p["num"]}</a>' for p in items) + '</p>')

    # A slot each, labelled, with the Move number in mono. It was two
    # unlabelled captions at opposite ends of a thousand pixels, and on Move 01
    # the only survivor was thrown to the right-hand edge with the left half of
    # the row empty. This is the only way forward for somebody working the book
    # in order.
    def pnl(cls, rel, mv, label):
        return (f'<a class="{cls}" rel="{rel}" href="{page(mv)}">'
                f'<span class="lbl">{label}</span>'
                f'<b>{mv["num"]}</b><span class="pt-t">{esc(mv["title"])}</span></a>')

    pn = ((pnl('prev', 'prev', prev, 'Previous') if prev else '<span></span>')
          + (pnl('nxt', 'next', nxt, 'Next') if nxt else ''))

    # THE HEADER POINTS FORWARD. bar() renders the lowest-numbered Move as the
    # `next` link, which is right on every other page and wrong here: on Move 01
    # with nothing ticked - the state of every first-time reader - it pointed at
    # the page it was sitting on. The book's own next Move is the correct
    # no-script answer, and app.js substitutes a later one when there is one.
    body = f"""{bar(1, nxt or m)}
<main id="main" class="shell">
<article class="move" data-part="{c['key']}">
  <header class="mh">
    <p class="lbl">{esc(c['roman'])} &middot; {esc(c['label'])} &middot; Move {m['num']} of {T['n']}</p>
    <h1 class="d page">{esc(m['title'])}</h1>
    <p class="hook">{inline(m['hook'])}</p>
  </header>

  <section class="sec led"><h2 class="d sect">The runbook</h2>
    <div class="acct"><ol class="steps" data-n="{m['num']}">{steps}</ol></div>
    <aside class="amt vitals" aria-label="This Move at a glance">
      <dl class="facts">{facts}</dl>
      {deplinks(dep_needs(m['num'], by), 'Needs', 'needs')}
    </aside></section>

  <section class="sec led"><h2 class="d sect">Before you start</h2>
    <div class="full"><div class="pre">{pre}</div></div></section>

  <section class="sec led"><h2 class="d sect">What you are leaving</h2>
    <div class="full"><ul class="clouds">{clouds}</ul></div></section>

  <section class="sec led"><h2 class="d sect">Why this works</h2>
    <div class="acct"><p>{inline(m['why'])}</p></div>
    <aside class="amt">{deplinks(dep_unlocks(m['num'], by), 'Unlocks', 'unlocks')}</aside>
  </section>

  <section class="sec led"><h2 class="d sect">Operator&rsquo;s notes</h2>
    <div class="full"><dl class="notes">{notes}</dl></div></section>

  <section class="sec led warn"><h2 class="d sect">Rollback</h2>
    <div class="acct"><p>{inline(m['rollback'])}</p></div>
    <aside class="amt">{mg_note('Back out', esc(back_out(m)))}</aside></section>

  <section class="sec led"><h2 class="d sect">The numbers</h2>
    <div class="full">{nums}
    <p class="turnoff"><span class="lbl">What you can turn off</span>
      {inline(m['turnoff'])}</p></div></section>

  <footer class="mf">
    <label class="ck big"><input type="checkbox" class="ck-box" data-n="{m['num']}">
      Mark Move {m['num']} as done</label>
    <nav class="pn" aria-label="Moves">{pn}</nav>
  </footer>
</article>
</main>
{foot(1)}"""
    (SITE / 'm' / page(m)).write_text(shell(
        f'{m["num"]} \u00b7 {m["title"]} \u2014 {IMP.TITLE}', body, 1, m['hook']),
        encoding='utf-8')

    # The numeric address. `m/16.html` is typeable, speakable over a phone in a
    # datacentre, and resolves with no script at all - the refresh does the work
    # and the link in the body catches anybody whose browser refuses it.
    redirect = (
        f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8">\n'
        f'<title>{esc(m["num"])} \u00b7 {esc(m["title"])}</title>\n'
        f'<link rel="canonical" href="{page(m)}">\n'
        f'<meta http-equiv="refresh" content="0;url={page(m)}">\n'
        f'</head><body><a href="{page(m)}">Move {esc(m["num"])} &mdash; '
        f'{esc(m["title"])}</a></body></html>\n')
    aliases = [f'{m["num"]}.html']
    # Keep published bookmarks working when a Move is retitled.
    if m['num'] == '11':
        aliases.append('11-a-cluster-in-an-afternoon.html')
    for alias in aliases:
        (SITE / 'm' / alias).write_text(redirect, encoding='utf-8')
    return idx


# ---------------------------------------------------------------- build gates
# A scheme, or a protocol-relative URL: not ours to resolve.
EXTERNAL = re.compile(r'^(?:[a-z][a-z0-9+.\-]*:|//|#?$)', re.I)


def check_links():
    """Every internal link must land on a file that exists, and every fragment
    on an id that exists.

    A dead link is invisible to every other check in this repository: the page
    builds, the link renders, and the reader arrives at a 404 or at the top of a
    document wondering what they missed. Both halves matter - checking only the
    fragments would have inspected about one link in seventy."""
    ids, bad = {}, []
    for f in SITE.rglob('*.html'):
        ids[f.resolve()] = set(re.findall(r'\sid="([^"]+)"', f.read_text(encoding='utf-8')))
    for f in sorted(SITE.rglob('*.html')):
        for href in re.findall(r'href="([^"]*)"', f.read_text(encoding='utf-8')):
            if EXTERNAL.match(href):
                continue
            p, _, frag = href.partition('#')
            p = p.partition('?')[0]            # the asset cache-buster
            target = (f.parent / p).resolve() if p else f.resolve()
            if not target.exists():
                bad.append(f'{f.relative_to(SITE)} -> {href} (no such file)')
            elif frag and target.suffix == '.html' and frag not in ids.get(target, ()):
                bad.append(f'{f.relative_to(SITE)} -> {href} (no such id)')
    return bad


def main():
    moves = load_all()
    if not moves:
        sys.exit('site: no Move files in moves/ yet')
    if SITE.exists():
        shutil.rmtree(SITE)

    # One page per Move, and the number is in the filename, so two Moves that
    # slug alike no longer overwrite each other. They are still forbidden:
    # verify.py rejects duplicate titles, and two addresses that differ only by
    # a number nobody reads is a URL scheme that cannot be dictated over a
    # phone. The assertion is here because this is where the damage lands.
    collisions = {}
    for m in moves:
        collisions.setdefault(slug(m), []).append(m['num'])
    clash = {s: ns for s, ns in collisions.items() if len(ns) > 1}
    assert not clash, f'moves share a slug and are indistinguishable in a URL: {clash}'
    # A Move whose title reduces to nothing would give `m/07-.html`, and one
    # that reduces to a bare number gives an address that reads as a stub.
    empty = [n for s, ns in collisions.items() if not s or s.isdigit() for n in ns]
    assert not empty, f'a Move slug is empty or a bare number: {empty}'

    (SITE / 'm').mkdir(parents=True)
    ASSETS.mkdir(parents=True)

    (ASSETS / 'style.css').write_text(
        fonts_css() + (HERE / 'web' / 'style.css').read_text()
        + parts_css() + rise_css(),
        encoding='utf-8')
    shutil.copy(HERE / 'web' / 'app.js', ASSETS / 'app.js')
    write_logo()
    (ASSETS / 'moves-index.js').write_text(moves_index_js(moves), encoding='utf-8')

    by = {m['num']: m for m in moves}
    T = totals(moves)
    build_index(moves, T)
    build_cost(moves, T)
    build_checklist(moves, T)
    build_start(moves, T)
    build_about(moves, T)
    for i, m in enumerate(moves):
        build_move(m, moves[i - 1] if i else None,
                   moves[i + 1] if i + 1 < len(moves) else None, by, moves, T)

    for src, name in ((PDF_SRC, PDF_NAME), (EPUB_SRC, EPUB_NAME)):
        if src.exists():
            shutil.copy(src, SITE / name)

    bad = check_links()
    if bad:
        sys.exit(f'site: {len(bad)} dead links\n  ' + '\n  '.join(bad[:20]))

    n = sum(1 for f in SITE.rglob('*') if f.is_file())
    size = sum(f.stat().st_size for f in SITE.rglob('*') if f.is_file()) / 1e6
    print(f'site: {len(moves)} moves -> {n} files, {size:.2f} MB in {SITE.name}/')


if __name__ == '__main__':
    main()
