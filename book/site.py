"""Generate the website from the same Move files that make the book.

Five pages and one page per Move. The reader is a startup engineer with a cloud
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
from kit import SHELVES, RULES, KIT, REFERENCE, HOMELAB, HOMELAB_KIT
from rollback_data import intro as rb_intro, POINTS as RB_POINTS, DISCLAIMER as RB_DISC
from equivalents import ROWS as EQ_ROWS, CLOUDS as EQ_CLOUDS
from symptoms import SYMPTOMS
from version import VERSION
import roadmap as RM
import costs as COSTS
import imprint as IMP
import mission as MISSION

SITE = ROOT / 'site'
ASSETS = SITE / 'assets'
NM = ROOT / 'node_modules'

PDF_NAME = IMP.PDF_NAME
EPUB_NAME = IMP.EPUB_NAME
PDF_SRC = ROOT / 'dist' / PDF_NAME
EPUB_SRC = ROOT / 'dist' / EPUB_NAME
GH_URL = f'https://{IMP.REPO}'

# The crew the site quotes its schedule for. Two, because that is who this
# edition is written for: a company with two or three engineers, one of whom
# still has a day job. The other two are drawn only as a comparison, so a
# reader can see what a third pair of hands actually buys - which is less than
# people expect, because the long pole is lead time and not labour.
DEFAULT_CREW = 2
CREWS = (1, 2, 3)

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


def mb(path):
    return path.stat().st_size / 1e6


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

    `parse.LAYERS` is the single source, and it carries two hexes a Stage: the
    one chosen to sit on paper and the one that lifts off a near-black screen.
    The screen is what the site is, so `dark` is what `:root` gets; `color` is
    correct only on paper and appears only inside the print block. Inlining the
    paper hex into a `style="--c:#1F4E79"` on every coloured element is what the
    site used to do, and it painted Stage signals at 2.2:1 to 3.6:1 on a dark
    ground - below the floor for a graphic, let alone a numeral."""
    def block(key):
        return '\n'.join(f'[data-part={LAYERS[k]["key"]}]{{--c:{LAYERS[k][key]}}}'
                          for k in ORDER)
    return (
        '\n/* The five Stages, written by site.py out of parse.LAYERS. The screen\n'
        '   is dark, so the screen takes the `dark` hex; paper takes the other. */\n'
        + block('dark') + '\n'
        + '@media print{\n' + block('color') + '\n}\n')


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


def shell(title, body, depth=0, desc=''):
    """The document. One stylesheet, and two scripts: the corpus of Moves, then
    the behaviour that reads it. `app.js` is deferred rather than inlined
    mid-body because nothing above the fold now depends on it - the header's
    next link is already correct in the HTML."""
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
<meta name="theme-color" content="#14181A">
<link rel="stylesheet" href="{up}assets/style.css{v}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%230B0E10'/%3E%3Crect x='2' y='3' width='12' height='2.6' fill='%23fff'/%3E%3Crect x='2' y='6.7' width='8' height='2.6' fill='%23fff'/%3E%3Crect x='2' y='10.4' width='4.5' height='2.6' fill='%23fff'/%3E%3C/svg%3E">
<script>document.documentElement.className='js'</script>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
{body}{js}
</body>
</html>"""


def bar(depth, first, active=''):
    """The header: a wordmark, five links, and the next Move.

    It is not sticky. Sticky chrome on a page somebody reads for twenty minutes
    is the thing this edition removed, and the next link is worth more at the
    top of the page you arrived on than pinned over the paragraph you are
    reading."""
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
    up = '../' * depth
    links = [f'<a href="{up}{h}">{esc(t)}</a>' for h, t in NAV]
    if PDF_SRC.exists():
        links.append(f'<a href="{up}{PDF_NAME}" download>PDF</a>')
    if EPUB_SRC.exists():
        links.append(f'<a href="{up}{EPUB_NAME}" download>EPUB</a>')
    links.append(f'<a href="{GH_URL}">Source</a>')
    return (
        f'<footer class="foot"><div class="foot-in">'
        f'<nav class="foot-nav" aria-label="Every page">{"".join(links)}</nav>'
        f'<p class="foot-note">Every Move states its cutover in minutes of user-visible '
        f'downtime, its risk as blast radius, and how long the thing it replaces must stay '
        f'warm before you turn it off. The schedule is computed from the Moves&rsquo; own '
        f'effort figures and the dependency graph rather than asserted, and every price is a '
        f'public list rate observed while writing. '
        f'<a href="{up}start.html">Read the safety page</a> before running anything.</p>'
        f'<p class="foot-note">{esc(IMP.BYLINE)} &mdash; '
        f'<a href="https://{IMP.ONEUPTIME_SITE}">{IMP.ONEUPTIME_SITE}</a>, an open-source '
        f'platform for uptime, incidents, on-call and status pages. It is recommended in '
        f'Stage 5, and the interest is declared on the '
        f'<a href="{up}about.html">about page</a>.</p>'
        f'<p class="foot-note">Open source: the Moves and the typesetter that builds this '
        f'are <a href="{GH_URL}">on GitHub</a> &mdash; software MIT, text CC BY 4.0. '
        f'<span class="ver">v{VERSION}</span></p>'
        f'</div></footer>')


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
    # of minus $1,250, and any future Move that stated a Was and no Now would
    # read as saving the whole of it. A null is a Move whose trade is somewhere
    # else on the bill, and the script has to be able to tell the difference.
    rows = [[m['num'], page(m)[:-5], m['title'], RM.effort_days(m),
             m['was'], m['now']] for m in moves]
    return 'window.BTM_MOVES=' + json.dumps(rows, separators=(',', ':')) + ';\n'


# ---------------------------------------------------------------- the numbers
def totals(moves):
    """Every figure any page quotes, computed once.

    Nothing here is written into prose anywhere. The pages interpolate this
    dict, so a Move added, removed or re-costed moves every sentence that
    mentions a total, in the same way mission.py takes the count as an
    argument rather than spelling it out."""
    R = REFERENCE
    owned = COSTS.owned_month(R['nodes'], R['spares'])
    dedicated = COSTS.dedicated_month(R['nodes'] + R['spares'])
    save = COSTS.BILL_MONTH - owned['total']
    sched = RM.schedule(moves, DEFAULT_CREW)
    # Only the Moves that state both halves of the trade can contribute to a
    # saving. A Move with an em dash in either cell is not a zero, it is a Move
    # whose saving is somewhere else on the bill.
    priced = [m for m in moves if m['was'] is not None and m['now'] is not None]
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
        'save': save,
        'pct': save / COSTS.BILL_MONTH * 100 if COSTS.BILL_MONTH else 0,
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


def hero(title, lede, sub='', display='page', extra=''):
    return (f'<section class="hero"><h1 class="d {display}">{title}</h1>'
            f'<p class="lede">{lede}</p>'
            + (f'<p class="sub">{sub}</p>' if sub else '') + extra + '</section>')


def band(bid, heading, inner):
    return (f'<section class="band" id="{bid}">'
            f'<h2 class="d sect">{esc(heading)}</h2>{inner}</section>')


# ------------------------------------------------------------- 1. the guide
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
            f'<span class="mv-f"><i>{esc(m["figures"][4])}</i><i>{esc(m["risk"])}</i>'
            f'<i>{downtime(m)}</i></span></a></li>' for m in rows)
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
    crews = ', '.join(
        f'{w} engineer{"" if w == 1 else "s"} about {T["crew_weeks"][w]:.0f} weeks'
        for w in CREWS if w in T['crew_weeks'])

    body = f"""{bar(0, first, 'index.html')}
<main id="main" class="shell">
{hero(IMP.wordmark_html(sep=' '),
      f'{T["n"]} Moves that take a startup off AWS, Google Cloud or Azure and onto '
      f'hardware you own.',
      f'Written for a company with two or three engineers and a cloud bill around '
      f'{mny(T["bill"])} a month. About {T["days"]:.0f} days of work spread across '
      f'{T["weeks"]:.0f} weeks, and most of that is waiting for hardware rather than '
      f'working.',
      'mast',
      figs([(T['n'], 'Moves'), (f'{T["days"]:.0f}', 'Days of work'),
            (f'{T["weeks"]:.0f}', 'Weeks end to end'),
            (f'{T["pct"]:.0f}%', 'Off the bill')])
      + f'<p class="cta"><a class="btn" href="m/{page(first)}">Start at Move '
        f'{first["num"]}</a> <a class="btn ghost" href="cost.html">Or check the '
        f'arithmetic first</a></p>')}

{band('plan', 'The whole plan, on one page',
      f'<p>{len(T["stages"])} stages, run in order, and every dependency points at a '
      f'lower number. '
      f'{T["zero"]} of the {T["n"]} Moves are invisible to a user; the whole programme '
      f'costs {T["cutover"]} minutes of downtime between them{oneway_line}.</p>'
      f'<ol class="stages">{"".join(blocks)}</ol>')}

{band('where', 'Start where it hurts',
      f'<p>Nobody sits down at nine in the morning thinking in stages. Find the line '
      f'that sounds like your week and go straight to the Move.</p>'
      f'<ul class="symp">{symps}</ul>')}

{band('how-long',
      'How long it takes',
      f'<p>The labour is about {T["days"]:.0f} person-days. With {DEFAULT_CREW} '
      f'engineers it lands in roughly {T["weeks"]:.0f} weeks, and the shortest it '
      f'could possibly take, with as many people as you care to put on it, is '
      f'{T["critical_weeks"]:.0f}. The gap between those two numbers is not labour. '
      f'It is the circuit order, the hardware lead time and the thirty-day windows a '
      f'Move has to sit through before the next one may start, and nobody is working '
      f'during any of it.</p>'
      + RM.svg(moves, DEFAULT_CREW, href=lambda m: 'm/' + page(m))
      + f'<p class="note">One bar per Move, drawn from each Move&rsquo;s own effort '
        f'figure and the dependency graph rather than from a plan somebody typed. The '
        f'outlined bars are the critical path. Adding people barely moves the end date: '
        f'{crews}.</p>')}
</main>
{foot(0)}"""
    (SITE / 'index.html').write_text(shell(
        f'{IMP.TITLE} \u2014 the whole plan', body, 0,
        f'{T["n"]} Moves in five stages that take a startup off AWS, Google Cloud or '
        f'Azure and onto hardware it owns.'), encoding='utf-8')


# ------------------------------------------------------------ 2. what it costs
def cost_bars(rows):
    """Three totals, one scale, drawn rather than charted.

    The point is a comparison a reader can check in their head, so there are no
    gridlines, no axis and no legend inside the drawing. Each bar is two
    segments - the metal, then the salaried time - because the salary is the
    whole argument and hiding it inside a total is what makes a repatriation
    look better on a slide than it turns out to be.

    Colours come from CSS rather than from here: the site has a dark theme and a
    hex written into an SVG cannot follow it."""
    if not rows:
        return ''
    W, PAD, ROW, BAR = 700, 120, 56, 20
    top = max(i + p for _, i, p in rows) or 1
    scale = (W - PAD) / top
    out = []
    for k, (label, infra, people) in enumerate(rows):
        y = k * ROW
        wi, wp = infra * scale, people * scale
        out.append(f'<text class="cost-l" x="0" y="{y + 11}">{esc(label)}</text>')
        out.append(f'<rect class="cost-i" x="0" y="{y + 20}" width="{wi:.1f}" '
                   f'height="{BAR}"/>')
        if wp > 0:
            out.append(f'<rect class="cost-p" x="{wi:.1f}" y="{y + 20}" '
                       f'width="{wp:.1f}" height="{BAR}"/>')
        out.append(f'<text class="cost-v" x="{wi + wp + 8:.1f}" y="{y + 35}">'
                   f'{mny(infra + people)}</text>')
    return (f'<svg class="cost" viewBox="0 0 {W} {len(rows) * ROW}" width="100%" '
            f'style="height:auto;display:block" role="img" aria-label="Monthly cost '
            f'compared: ' + '; '.join(f'{l}, {mny(i + p)}' for l, i, p in rows)
            + f'">{"".join(out)}</svg>')


def build_cost(moves, T):
    by = {m['num']: m for m in moves}
    first = moves[0]
    owned, ded, bill = T['owned'], T['dedicated'], T['bill']

    heads = ['Cloud now', 'Own the machines', 'Rent the machines by the month']
    cmp_rows = [
        ('Infrastructure', '', [mny(bill), mny(owned['infrastructure']),
                                mny(ded['infrastructure'])]),
        ('People', 'people', ['Already in the bill', mny(owned['people']),
                              mny(ded['people'])]),
        ('Total a month', 'tot', [mny(bill), mny(owned['total']), mny(ded['total'])]),
        ('Saved a month', 'save', ['&mdash;', mny(bill - owned['total']),
                                   mny(bill - ded['total'])]),
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
    # bill it takes off. The rows sum to less than the headline saving and
    # should - some Moves buy safety rather than money, and they say so with
    # an em dash rather than a zero.
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
      f'{mny(bill)} a month becomes {mny(owned["total"])} with the salary counted. '
      f'That is {mny(T["save"] * 12)} a year, or {T["pct"]:.0f} per cent of the bill.',
      f'The reference build is {REFERENCE["nodes"]} machines and a spare on the shelf, '
      f'in one cage. Every figure below is a public list price observed while writing, '
      f'against a bill this size. Substitute your own and the shape does not change.',
      'page',
      figs([(mny(bill), 'Cloud, a month'), (mny(owned['total']), 'Owned, a month'),
            (mny(T['save'] * 12), 'Saved a year'), (f'{T["pct"]:.0f}%', 'Off the bill')]))}

{band('compare', 'The comparison, with the salary in it',
      cmp_html
      + f'<p class="callout"><span class="lbl">The people row</span> The salaried time '
        f'is the largest number in the owned column, and a comparison without it is the '
        f'reason repatriations get approved and then regretted. The cloud already costs '
        f'{COSTS.PEOPLE["engineers_before"]} of an engineer to run; owning the machines '
        f'costs {COSTS.PEOPLE["engineers_after"]}, so the difference is what appears '
        f'here. If your answer changes when that line goes in, you want to know in week '
        f'one rather than month ten.</p>'
      + f'<p class="cost-key"><i class="k-i"></i>Infrastructure '
        f'<i class="k-p"></i>Salaried time</p>'
      + cost_bars([('Cloud now', bill, 0),
                   ('Own the machines', owned['infrastructure'], owned['people']),
                   ('Rent by the month', ded['infrastructure'], ded['people'])]))}

{band('where-money', 'Where the money goes',
      f'<p>One row per Move, in the order you run them. Some Moves buy safety rather '
      f'than money and say so with a dash. The rows that state both halves come to '
      f'{mny(tw - tn)} a month, which is more than the {mny(T["save"])} at the top of '
      f'this page: these are line savings, taken before the salaried time and the fixed '
      f'cost of the cage that the comparison above puts back in.</p>' + perm)}

{band('replaces', 'What replaces what',
      f'<p>Find the row you are paying for, then read the Move. Where the last column '
      f'says keep paying, that is a conclusion rather than a gap: a content delivery '
      f'network, scrubbing capacity at the edge and outbound mail deliverability are '
      f'businesses somebody else already runs better than you will.</p>' + eq)}

{band('onramp', 'Before you sign anything',
      f'<p>Almost nobody should sign a facility contract before they have run this '
      f'stack once. {HOMELAB["nodes"]} refurbished machines on a managed switch under a '
      f'desk cost about {mny(COSTS.homelab_capex())} once and '
      f'{mny(COSTS.homelab_month())} a month in electricity, and they run the whole of '
      f'Stage 3 unchanged. It saves nothing, and that is not what it is for: it is the '
      f'smallest bet that tells you whether the rest of this book is for you.</p>'
      f'<p class="note">Every figure on this page is a dated list-price observation, '
      f'not a quotation. Cloud prices are on-demand and undiscounted on purpose; a '
      f'reader with a commitment discount should substitute their own effective rate, '
      f'and a reader without one is genuinely paying this.</p>')}
</main>
{foot(0)}"""
    (SITE / 'cost.html').write_text(shell(
        f'What it costs \u2014 {IMP.TITLE}', body, 0,
        f'The arithmetic: {mny(bill)} a month on the cloud against {mny(owned["total"])} '
        f'on machines you own, with the salary counted.'), encoding='utf-8')


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
        blocks.append(
            f'<section class="stage" data-part="{info["key"]}">'
            f'<div class="stage-head"><span class="lbl">{esc(info["roman"])}</span>'
            f'<h2 class="d">{esc(info["label"])}</h2>'
            f'<p class="stage-do">{esc(info["doing"])}</p>'
            f'<p class="stage-done"><span class="lbl">Done when</span> '
            f'{esc(info["done"])}</p></div>{cks}</section>')

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
      f'<ol class="pts">{pts}</ol>'
      f'<p class="note">{esc(RB_DISC)}</p>')}

{band('rules', 'The rules',
      f'<p>{len(RULES)} of them: the spine of the argument, and what survived being '
      f'rewritten for a company with two engineers rather than twenty.</p>'
      f'<ol class="rules">{rules}</ol>')}

{band('kit', 'What to buy',
      f'<p>Every Move is written against one cluster, so a runbook can name a real '
      f'thing rather than a category: {REFERENCE["nodes"]} nodes and '
      f'{REFERENCE["spares"]} spare in one cage, {REFERENCE["cores_per_node"]} cores and '
      f'{REFERENCE["ram_gb_per_node"]} GB a node, on a '
      f'{REFERENCE["uplink_gbps"]} GbE uplink. Scale the numbers; do not scale away the '
      f'redundancy. Tick it off against a quote.</p>'
      f'<div class="shelves">{shelves}</div>'
      f'<h3 class="d sub-h">On the laptop of whoever is running a Move</h3>'
      f'<ul class="tools">'
      + ''.join(f'<li>{esc(t)}</li>' for t in KIT) + '</ul>'
      f'<h3 class="d sub-h">The on-ramp, under a desk</h3>'
      f'<p>{HOMELAB["nodes"]} refurbished machines, {HOMELAB["cores_per_node"]} cores '
      f'and {HOMELAB["ram_gb_per_node"]} GB each, prove the whole stack for about '
      f'{mny(COSTS.homelab_capex())} once and {mny(COSTS.homelab_month())} a month in '
      f'electricity. What it cannot teach you is the cage: one power feed, one switch, '
      f'no cross-connect.</p>'
      f'<ul class="onramp">'
      + ''.join(f'<li>{esc(k)}</li>' for k in HOMELAB_KIT) + '</ul>')}
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

    dls = []
    if PDF_SRC.exists():
        dls.append(
            f'<a class="dl" href="{PDF_NAME}" download><b class="dl-t">The print '
            f'interior</b><span class="dl-m">PDF'
            + (f' &middot; {pp} pages' if pp else '')
            + f' &middot; {mb(PDF_SRC):.1f} MB</span></a>')
    if EPUB_SRC.exists():
        dls.append(
            f'<a class="dl" href="{EPUB_NAME}" download><b class="dl-t">The Kindle '
            f'edition</b><span class="dl-m">EPUB &middot; reflowable &middot; '
            f'{mb(EPUB_SRC):.1f} MB</span></a>')

    colophon = ''.join(f'<div><dt class="lbl">{esc(k)}</dt><dd>{v}</dd></div>'
                       for k, v in [
                           ('Version', f'v{VERSION}'),
                           ('Moves', T['n']),
                           ('Stages', len(T['stages'])),
                           ('Interior', f'{pp} pages' if pp else 'PDF'),
                           ('Text', 'CC BY 4.0'),
                           ('Software', 'MIT')])

    body = f"""{bar(0, first, 'about.html')}
<main id="main" class="shell">
{hero(esc(' '.join(MISSION.HEADING_LINES)),
      'A handbook, not an argument. The argument has been had.',
      esc(MISSION.KICKER))}

<section class="band" id="why">
<div class="prose">{''.join(
    f'<p>{p}</p>' for p in MISSION.paras(f'<a href="{GH_URL}">{IMP.REPO}</a>', T['n']))}</div>
</section>

{band('download', 'Take it with you',
      f'<p>The same {T["n"]} Moves, typeset. The print interior is the one to read on '
      f'paper beside a rack; the Kindle edition reflows.</p>'
      f'<div class="dls">{"".join(dls)}</div>'
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
      f'<a class="btn ghost" href="{GH_URL}/blob/main/CONTRIBUTING.md">Add a Move</a></p>')}

{band('disclosure', 'Disclosure',
      f'<p class="callout">{esc(IMP.DISCLOSURE)}</p>')}

{band('licence', 'Two licences',
      f'<p>{esc(IMP.LICENCE)}</p>'
      f'<dl class="colo">{colophon}</dl>'
      f'<p class="note">{esc(IMP.TYPE_NOTE)} Written by {esc(IMP.AUTHOR)} and published '
      f'by {esc(IMP.PUBLISHER)}. {esc(IMP.DISCLAIMER)}</p>')}
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

    labels = ['Was', 'Now', 'Saved', 'Cutover', 'Effort', 'Wait']
    nums = ('<table class="nums"><thead><tr>'
            + ''.join(f'<th scope="col">{l}</th>' for l in labels)
            + '</tr></thead><tbody><tr>'
            + ''.join(f'<td>{esc(v)}</td>' for v in m['figures'])
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

    pn = ''.join(x for x in [
        (f'<a class="prev" rel="prev" href="{page(prev)}">{prev["num"]} &middot; '
         f'{esc(prev["title"])}</a>') if prev else '',
        (f'<a class="nxt" rel="next" href="{page(nxt)}">{nxt["num"]} &middot; '
         f'{esc(nxt["title"])}</a>') if nxt else ''])

    body = f"""{bar(1, moves[0])}
<main id="main" class="shell">
<article class="move" data-part="{c['key']}">
  <header class="mh">
    <p class="lbl">{esc(c['roman'])} &middot; {esc(c['label'])} &middot; Move {m['num']} of {T['n']}</p>
    <h1 class="d page">{esc(m['title'])}</h1>
    <p class="hook">{inline(m['hook'])}</p>
    <dl class="facts">{facts}</dl>
    {deplinks(dep_needs(m['num'], by), 'Needs', 'needs')}
  </header>

  <section class="sec"><h2 class="d sect">The runbook</h2>
    <ol class="steps" data-n="{m['num']}">{steps}</ol></section>

  <section class="sec"><h2 class="d sect">Before you start</h2>
    <div class="pre">{pre}</div></section>

  <section class="sec"><h2 class="d sect">What you are leaving</h2>
    <ul class="clouds">{clouds}</ul></section>

  <section class="sec"><h2 class="d sect">Why this works</h2>
    <p>{inline(m['why'])}</p></section>

  <section class="sec"><h2 class="d sect">Operator&rsquo;s notes</h2>
    <dl class="notes">{notes}</dl></section>

  <section class="sec warn"><h2 class="d sect">Rollback</h2>
    <p>{inline(m['rollback'])}</p></section>

  <section class="sec"><h2 class="d sect">The numbers</h2>
    {nums}
    <p class="turnoff"><span class="lbl">What you can turn off</span>
      {inline(m['turnoff'])}</p></section>

  <footer class="mf">
    <label class="ck big"><input type="checkbox" class="ck-box" data-n="{m['num']}">
      Mark Move {m['num']} as done</label>
    <nav class="pn" aria-label="Moves">{pn}</nav>
    {deplinks(dep_unlocks(m['num'], by), 'Unlocks', 'unlocks')}
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
    (SITE / 'm' / f'{m["num"]}.html').write_text(
        f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8">\n'
        f'<title>{esc(m["num"])} \u00b7 {esc(m["title"])}</title>\n'
        f'<link rel="canonical" href="{page(m)}">\n'
        f'<meta http-equiv="refresh" content="0;url={page(m)}">\n'
        f'</head><body><a href="{page(m)}">Move {esc(m["num"])} &mdash; '
        f'{esc(m["title"])}</a></body></html>\n', encoding='utf-8')
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
        fonts_css() + (HERE / 'web' / 'style.css').read_text() + parts_css(),
        encoding='utf-8')
    shutil.copy(HERE / 'web' / 'app.js', ASSETS / 'app.js')
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
