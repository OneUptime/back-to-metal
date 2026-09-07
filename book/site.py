"""Generate the website from the same Move files that make the book.

One page per question, and the front page answers the one the reader arrived
with: which Move do I do next. It shows that Move, the five figures that decide
whether it can start today, and two other ways in - the sentence that says which
stage you are at, and the symptom index for somebody whose bill or pager sent
them here rather than a plan.

The rest is one page each for a different question. checklist.html is all 122
Moves in order with a tick box each, and is the page you work down.
roadmap.html answers "how long". plan.html answers "what if we only do some of
it". The three reference pages answer themselves.

Output lands in site/ as plain files - no server, no build step, no external
request. The fonts are embedded in the stylesheet, so the directory drops onto
any static host unchanged.
"""
import base64, html, json, re, shutil, sys
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from parse import load_all, LAYERS, ORDER, CUTOVER_CAP, CLOUDS, inline
from icons import icon, meter, risk_bars
from deps import DEPS, needs as dep_needs, unlocks as dep_unlocks
from kit import SHELVES, KIT, RULES, REFERENCE, HOMELAB, HOMELAB_KIT
from rollback_data import INTRO as RB_INTRO, POINTS as RB_POINTS, DISCLAIMER as RB_DISC
from equivalents import ROWS as EQ_ROWS, CLOUDS as EQ_CLOUDS
from symptoms import SYMPTOMS
from version import VERSION
import roadmap as RM
import costs as COSTS
import imprint as IMP
import mission as MISSION
import build as B

SITE = ROOT / 'site'
ASSETS = SITE / 'assets'
NM = ROOT / 'node_modules'

PDF_NAME = IMP.PDF_NAME
EPUB_NAME = IMP.EPUB_NAME
PDF_SRC = ROOT / 'dist' / PDF_NAME
EPUB_SRC = ROOT / 'dist' / EPUB_NAME
GH_URL = f'https://{IMP.REPO}'

# How many people the roadmap is drawn for. The reader picks; the charts are all
# rendered here so the scheduling runs once, on the server.
CREWS = (1, 2, 3, 6)
DEFAULT_CREW = 3

esc = lambda s: html.escape(str(s), quote=False)
b64 = lambda p: base64.b64encode(Path(p).read_bytes()).decode()


def slug(m):
    return re.sub(r'[^a-z0-9]+', '-', m['title'].lower()).strip('-')


def pdf_pages():
    if not PDF_SRC.exists():
        return None
    counts = [int(m) for m in re.findall(rb'/Count\s+(\d+)', PDF_SRC.read_bytes())]
    return max(counts) if counts else None


def fonts_css():
    """Archivo and JetBrains Mono, embedded. Two families: one carries every word,
    the other every number. The 'standard' cut of Archivo is the one with the
    width axis the display voice is built on."""
    AR = NM / '@fontsource-variable/archivo/files'
    JB = NM / '@fontsource-variable/jetbrains-mono/files'
    css = ''
    for style, f in (('normal', 'archivo-latin-standard-normal.woff2'),
                     ('italic', 'archivo-latin-standard-italic.woff2')):
        css += (f"@font-face{{font-family:'Archivo';src:url(data:font/woff2;base64,"
                f"{b64(AR / f)}) format('woff2-variations');font-weight:100 900;"
                f"font-stretch:62% 125%;font-style:{style};font-display:swap}}\n")
    css += (f"@font-face{{font-family:'JetBrains Mono';src:url(data:font/woff2;base64,"
            f"{b64(JB / 'jetbrains-mono-latin-wght-normal.woff2')}) "
            f"format('woff2-variations');font-weight:100 800;font-style:normal;"
            f"font-display:swap}}\n")
    return css


def shell(title, body, depth=0, desc='', scripts=()):
    up = '../' * depth
    v = f'?v={VERSION}'
    more = ''.join(f'\n<script src="{up}assets/{s}{v}" defer></script>' for s in scripts)
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0A0C0D">
<link rel="stylesheet" href="{up}assets/style.css{v}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%230B0E10'/%3E%3Crect x='2' y='3' width='12' height='2.6' fill='%23fff'/%3E%3Crect x='2' y='6.7' width='8' height='2.6' fill='%23fff'/%3E%3Crect x='2' y='10.4' width='4.5' height='2.6' fill='%23fff'/%3E%3C/svg%3E">
<script>document.documentElement.className='js'</script>
</head>
<body>
{body}
<script src="{up}assets/app.js{v}" defer></script>{more}
</body>
</html>"""


# Five links, each named for the question it answers. The reference pages and the
# downloads moved to the footer: a sticky bar with ten things in it is a menu you
# have to read, and the reader arriving here has one question, not ten.
NAV = [('index.html', 'What next'), ('checklist.html', 'Checklist'),
       ('roadmap.html', 'How long'), ('plan.html', 'Plan yours'),
       ('rollback.html', 'Rollback')]

REF = [('kit.html', 'Kit'), ('replaces.html', 'What replaces what'),
       ('about.html', 'About')]


def nav(depth=0, active=''):
    up = '../' * depth
    parts = []
    for h, t in NAV:
        on = ' class="on"' if active and h.startswith(active) else ''
        parts.append(f'<a href="{up}{h}"{on}>{t}</a>')
    return f'<nav class="nav">{"".join(parts)}</nav>'


def masthead(moves, depth=0, sub=None):
    """The wordmark, one sentence, and the five facts that place the book.

    It used to carry eight, including 975 person-days and 242 weeks. Those are
    real numbers and they are the first thing somebody reads on arrival, which
    is the wrong place for them: they answer "how big is this" to a reader who
    asked "what do I do". They live on the roadmap page, which is the page that
    question belongs to, and the schedule is no longer computed on every one of
    a hundred and thirty pages to print them.
    """
    up = '../' * depth
    bits = [f'<span>v{VERSION}</span>',
            f'<span><b>{len(moves)}</b> Moves</span>',
            f'<span><b>{len(ORDER)}</b> Stages</span>',
            f'<span>AWS &middot; Google Cloud &middot; Azure</span>',
            f'<span><a href="https://{IMP.ONEUPTIME_SITE}" style="color:inherit">'
            f'{esc(IMP.BYLINE)}</a></span>']
    lede = sub or ('A step-by-step roadmap off AWS, Google Cloud or Azure and onto '
                   'Kubernetes you run on hardware you control.')
    return (f'<header class="mast"><div class="mast-in">'
            f'<a class="wordmark d" href="{up}index.html">{IMP.wordmark_html()}</a>'
            f'<div class="mast-sub"><p>{lede}</p></div></div>'
            f'<div class="edition">{"".join(bits)}</div></header>')


def rail(moves, sched, depth=0, here=None, progress=False):
    """The printed book's fore-edge tab, stood on its side.

    It only appears on the two pages where the reader is inside the sequence -
    the checklist and a Move - because a rail on a page you are reading rather
    than working through is a second navigation nobody asked for. On the
    checklist it also carries how far each stage has got, which app.js keeps up
    to date; the server-rendered value is the correct one for a reader who has
    ticked nothing, so it is right before any script runs.
    """
    up = '../' * depth
    out = []
    for s in RM.stages(moves, sched):
        info = LAYERS[s['layer']]
        on = ' class="on"' if here == s['layer'] else ''
        foot = (f'<div class="r-w" data-stage="{info["stage"]}">'
                f'0 of {s["count"]} done</div>' if progress else
                f'<div class="r-w">{s["first"]}&ndash;{s["last"]} &middot; '
                f'{esc(s["layer"])}</div>')
        out.append(
            f'<a{on} href="{up}checklist.html#{info["key"]}" '
            f'style="--c:{s["color"]}">'
            f'<div class="r-n">Stage {info["stage"]}</div>'
            f'<div class="r-t">{esc(info["doing"])}</div>'
            f'{foot}</a>')
    return f'<aside class="rail">{"".join(out)}</aside>'


def footer(depth=0):
    up = '../' * depth
    links = [f'<a href="{up}{h}">{lab}</a>' for h, lab in REF]
    if PDF_SRC.exists():
        links.append(f'<a href="{up}{PDF_NAME}" download>PDF</a>')
    if EPUB_SRC.exists():
        links.append(f'<a href="{up}{EPUB_NAME}" download>EPUB</a>')
    links.append(f'<a href="{GH_URL}">Source</a>')
    shop = ''
    if IMP.on_amazon():
        ps = [f'<a href="{IMP.amazon_url(k)}">{lab}</a>' for k, lab in
              [('paperback', 'paperback'), ('hardback', 'hardcover'), ('kindle', 'Kindle')]
              if IMP.amazon_url(k)]
        shop = f'<p>Also on Amazon in {", ".join(ps)}.</p>'
    return (f'<footer class="foot">'
            f'<nav class="foot-links">{"".join(links)}</nav>'
            f'<p class="ft">{esc(IMP.TITLE)}</p>'
            f'<p>Every Move states its cutover in minutes of user-visible downtime, its risk '
            f'as blast radius, and how long the thing it replaces must stay warm before you '
            f'turn it off. The schedule is computed from the Moves’ own effort figures and '
            f'the dependency graph, not asserted. Prices are public list rates observed while '
            f'writing and will drift. '
            f'<a href="{up}rollback.html">Read the rollback page</a> before running anything.</p>'
            f'{shop}'
            f'<p>{esc(IMP.BYLINE)} &mdash; '
            f'<a href="https://{IMP.ONEUPTIME_SITE}">{IMP.ONEUPTIME_SITE}</a>, '
            f'an open-source platform for uptime, incidents, on-call and status pages. '
            f'It is recommended in Part VII, and the interest is declared on the '
            f'<a href="{up}about.html">about page</a>.</p>'
            f'<p>Open source. The Moves and the typesetter that builds this are '
            f'<a href="{GH_URL}">on GitHub</a> — software MIT, text CC BY 4.0. '
            f'<span class="ver">v{VERSION}</span></p></footer>')


def risk_cell(m):
    return f'<span class="r-{m["risk"].lower()}">{m["risk"]}</span>'


# ---------------------------------------------------------------- shared data
# One record per Move, built once. The planner fetches it as assets/moves.json
# and the front page inlines the same bytes, so the two cannot drift and the
# front page makes no request - it works from a file:// URL and off a USB stick
# in a datacentre with no signal.
def payload(moves):
    return [{
        'n': m['num'], 'slug': slug(m), 't': m['title'], 'l': m['layer'],
        'c': m['l']['color'], 'lv': m['leaving'], 'r': m['risk'], 'cut': m['cutover'],
        'rev': m['reversible'], 'was': m['was'], 'now': m['now'],
        'eff': RM.effort_days(m), 'deps': DEPS.get(m['num'], []), 'hook': m['hook'],
        'stage': m['l']['stage'], 'doing': m['l']['doing'],
        'effs': m['figures'][4], 'wait': m['figures'][5], 'oneway': m['oneway'],
    } for m in moves]


# The self-placement sentences: one per stage, phrased the way somebody would
# describe their own estate out loud. The point is that a reader who has never
# opened the book can place themselves in it in about ten seconds.
WHERE = [
    ('Iron',     'We have not bought anything yet'),
    ('Site',     'We know what to buy, not where to put it'),
    ('Cluster',  'The machines are racked and powered'),
    ('Platform', 'The cluster runs, nothing is on it'),
    ('Data',     'Apps have moved, the data is still rented'),
    ('Edge',     'Everything runs here except the traffic'),
    ('Watch',    'It all moved and we are still paying'),
]


def facts(m):
    """The five figures that decide whether you can start this Move today.

    They are printed for the one Move being recommended and nowhere else. On a
    list of a hundred and twenty-two rows the same five figures are texture -
    a hundred and ten of them read `0 min` - and texture is what made the page
    hard to read. Here there is one Move, so every figure is about it.
    """
    bits = [('cutover', f'{m["cutover"]} min'),
            ('risk', m['risk']),
            ('effort', m['figures'][4]),
            ('back out', 'Cannot be undone' if m['oneway'] else m['reversible'])]
    if m['figures'][5] not in ('\u2014', ''):
        bits.append(('then wait', m['figures'][5]))
    return ''.join(f'<span><i>{k}</i>{esc(v)}</span>' for k, v in bits)


def answer(m, then, depth=0):
    """The answer to the only question the front page asks."""
    up = '../' * depth
    nxt = (f'<p class="ans-then"{"" if then else " hidden"}>'
           f'{("Then " + ", ".join(x["num"] for x in then) + ".") if then else ""}</p>')
    return (
        f'<section class="answer" id="answer" tabindex="-1" data-n="{m["num"]}" '
        f'style="--c:{m["l"]["color"]}">'
        f'<p class="ans-k">Stage {m["l"]["stage"]} &middot; {esc(m["l"]["doing"])}</p>'
        f'<p class="ans-note" id="ans-note" hidden></p>'
        f'<div class="ans-hd"><span class="ans-n" id="ans-n">{m["num"]}</span>'
        f'<h2 class="ans-t"><a id="ans-t" href="{up}m/{slug(m)}.html">'
        f'{esc(m["title"])}</a></h2></div>'
        f'<p class="ans-hook" id="ans-hook">{inline(m["hook"])}</p>'
        f'<p class="ans-facts" id="ans-facts">{facts(m)}</p>'
        f'{nxt}'
        f'<p class="ans-act">'
        f'<a class="btn btn-p" id="ans-open" href="{up}m/{slug(m)}.html">'
        f'Open Move {m["num"]}</a>'
        f'<button class="btn" id="ans-tick" hidden>Mark {m["num"]} done</button>'
        f'<button class="btn" id="ans-undo" hidden>Undo</button>'
        f'<a class="ans-all" href="{up}checklist.html">The whole checklist</a></p>'
        f'<p class="ans-nojs">This page remembers what you have ticked when '
        f'JavaScript is on.</p>'
        f'</section>')


def progress(moves):
    return (f'<div class="prog"><span class="track"><i id="now-fill"></i></span>'
            f'<span class="pct" id="now-pct">0 of {len(moves)} done</span></div>'
            f'<p class="prog-note">Ticks are kept in this browser and go no further.</p>')


def symptom_index(by):
    return ''.join(
        f'<div class="sym"><div class="sq">{q}</div><div class="sl">' +
        ''.join(f'<a href="m/{slug(by[n])}.html"><b>{n}</b>{esc(by[n]["title"])}</a>'
                for n in ns.split() if n in by) + '</div></div>'
        for q, ns in SYMPTOMS)


# ------------------------------------------------------------ the front page
def build_index(moves):
    """One question, one answer.

    This page used to be the whole checklist: seven stages, a hundred and
    twenty-two rows and six figures on every row, all of it on screen at once
    before the reader had decided anything. That is a warehouse, and a reader
    halfway through a migration standing in a warehouse asks the same question
    they arrived with. So the warehouse is checklist.html and this page answers
    the question: here is the Move to do next, why, what it costs, and how to
    say that is not where you are.

    The answer is rendered by the build, not by script. Move 01 with nothing
    ticked is not a fallback - it is the correct answer for every reader on a
    first visit. JavaScript only substitutes a later Move once there is a tick
    to substitute it from.
    """
    by = {m['num']: m for m in moves}
    sched = RM.schedule(moves, DEFAULT_CREW)
    stages = RM.stages(moves, sched)
    first, then = moves[0], moves[1:3]

    # Looked up by key rather than zipped by position: a Part that WHERE has not
    # been taught should fail the build, not render half a route drawn from the
    # Part next to it.
    by_stage = {s['layer']: s for s in stages}
    routes = ''.join(
        f'<a class="route" href="checklist.html#{LAYERS[k]["key"]}" '
        f'data-floor="{by_stage[k]["first"]}" style="--c:{LAYERS[k]["color"]}">'
        f'<span class="rt-s">{esc(where)}</span>'
        f'<span class="rt-m">Stage {LAYERS[k]["stage"]} &middot; '
        f'{esc(LAYERS[k]["doing"])} &middot; '
        f'Moves {by_stage[k]["first"]}&ndash;{by_stage[k]["last"]}'
        f'</span></a>'
        for k, where in WHERE)

    tail = ''.join(
        f'<a href="{h}"><span class="tl-t">{t}</span>'
        f'<span class="tl-s">{s}</span></a>' for h, t, s in [
            ('checklist.html', 'The whole checklist',
             f'All {len(moves)} Moves, in order, with a tick box each'),
            ('roadmap.html', 'How long it takes',
             'The schedule and the critical path, computed from the Moves'),
            ('plan.html', 'Plan a subset',
             'Pick only what you run and get an ordered plan')])

    data = json.dumps(payload(moves), separators=(',', ':'))
    body = f"""{masthead(moves)}
{nav(0, 'index')}
<div class="shell solo">
<main class="main">
  <div class="q-head">
    <h1 class="d">What to do next</h1>
    <span class="lbl" id="q-where">Stage {first['l']['stage']} of {len(ORDER)}</span>
  </div>
  {answer(first, then)}
  {progress(moves)}
  <script type="application/json" id="moves-data">{data}</script>
  <script src="assets/next.js?v={VERSION}"></script>

  <div class="sec-h"><h2 class="d">If that is not where you are</h2>
    <span class="lbl">Pick the line that sounds like your estate</span></div>
  <div class="routes">{routes}</div>

  <div class="sec-h" id="symptoms"><h2 class="d">Where do I start</h2>
    <span class="lbl">The real index</span></div>
  <p class="sec-b">When something on the bill or the pager has become intolerable and
  you do not want to read seven stages first, find it here and go straight to the Move.</p>
  <div class="syms">{symptom_index(by)}</div>

  <div class="tail">{tail}</div>
</main>
</div>
{footer(0)}"""
    (SITE / 'index.html').write_text(shell(
        f'{IMP.TITLE} - what to do next', body, 0,
        f'The next Move to make in a migration off AWS, Google Cloud or Azure onto '
        f'Kubernetes you run yourself, out of {len(moves)} in seven stages.'),
        encoding='utf-8')


# ------------------------------------------------------------- the checklist
def build_checklist(moves):
    """Every Move, in order, with a tick box each.

    The page the front page used to be, given a page of its own and thinned out.
    A row is a tick box, a number, a title and - on the rows where it changes
    what you do - one flag. The six figures that used to sit on every row are
    still here and still rendered by the build; they are hidden until the reader
    asks for them, because a column that reads `0 min` on a hundred and ten rows
    out of a hundred and twenty-two is not information.
    """
    sched = RM.schedule(moves, DEFAULT_CREW)
    stages = RM.stages(moves, sched)
    first = moves[0]

    blocks = ''
    for st in stages:
        k = st['layer']
        info = LAYERS[k]
        rows = ''
        rows_in = [x for x in moves if x['layer'] == k]
        for m in rows_in:
            need = DEPS.get(m['num'], [])
            n = m['num']
            # One flag, and only where the fact changes what the reader does.
            # A Move that cannot be undone says so; a Move that takes the site
            # off the air says how long. Almost every row says neither, which is
            # the correct rendering of nothing happening.
            if m['oneway']:
                flag = '<span class="ck-f ck-warn">no way back</span>'
            elif m['cutover']:
                flag = f'<span class="ck-f">{m["cutover"]} min down</span>'
            else:
                flag = ''
            rest = ''.join([
                (f'<span class="ck-need" data-need="{",".join(need)}">'
                 f'after {", ".join(need)}</span>') if need else '',
                f'<span>{m["cutover"]} min</span>',
                f'<span class="r-{m["risk"].lower()}">{m["risk"]}</span>',
                f'<span>{esc(m["figures"][4])}</span>',
                (f'<span>+{esc(m["figures"][5])} wait</span>'
                 if m['figures'][5] not in ('\u2014', '') else ''),
            ])
            rows += (
                f'<li id="m-{n}" data-n="{n}" data-deps="{",".join(need)}">'
                f'<label class="ck-b"><input type="checkbox" data-move="{n}" '
                f'aria-labelledby="n{n} t{n}">'
                f'<span class="ck-n" id="n{n}">{n}</span></label>'
                f'<a class="ck-t" id="t{n}" href="m/{slug(m)}.html">{esc(m["title"])}</a>'
                f'{flag}<span class="ck-r">{rest}</span></li>')

        # Lead times are the figure that wrecks a plan, and the only one worth
        # promoting out of the hidden strip: nobody is working during a wait, so
        # a Move ordered late holds up everything behind it.
        early = [m for m in rows_in if RM.wait_days(m) >= 20]
        lead = (f'<p class="stg-lead"><b>Order early</b>' +
                ' &middot; '.join(f'{m["num"]} waits {esc(m["figures"][5])}'
                                  for m in early) + '</p>') if early else ''
        blocks += (
            f'<details class="stg" id="{info["key"]}" open '
            f'data-stage="{info["stage"]}" style="--c:{info["color"]}">'
            f'<summary class="stg-h"><span class="stg-mk"></span>'
            f'<span class="stg-n">Stage {info["stage"]}</span>'
            f'<h2 class="d">{esc(info["doing"])}</h2>'
            f'<span class="stg-part">{info["roman"]} &middot; {esc(k)} &middot; '
            f'Moves {st["first"]}&ndash;{st["last"]}</span>'
            f'<span class="stg-prog"><span class="track"><i></i></span>'
            f'<span class="cnt">0/{st["count"]}</span></span>'
            f'</summary>'
            f'<p class="stg-done"><b>Done when</b>{esc(info["done"])}</p>'
            f'{lead}'
            f'<ol class="ck">{rows}</ol></details>')

    body = f"""{masthead(moves, 0, 'Every Move in order, with a tick box each. The page '
                'remembers where you got to, in this browser.')}
{nav(0, 'checklist')}
<div class="shell">
{rail(moves, sched, 0, None, True)}
<main class="main">
  <div class="q-head"><h1 class="d">The checklist</h1>
    <span class="lbl">Work down it in order</span></div>
  <p class="ck-lede" id="now-next">Nothing is ticked yet. The first Move is
    <a href="m/{slug(first)}.html"><b>{first['num']}</b>
    {esc(first['title'])}</a>, and it needs nothing before it.</p>
  {progress(moves)}
  <script src="assets/next.js?v={VERSION}"></script>
  <input type="checkbox" id="nums">
  <p class="nums-l"><label for="nums">Show the figures on every row</label>
    <span>Downtime, risk, effort, wait and what has to be done first</span></p>
  {blocks}
  <div class="ck-tools">
    <button class="btn" id="ck-reset">Clear every tick</button>
    <button class="btn" id="ck-restart" hidden>Start from the beginning</button>
    <a class="btn" href="index.html">Back to what to do next</a>
  </div>
</main>
</div>
{footer(0)}"""
    (SITE / 'checklist.html').write_text(shell(
        f'The checklist - {IMP.TITLE}', body, 0,
        f'All {len(moves)} Moves for a migration off AWS, Google Cloud or Azure onto '
        f'Kubernetes you run yourself, in order, with a tick box each.'), encoding='utf-8')


# ------------------------------------------------------------- the roadmap page
def build_roadmap(moves):
    sched = RM.schedule(moves, DEFAULT_CREW)
    cp = RM.critical_path(moves)
    zero = sum(1 for m in moves if m['cutover'] == 0)
    oneway = sum(1 for m in moves if m['oneway'])

    picks = ''.join(
        f'<input type="radio" name="crew" id="w{w}"'
        f'{" checked" if w == DEFAULT_CREW else ""}>' for w in CREWS)
    labels = ''.join(
        f'<label for="w{w}">{w} engineer{"" if w == 1 else "s"}</label>' for w in CREWS)
    views = ''
    for w in CREWS:
        sc = RM.schedule(moves, w)
        views += (
            f'<figure class="v{w}"><div class="rm-wrap">'
            f'{RM.svg(moves, w, href=lambda m: "m/" + slug(m) + ".html")}</div>'
            f'<figcaption class="rm-cap">'
            f'<span><i class="out"></i>Critical path outlined</span>'
            f'<span>{sc["weeks"]:.0f} working weeks with {w} '
            f'engineer{"" if w == 1 else "s"}</span>'
            f'<span>{sc["utilisation"]:.0%} utilisation</span></figcaption></figure>')

    figs = ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for v, k in [
        (len(moves), 'Moves'), (f'{sched["person_days"]:.0f}', 'Person-days'),
        (f'{cp["days"] / RM.WEEK:.0f}', 'Weeks, critical path'),
        (zero, 'At zero downtime'),
        (sum(m['cutover'] for m in moves), 'Minutes of outage'),
        (oneway, 'Cannot be undone')])

    body = f"""{masthead(moves, 0, 'How long the whole thing takes, and which Moves are on '
                'the critical path. The checklist is where you actually work.')}
{nav(0, 'roadmap')}
<div class="shell solo">
<main class="main">
  <div class="rm-head">
    <h2 class="d">How long it takes</h2>
    <span class="lbl">Computed from the Moves, not asserted</span>
  </div>
  <p class="rm-lede">Every Move states its own effort, and every dependency points at an
  earlier Move, so this is calculated rather than drawn by hand: the critical path is
  {cp['days'] / RM.WEEK:.0f} weeks, and with {DEFAULT_CREW} engineers the whole book is about
  {sched['weeks']:.0f}. None of it is a promise &mdash; effort figures are estimates, and the
  constraint is usually the overlap window rather than the calendar.</p>
  {picks}
  <div class="rm-pick">{labels}</div>
  <div class="rm-views">{views}</div>
  <div class="figs">{figs}</div>
  <p class="rm-note">The symptom index &mdash; which Move answers which problem &mdash; is
  on the <a href="index.html#symptoms">front page</a>, where somebody arriving with a
  problem rather than a programme will find it.</p>
</main>
</div>
{footer(0)}"""
    (SITE / 'roadmap.html').write_text(shell(
        f'How long it takes - {IMP.TITLE}', body, 0,
        'A computed schedule for the whole migration, and the critical path through it.'),
        encoding='utf-8')


# ---------------------------------------------------------------- a Move
def build_move(m, prev, nxt, by, sched):
    c = m['l']
    pres = ''
    for g in m['pre_groups']:
        if g['name']:
            pres += f'<p class="pre-h">{inline(g["name"])}</p>'
        pres += ('<ul class="prelist">' + ''.join(
            f'<li><label><input type="checkbox"><span>{inline(x)}</span></label></li>'
            for x in g['items']) + '</ul>')

    origins = ''.join(
        f'<div class="orow"><span class="oc">{esc(o["cloud"])}</span>'
        f'<span class="os">{inline(o["service"])}</span>'
        f'<span class="on">{inline(o["note"])}</span></div>' for o in m['origins'])

    steps = ''.join(
        f'<li class="step"><button class="sdone" aria-label="Mark step {i + 1} done">'
        f'{i + 1:02d}</button><div class="stext">{inline(s)}</div></li>'
        for i, s in enumerate(m['steps']))

    notes = ''.join(f'<div class="note"><b>{inline(t)}</b><p>{inline(b)}</p></div>'
                    for t, b in m['notes'])

    labels = ['Was', 'Now', 'Saved', 'Cutover', 'Effort', 'Wait']
    figs = ''.join(f'<div><b>{esc(v)}</b><span>{k}</span></div>'
                   for v, k in zip(m['figures'], labels))

    def deplinks(items, label, note):
        if not items:
            return ''
        return (f'<p class="pre-h">{label}</p><div class="deplist">' + ''.join(
            f'<a href="{slug(p)}.html"><i style="color:{p["l"]["color"]}">{p["num"]}</i>'
            f'<span>{esc(p["title"])}</span></a>' for p in items) +
            f'</div><p class="pnote">{note}</p>')

    wk = int(sched['start'][m['num']] // RM.WEEK) + 1
    all_moves = sorted(by.values(), key=lambda x: int(x['num']))
    body = f"""{masthead(all_moves, 1)}
{nav(1, '')}
<div class="shell">
{rail(all_moves, sched, 1, m['layer'])}
<main class="main" style="--c:{c['color']}">
  <div class="mv-head">
    <div class="mv-n">{m['num']}</div>
    <h1 class="d">{esc(m['title'])}</h1>
    <div class="mv-spec">
      <div><div class="k">Part</div><div class="v">
        <span style="color:{c['color']}">{icon(c['key'], '1em', 1.7)}</span>
        {c['label'].upper()}</div></div>
      <div><div class="k">Leaving</div><div class="v">{esc(m['leaving'])}</div></div>
      <div><div class="k">Risk</div><div class="v">
        {risk_bars(m['risk'], 'currentColor', '1em')}{m['risk'].upper()}</div></div>
      <div><div class="k">Cutover</div><div class="v">{m['cutover']} MIN</div></div>
      <div><div class="k">Back out for</div><div class="v">
        {esc(m['reversible']).upper()}</div></div>
      <div><div class="k">Roadmap</div><div class="v">WEEK {wk}</div></div>
    </div>
    <p class="hook">{inline(m['hook'])}</p>
  </div>

  <p class="blab">Leaving from</p>
  {origins}

  <div class="two">
  <div>
    <p class="blab">Why this works</p>
    <p class="why">{inline(m['why'])}</p>
    <p class="blab">The runbook</p>
    <ol class="steps">{steps}</ol>
    <div class="rollback"><b>Rollback</b><p>{inline(m['rollback'])}</p></div>
    <p class="blab">Operator&rsquo;s notes</p>
    <div class="notes">{notes}</div>
    <p class="blab">The numbers</p>
    <div class="figs">{figs}</div>
    <p class="turnoff"><b>What you can turn off</b>{inline(m['turnoff'])}</p>
  </div>
  <aside>
    <p class="blab" style="margin-top:0">Before you start</p>
    {pres}
    {deplinks(dep_needs(m['num'], by), 'Needs first',
              'These must be finished before step one.')}
    {deplinks(dep_unlocks(m['num'], by), 'Unlocks',
              'These become possible once this Move is done.')}
  </aside>
  </div>

  <nav class="mvnav">
    {f'<a href="{slug(prev)}.html"><b>Previous</b>{esc(prev["num"])} &middot; {esc(prev["title"])}</a>' if prev else '<span></span>'}
    {f'<a href="{slug(nxt)}.html" style="text-align:right"><b>Next</b>{esc(nxt["num"])} &middot; {esc(nxt["title"])}</a>' if nxt else '<span></span>'}
  </nav>
</main></div>
{footer(1)}"""
    (SITE / 'm' / f'{slug(m)}.html').write_text(shell(
        f'{m["num"]} · {m["title"]} - {IMP.TITLE}', body, 1, esc(m['hook'])),
        encoding='utf-8')


# ---------------------------------------------------------------- the planner
def build_plan(moves):
    picker = ''
    for k in ORDER:
        rows = [m for m in moves if m['layer'] == k]
        if not rows:
            continue
        picker += (f'<div class="stage-h" style="--c:{LAYERS[k]["color"]};margin-top:30px">'
                   f'<span class="s-n">{LAYERS[k]["roman"].upper()}</span>'
                   f'<h3 class="d">{esc(k)}</h3>'
                   f'<span class="s-w"><button class="clear" data-all="{LAYERS[k]["key"]}">'
                   f'Select the Part</button></span></div>')
        for m in rows:
            picker += (
                f'<label class="pk" data-layer="{LAYERS[k]["key"]}">'
                f'<input type="checkbox" value="{m["num"]}">'
                f'<span class="pn">{m["num"]}</span>'
                f'<span>{esc(m["title"])}'
                f'<small>{esc(m["leaving"])} &middot; {m["cutover"]} min &middot; '
                f'{m["risk"]}</small></span></label>')

    body = f"""{masthead(moves, 0, 'Tick what you actually run. The planner pulls in '
                'everything those Moves depend on, orders it so nothing is asked for before '
                'it exists, and totals the downtime, the effort and the saving.')}
{nav(0, 'plan')}
<div class="shell solo">
<main class="main"><div class="planwrap">
  <div class="picker">{picker}</div>
  <aside><div class="planout">
    <div class="stage-h" style="--c:var(--ink)"><h3 class="d">Your migration</h3></div>
    <p class="pnote" id="p-empty">Nothing selected yet. Tick a Move, or select a whole Part.</p>
    <div class="psum" id="p-sum" hidden>
      <div><b id="p-count">0</b><span>Moves</span></div>
      <div><b id="p-weeks">0</b><span>Weeks at 3</span></div>
      <div><b id="p-cut">0</b><span>Min downtime</span></div>
      <div><b id="p-save">$0</b><span>Monthly, illustrative</span></div>
    </div>
    <ol class="porder" id="p-order"></ol>
    <p class="pnote" id="p-note" hidden>Greyed Moves were pulled in because something you
    picked depends on them. The order is the order to run them in.</p>
    <div class="actions">
      <button class="btn" id="p-clear">Clear</button>
      <button class="btn" id="p-print">Print</button>
    </div>
  </div></aside>
</div></main></div>
{footer(0)}"""
    (SITE / 'plan.html').write_text(shell(
        f'Plan your migration - {IMP.TITLE}', body, 0,
        'Pick the Moves you need and get an ordered plan with the downtime, the effort and '
        'the saving totalled.', scripts=('plan.js',)), encoding='utf-8')
    (ASSETS / 'moves.json').write_text(
        json.dumps(payload(moves), separators=(',', ':')), encoding='utf-8')


def page_head(title, lede):
    return f'<div class="phead"><h1 class="d">{title}</h1><p class="lede">{lede}</p></div>'


def build_kit(moves):
    shelves = ''.join(
        f'<div class="shelf"><h4>{esc(name)}</h4>' +
        ''.join(f'<label><input type="checkbox"><span>{esc(i)}</span></label>' for i in items) +
        '</div>' for name, items in SHELVES)
    R = REFERENCE
    n = R['sites'] * R['nodes_per_site']
    o = COSTS.owned_month(R['sites'], R['nodes_per_site'])
    d = COSTS.dedicated_month(n)
    vcpu = n * R['cores_per_node'] * 2
    aws = vcpu * COSTS.AWS['ec2_vcpu_hour'] * 730
    mny = lambda v: f'${v:,.0f}'
    body = f"""{masthead(moves, 0, 'The reference build every Move is written against, what it '
                'costs with the salary in it, and the cluster you should build before any of it.')}
{nav(0, '')}
<div class="shell solo">
<main class="main">
  {page_head('Kit', f'Every Move is written against one cluster, so a runbook can name a real '
             f'thing rather than a category: {R["sites"]} sites, {R["nodes_per_site"]} nodes '
             f'each, {R["cores_per_node"]} cores and {R["ram_gb_per_node"]} GB a node. Scale '
             f'the numbers; do not scale away the redundancy.')}
  <div class="shelves">{shelves}</div>

  <div class="stage-h" style="--c:{LAYERS['Iron']['color']};margin-top:44px">
    <h3 class="d">The on-ramp</h3><span class="s-w">Build this one first</span></div>
  <p class="stage-b">Almost nobody should sign a facility contract before they have run this
  stack once. {HOMELAB['nodes']} refurbished machines on a managed switch under a desk will run
  every Move in the Cluster and Platform Parts unchanged &mdash; about
  {mny(COSTS.homelab_capex())} once and {mny(COSTS.homelab_month())} a month in electricity.
  It saves nothing, and that is not what it is for. What it cannot teach you is the Site Part,
  because a homelab has one power feed, one switch, no cross-connect and no second site.</p>
  <div class="shelves"><div class="shelf">{''.join(
      f'<label><input type="checkbox"><span>{esc(k)}</span></label>' for k in HOMELAB_KIT)}</div></div>

  <div class="stage-h" style="--c:{LAYERS['Watch']['color']};margin-top:44px">
    <h3 class="d">What it costs</h3><span class="s-w">With the salary in it</span></div>
  <div class="grid2">
    <div class="gcard"><h4>On the cloud, compute alone</h4><p>{vcpu:,} vCPU on demand is
      <b>{mny(aws)}</b> a month before a gigabyte of storage, a load balancer or a byte of
      egress. 100 TB a month of egress is {mny(COSTS.egress_month(100))} on top.</p></div>
    <div class="gcard"><h4>Owned, two facilities</h4><p>{mny(o['infrastructure'])} of
      infrastructure plus {mny(o['people'])} of additional salaried time.
      <b>{mny(o['total'])}</b> a month, with redundancy the cloud figure does not
      include.</p></div>
    <div class="gcard"><h4>Rented by the month</h4><p>Dedicated hosts are
      {mny(d['infrastructure'])} and remove the racking, the spares and half a person:
      <b>{mny(d['total'])}</b> all in, with a supplier you can leave in thirty days.</p></div>
    <div class="gcard"><h4>What the difference buys</h4><p>About {mny(aws - o['total'])} a
      month against a capital outlay of {mny(n * COSTS.HARDWARE['node_capex'])}, paying for
      itself in roughly {n * COSTS.HARDWARE['node_capex'] / max(aws - o['total'], 1):.0f}
      months.</p></div>
  </div>

  <div class="stage-h" style="--c:var(--ink);margin-top:44px">
    <h3 class="d">Ten rules</h3><span class="s-w">The spine of the argument</span></div>
  <div class="rules">{''.join(
      f'<div class="rule"><div class="rn">{i + 1:02d}</div>'
      f'<p><b>{esc(t)}</b> {esc(b)}</p></div>' for i, (t, b) in enumerate(RULES))}</div>
</main></div>
{footer(0)}"""
    (SITE / 'kit.html').write_text(shell(f'Kit - {IMP.TITLE}', body, 0,
        'The reference build, the homelab on-ramp, what it costs with the salary in it, and '
        'the ten rules.'), encoding='utf-8')


def build_rollback(moves):
    cards = ''.join(f'<div class="gcard"><h4>{esc(t)}</h4><p>{esc(b)}</p></div>'
                    for t, b in RB_POINTS)
    ow = [m for m in moves if m['oneway']]
    owblock = ''
    if ow:
        rows = ''.join(
            f'<tr class="mv-row"><td class="c-n" style="--c:{m["l"]["color"]}">{m["num"]}</td>'
            f'<td class="c-t"><a href="m/{slug(m)}.html">{esc(m["title"])}</a>'
            f'<p>{esc(m["hook"])}</p></td>'
            f'<td class="c-r">{risk_cell(m)}</td></tr>' for m in ow)
        owblock = (f'<div class="stage-h" style="--c:#A32E1F;margin-top:44px">'
                   f'<h3 class="d">The Moves you cannot undo</h3>'
                   f'<span class="s-w">{len(ow)} of {len(moves)}</span></div>'
                   f'<p class="stage-b">Everything else in this book has a way back. These do '
                   f'not, and each says so in its own Rollback section as well as here.</p>'
                   f'<table class="mv"><tbody>{rows}</tbody></table>')
    body = f"""{masthead(moves, 0, esc(RB_INTRO))}
{nav(0, 'rollback')}
<div class="shell solo">
<main class="main">
  {page_head('Before you touch anything', esc(RB_INTRO))}
  <div class="grid2">{cards}</div>
  {owblock}
  <p class="pnote" style="margin-top:34px">{esc(RB_DISC)}</p>
</main></div>
{footer(0)}"""
    (SITE / 'rollback.html').write_text(shell(
        f'Before you touch anything - {IMP.TITLE}', body, 0,
        'How to roll back, what a point of no return is, and the rule that a backup nobody '
        'restored is not a backup.'), encoding='utf-8')


def build_replaces(moves):
    by = {m['num']: m for m in moves}
    rows = ''.join(
        f'<tr class="{"keep" if r[3].lower().startswith("keep paying") else ""}">'
        f'<td>{esc(r[0])}</td><td>{esc(r[1])}</td><td>{esc(r[2])}</td>'
        f'<td class="yours">{esc(r[3])}'
        + (f' <a href="m/{slug(by[r[4]])}.html">&rarr; {r[4]}</a>'
           if r[4] and r[4] in by else '')
        + '</td></tr>' for r in EQ_ROWS)
    body = f"""{masthead(moves, 0, 'Every Move names the real service on all three clouds and '
                'the one thing that differs on each, so this table is the map rather than the '
                'content.')}
{nav(0, '')}
<div class="shell solo">
<main class="main">
  {page_head('What replaces what', 'Find the row you are paying for, then read the Move. '
             'Where the last column says keep paying, that is a conclusion rather than a gap.')}
  <div class="tablewrap"><table class="eq">
    <thead><tr><th>{EQ_CLOUDS[0]}</th><th>{EQ_CLOUDS[1]}</th><th>{EQ_CLOUDS[2]}</th>
      <th>What you run instead</th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="pnote" style="margin-top:26px">Three rows are set in red. A global content network,
  scrubbing capacity at the edge and outbound mail deliverability are not technical problems
  nobody has solved. They are businesses, and you are not in them.</p>
</main></div>
{footer(0)}"""
    (SITE / 'replaces.html').write_text(shell(
        f'What replaces what - {IMP.TITLE}', body, 0,
        'Every managed service, its equivalent on all three clouds, and what you run instead.'),
        encoding='utf-8')


def build_about(moves):
    paras = ''.join(f'<p>{p}</p>' for p in MISSION.paras(
        f'<a href="{GH_URL}">{IMP.REPO}</a>', len(moves)))
    pp = pdf_pages()
    body = f"""{masthead(moves, 0, 'A handbook, not an argument. The argument has been had.')}
{nav(0, '')}
<div class="shell solo">
<main class="main">
  {page_head(esc(' '.join(MISSION.HEADING_LINES)), esc(MISSION.KICKER))}
  <div class="prose">{paras}</div>
  <div class="stage-h" style="--c:var(--ink);margin-top:44px">
    <h3 class="d">How it is made</h3><span class="s-w">Two gates, one source</span></div>
  <div class="grid2">
    <div class="gcard"><h4>One source of truth</h4><p>{len(moves)} markdown files are the whole
      book. A Python toolchain turns them into a {f"{pp}-page " if pp else ""}print interior, an
      EPUB and this site. Every number in any of them &mdash; page numbers, totals, the
      roadmap, the filters here &mdash; is derived from those files.</p></div>
    <div class="gcard"><h4>The schedule is computed</h4><p>The roadmap is not drawn by hand. It
      is list-scheduled from each Move&rsquo;s stated effort and the dependency graph, so it
      cannot drift from the Moves, and the critical path falls out of the same calculation.</p></div>
    <div class="gcard"><h4>Two gates</h4><p><code>verify.py</code> checks the shape of every
      Move: the sections, the three-cloud block, the cost arithmetic, and that no Move moving
      persistent state ships without saying how the state comes back. <code>audit.py</code>
      checks the content. Both must be clean.</p></div>
    <div class="gcard"><h4>Corrections</h4><p>The most valuable contribution is a correction. If
      you ran a runbook and it did not work as written, or a price is wrong for your region,
      that is worth an issue on its own.</p></div>
    <div class="gcard"><h4>Disclosure</h4><p>{esc(IMP.DISCLOSURE)}</p></div>
  </div>
  <div class="actions"><a class="btn btn-p" href="{GH_URL}">View the repository</a>
    <a class="btn" href="{GH_URL}/blob/main/CONTRIBUTING.md">Add a Move</a></div>
</main></div>
{footer(0)}"""
    (SITE / 'about.html').write_text(shell(f'About - {IMP.TITLE}', body, 0,
        'Why the book exists, how it is built, and how to correct it.'), encoding='utf-8')


def main():
    moves = load_all()
    if not moves:
        sys.exit('site: no Move files in moves/ yet')
    if SITE.exists():
        shutil.rmtree(SITE)
    # One page per Move, so one slug per Move. verify.py checks this too; the
    # assertion is here because this is where the damage would happen - a
    # collision silently overwrites a page and the only symptom is a Move that
    # is not on the website.
    collisions = {}
    for m in moves:
        collisions.setdefault(slug(m), []).append(m['num'])
    clash = {s: ns for s, ns in collisions.items() if len(ns) > 1}
    assert not clash, f'moves share a slug and would overwrite each other: {clash}'

    (SITE / 'm').mkdir(parents=True)
    ASSETS.mkdir(parents=True)

    (ASSETS / 'style.css').write_text(
        fonts_css() + (HERE / 'web' / 'style.css').read_text(), encoding='utf-8')
    for js in ('app.js', 'next.js', 'plan.js'):
        shutil.copy(HERE / 'web' / js, ASSETS / js)

    by = {m['num']: m for m in moves}
    sched = RM.schedule(moves, DEFAULT_CREW)
    build_index(moves)
    build_checklist(moves)
    build_roadmap(moves)
    for i, m in enumerate(moves):
        build_move(m, moves[i - 1] if i else None,
                   moves[i + 1] if i + 1 < len(moves) else None, by, sched)
    build_plan(moves)
    build_kit(moves)
    build_rollback(moves)
    build_replaces(moves)
    build_about(moves)

    for src, name in ((PDF_SRC, PDF_NAME), (EPUB_SRC, EPUB_NAME)):
        if src.exists():
            shutil.copy(src, SITE / name)

    n = sum(1 for _ in SITE.rglob('*') if _.is_file())
    mb = sum(f.stat().st_size for f in SITE.rglob('*') if f.is_file()) / 1e6
    print(f'site: {len(moves)} moves -> {n} files, {mb:.2f} MB in {SITE.name}/')


if __name__ == '__main__':
    main()
