"""Generate the website from the same Move files that make the book.

The site is an instrument, not a document. Somebody keeps it open for six months
while they rack machines, so every one of its 131 pages carries the same 48px
chrome - where you are, where you can go, how far you have got, and a box that
takes a Move number - and the book cover appears once, on the front page, where
a cover belongs.

One page per question. index.html answers the one the reader arrived with: which
Move do I do next. checklist.html is all 122 in order with a tick box each and is
the page you work down. roadmap.html answers "how long". plan.html answers "what
if we only do some of it". s/*.html is one page per stage, so the book's own
organising unit has an address instead of being a fragment of a seven-thousand
pixel scroll. m/*.html is the Move itself, ordered so the runbook comes first and
the prerequisites come above it rather than four screens below.

Output lands in site/ as plain files - no server, no build step, no external
request. The fonts and the Part colours are written into the stylesheet, so the
directory drops onto any static host unchanged and works from a file:// URL.
"""
import base64, html, json, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from parse import load_all, LAYERS, ORDER, inline
from icons import icon, risk_bars
from deps import DEPS, needs as dep_needs, unlocks as dep_unlocks
from kit import SHELVES, RULES, REFERENCE, HOMELAB, HOMELAB_KIT
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

# How many people the roadmap is drawn for. The reader picks; the charts are all
# rendered here so the scheduling runs once, on the server.
CREWS = (1, 2, 3, 6)
DEFAULT_CREW = 3

esc = lambda s: html.escape(str(s), quote=False)
attr = lambda s: html.escape(str(s), quote=True)
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
    """The seven Part colours, as attribute rules rather than inline hexes.

    `parse.LAYERS` is the single source: it carries the colour that sits on paper
    and the colour that lifts off a near-black screen. The site used to inline the
    first one into a `style="--c:#1F4E79"` on every coloured element, which meant
    the dark theme painted Part signals at 2.2:1 to 3.6:1 - below the floor for a
    graphic, let alone a numeral. One attribute now drives both."""
    def block(prefix, key):
        return '\n'.join(f'{prefix}[data-part={LAYERS[k]["key"]}]{{--c:{LAYERS[k][key]}}}'
                         for k in ORDER)
    return (
        '\n/* The seven Parts, written by site.py out of parse.LAYERS. Two hexes\n'
        '   each: the one that sits on paper and the one that lifts off a\n'
        '   near-black screen. Which is correct depends on what is behind it. */\n'
        + block('', 'color') + '\n'
        + '@media (prefers-color-scheme:dark){\n'
        + block('', 'dark') + '\n}\n')


def shell(title, body, depth=0, desc='', scripts=(), core=True):
    """The document. `core` loads next.js at the end of the body; the two pages
    that paint an answer above the fold load it mid-body instead, so no wrong
    Move is ever on screen."""
    up = '../' * depth
    v = f'?v={VERSION}'
    js = list(scripts)
    if core:
        js.insert(0, 'next.js')
    js.insert(0, 'moves-index.js')
    js.append('app.js')
    more = ''.join(f'\n<script src="{up}assets/{s}{v}" defer></script>' for s in js)
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{attr(desc)}">
<meta name="theme-color" content="#FCFCFB" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14181A" media="(prefers-color-scheme: dark)">
<link rel="stylesheet" href="{up}assets/style.css{v}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%230B0E10'/%3E%3Crect x='2' y='3' width='12' height='2.6' fill='%23fff'/%3E%3Crect x='2' y='6.7' width='8' height='2.6' fill='%23fff'/%3E%3Crect x='2' y='10.4' width='4.5' height='2.6' fill='%23fff'/%3E%3C/svg%3E">
<script>document.documentElement.className='js'</script>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
{body}{more}
</body>
</html>"""


# Every page on the site, in the order the rail lists them. The five that used to
# be a sticky tab strip and the three that were reachable only from a footer at
# the bottom of a seven-screen scroll are one list now, and the page you are on
# is marked on all of them.
PAGES = [
    ('index.html', 'What to do next'),
    ('checklist.html', 'The checklist'),
    ('roadmap.html', 'How long it takes'),
    ('plan.html', 'Plan yours'),
    ('symptoms.html', 'Where do I start'),
    ('rollback.html', 'Before you touch anything'),
    ('kit.html', 'Kit'),
    ('replaces.html', 'What replaces what'),
    ('about.html', 'About'),
]


def moves_index_js(moves):
    """The jump box's corpus: number, slug and title, once.

    It is a script rather than a `<datalist>` in the markup because the markup
    is on every page and the script is fetched once and cached. Inlining it cost
    16 KB a page and 2 MB across the site to save one request, which is the
    wrong way round; a `<script src>` also still resolves from a file:// URL,
    which a fetch does not, so the box works off a USB stick in a datacentre.

    app.js builds the native `<datalist>` from it, so the input keeps its own
    type-ahead as well as the result list."""
    rows = [[m['num'], slug(m), m['title']] for m in moves]
    return 'window.BTM_MOVES=' + json.dumps(rows, separators=(',', ':')) + ';\n'


def spine_html(stages, here=None):
    """Seven segments, one per stage, each as wide as that stage has Moves and
    filled in that stage's own colour as they are ticked.

    The printed book's fore-edge tab, laid flat under the chrome. It is the only
    progress readout the 122 Move pages have ever had, it is a rule and some
    space, and it is correct before any script runs: nothing ticked is what is
    true for every reader on a first visit."""
    cols = ' '.join(f'{s["count"]}fr' for s in stages)
    # Each segment carries the Move numbers it spans, so the fill can be worked
    # out from the ticks alone. Without them the spine could only be painted on
    # the page types that happen to carry a list of Moves, and would read zero
    # everywhere else while the counter three pixels above it read the truth.
    cells = ''.join(
        f'<i data-part="{LAYERS[s["layer"]]["key"]}" data-stage="{LAYERS[s["layer"]]["stage"]}"'
        f' data-from="{s["first"]}" data-to="{s["last"]}" data-n="{s["count"]}"'
        f'{" class=" + chr(34) + "here" + chr(34) if here == s["layer"] else ""}>'
        f'<b></b></i>' for s in stages)
    return (f'<div class="spine" id="spine" aria-hidden="true" '
            f'style="grid-template-columns:{cols}">{cells}</div>')


def chrome(depth, moves, stages, active='', crumb=(), here=None, prevnext=None):
    """The 48px application chrome, byte-identical on every page except the
    breadcrumb and the two arrows.

    It replaced a 265px masthead reprinted on every page - 39% of a phone's
    viewport before a word of content - and a five-tab strip that lit nothing on
    all but five of the pages it appeared on."""
    up = '../' * depth
    bits = []
    for i, (href, label) in enumerate(crumb):
        if i:
            bits.append('<i>&rsaquo;</i>')
        bits.append(f'<a href="{up}{href}">{esc(label)}</a>' if href
                    else f'<b>{esc(label)}</b>')
    pn = ''
    if prevnext:
        prev, nxt = prevnext
        pn = ((f'<a class="pn" rel="prev" href="{prev[0]}" '
               f'aria-label="{attr(prev[1])}">&lsaquo;</a>' if prev else '')
              + (f'<a class="pn" rel="next" href="{nxt[0]}" '
                 f'aria-label="{attr(nxt[1])}">&rsaquo;</a>' if nxt else ''))
    pages = ''.join(
        f'<a href="{up}{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == active else ""}>'
        f'{esc(t)}</a>' for h, t in PAGES)
    return (
        f'<header class="bar">'
        f'<div class="bar-in">'
        f'<a class="bar-mark" href="{up}index.html">{IMP.wordmark_html(sep=" ")}</a>'
        f'<nav class="crumb" aria-label="You are here">{"".join(bits)}</nav>'
        f'<div class="bar-tools">{pn}'
        f'<form class="jump jsonly" role="search" action="{up}checklist.html" method="get">'
        f'<label class="vh" for="jump">Go to a Move by number or title</label>'
        f'<input id="jump" name="q" type="search" list="moves-list" autocomplete="off"'
        f' spellcheck="false" enterkeyhint="go" placeholder="Go to a Move">'
        f'<kbd aria-hidden="true">/</kbd>'
        f'<div class="jump-out" id="jump-out" hidden></div></form>'
        f'<datalist id="moves-list"></datalist>'
        f'<span class="bar-pct" id="now-pct" data-total="{len(moves)}">'
        f'0 / {len(moves)}</span>'
        f'<details class="pages"><summary>Pages</summary>'
        f'<nav aria-label="All pages">{pages}</nav></details>'
        f'</div></div>'
        f'{spine_html(stages, here)}'
        f'</header>')


def masthead(moves):
    """The wordmark, one sentence, and the five facts that place the book.

    On the front page only. It used to sit on all 131, which is a cover glued to
    the top of every page of the book it wraps."""
    bits = [f'<span>v{VERSION}</span>',
            f'<span><b>{len(moves)}</b> Moves</span>',
            f'<span><b>{len(ORDER)}</b> Stages</span>',
            f'<span>AWS &middot; Google Cloud &middot; Azure</span>',
            f'<span><a href="https://{IMP.ONEUPTIME_SITE}">{esc(IMP.BYLINE)}</a></span>']
    return (f'<header class="mast"><div class="mast-in">'
            f'<a class="wordmark" href="index.html">{IMP.wordmark_html()}</a>'
            f'<div class="mast-sub"><p>A step-by-step roadmap off AWS, Google Cloud '
            f'or Azure and onto Kubernetes you run on hardware you control.</p></div>'
            f'</div></header>'
            f'<div class="edition"><div class="edition-in">{"".join(bits)}</div></div>')


def rail(moves, stages, depth=0, here=None, active='', progress=False, page_links=''):
    """The printed book's fore-edge tab, stood on its side, and the site's primary
    navigation.

    It is on every page now rather than two, it carries every destination the site
    has, and the stage you are in opens into its own Moves - so any Move is one
    click from any other Move beside it, which used to cost a trip to a 7,600px
    list. Below 900px the same markup becomes a seven-cell strip across the top,
    because a phone has the axis for it and `display:none` is not a responsive
    strategy.
    """
    up = '../' * depth
    out = []
    for s in stages:
        info = LAYERS[s['layer']]
        on = here == s['layer']
        rows = ''
        if on:
            rows = '<ol class="r-moves">' + ''.join(
                f'<li data-n="{m["num"]}"><a href="{up}m/{slug(m)}.html"'
                f'{" aria-current=" + chr(34) + "page" + chr(34) if m["num"] == active else ""}>'
                f'<i>{m["num"]}</i><span>{esc(m["title"])}</span></a></li>'
                for m in moves if m['layer'] == s['layer']) + '</ol>'
        foot = (f'<span class="track"><i></i></span>'
                f'<span data-stage="{info["stage"]}">0/{s["count"]}</span>' if progress or on
                else f'<span>{s["first"]}&ndash;{s["last"]}</span>')
        out.append(
            f'<a class="r-s{" on" if on else ""}" data-part="{info["key"]}" '
            f'data-stage="{info["stage"]}" href="{up}s/{info["key"]}.html"'
            f'{" aria-current=" + chr(34) + "true" + chr(34) if on else ""}>'
            f'<span class="r-n"><span class="w">Stage </span>{info["stage"]}</span>'
            f'<span class="r-t">{esc(info["doing"])}</span>'
            f'<span class="r-w">{foot}</span></a>')
        out.append(rows)
    pages = ''.join(
        f'<a href="{up}{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == active else ""}>'
        f'{esc(t)}</a>' for h, t in PAGES)
    return (f'<nav class="rail" aria-label="Stages and pages">'
            f'<p class="lbl r-h">The seven stages</p>{"".join(out)}'
            f'{page_links}'
            f'<div class="r-pages"><p class="lbl r-h">Every page</p>{pages}</div>'
            f'</nav>')


def footer(depth=0):
    up = '../' * depth
    links = [f'<a href="{up}{h}">{lab}</a>' for h, lab in PAGES]
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
    return (f'<footer class="foot"><div class="foot-in">'
            f'<nav class="foot-links" aria-label="Every page">{"".join(links)}</nav>'
            f'<p class="ft">{esc(IMP.TITLE)}</p>'
            f'<p>Every Move states its cutover in minutes of user-visible downtime, its risk '
            f'as blast radius, and how long the thing it replaces must stay warm before you '
            f'turn it off. The schedule is computed from the Moves’ own effort figures and '
            f'the dependency graph, not asserted. Prices are public list rates observed while '
            f'writing and will drift. '
            f'<a href="{up}rollback.html">Read the rollback page</a> before running anything.</p>'
            f'{shop}'
            f'<p class="jsonly">Press <kbd>/</kbd> to jump to a Move by number or title, '
            f'<kbd>1</kbd>&ndash;<kbd>7</kbd> for a stage, and <kbd>&larr;</kbd> '
            f'<kbd>&rarr;</kbd> to turn the page on a Move.</p>'
            f'<p>{esc(IMP.BYLINE)} &mdash; '
            f'<a href="https://{IMP.ONEUPTIME_SITE}">{IMP.ONEUPTIME_SITE}</a>, '
            f'an open-source platform for uptime, incidents, on-call and status pages. '
            f'It is recommended in Part VII, and the interest is declared on the '
            f'<a href="{up}about.html">about page</a>.</p>'
            f'<p>Open source. The Moves and the typesetter that builds this are '
            f'<a href="{GH_URL}">on GitHub</a> — software MIT, text CC BY 4.0. '
            f'<span class="ver">v{VERSION}</span></p></div></footer>')


def page_head(title, lede, kicker=''):
    k = f'<p class="lbl">{esc(kicker)}</p>' if kicker else ''
    return (f'<div class="phead">{k}<h1 class="d">{title}</h1>'
            f'<p class="lede">{lede}</p></div>')


def risk_cell(m):
    return f'<span class="r-{m["risk"].lower()}">{m["risk"]}</span>'


# ---------------------------------------------------------------- shared data
# One record per Move, built once. The planner and the front page both inline the
# same bytes, so the two cannot drift and neither makes a request - both work
# from a file:// URL and off a USB stick in a datacentre with no signal.
def payload(moves):
    return [{
        'n': m['num'], 'slug': slug(m), 't': m['title'], 'p': m['l']['key'],
        'r': m['risk'], 'cut': m['cutover'], 'rev': m['reversible'],
        'was': m['was'], 'now': m['now'], 'eff': RM.effort_days(m),
        'deps': DEPS.get(m['num'], []), 'hook': m['hook'],
        'stage': m['l']['stage'], 'doing': m['l']['doing'],
        'effs': m['figures'][4], 'wait': m['figures'][5], 'oneway': m['oneway'],
    } for m in moves]


def data_block(moves):
    """The payload, inlined so the page makes no request and works from file://.

    `<` is escaped to its JSON unicode form: json.dumps does not escape it, the
    HTML parser ends a script element at the first `</script`, and a Move title
    is content. The escape is still valid JSON and JSON.parse returns the same
    string, so nothing downstream knows it happened."""
    data = json.dumps(payload(moves), separators=(',', ':')).replace('<', '\\u003c')
    return f'<script type="application/json" id="moves-data">{data}</script>'



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
    if m['figures'][5] not in ('—', ''):
        bits.append(('then wait', m['figures'][5]))
    return ''.join(f'<span><i>{k}</i>{esc(v)}</span>' for k, v in bits)


def answer(m, then, depth=0):
    """The answer to the only question the front page asks."""
    up = '../' * depth
    nxt = (f'<p class="ans-then"{"" if then else " hidden"}>'
           f'{("Then " + ", ".join(x["num"] for x in then) + ".") if then else ""}</p>')
    return (
        f'<section class="answer" id="answer" tabindex="-1" data-n="{m["num"]}" '
        f'data-part="{m["l"]["key"]}" aria-labelledby="ans-t">'
        f'<p class="ans-k">Stage {m["l"]["stage"]} &middot; {esc(m["l"]["doing"])}</p>'
        f'<p class="ans-note" id="ans-note" hidden></p>'
        f'<div class="ans-hd"><span class="ans-n" id="ans-n">{m["num"]}</span>'
        f'<h2 class="ans-t" id="ans-t"><a id="ans-a" href="{up}m/{slug(m)}.html">'
        f'{esc(m["title"])}</a></h2></div>'
        f'<p class="ans-hook" id="ans-hook">{inline(m["hook"])}</p>'
        f'<p class="ans-facts" id="ans-facts">{facts(m)}</p>'
        f'{nxt}'
        f'<p class="ans-act">'
        f'<a class="btn btn-p" id="ans-open" href="{up}m/{slug(m)}.html">'
        f'Open Move {m["num"]}</a>'
        f'<button class="btn" id="ans-tick" type="button" hidden>Mark {m["num"]} done</button>'
        f'<button class="btn" id="ans-undo" type="button" hidden>Undo</button>'
        f'<a class="ans-all" id="ans-all" href="{up}checklist.html#m-{m["num"]}">'
        f'Find it on the checklist</a></p>'
        f'<p class="vh" id="ans-said" role="status"></p>'
        f'<p class="ans-nojs">This page remembers what you have ticked when '
        f'JavaScript is on.</p>'
        f'</section>')


def symptom_index(by, depth=0, limit=None):
    up = '../' * depth
    rows = SYMPTOMS if limit is None else SYMPTOMS[:limit]
    return ''.join(
        f'<div class="sym"><div class="sq">{esc(q)}</div><div class="sl">' +
        ''.join(f'<a href="{up}m/{slug(by[n])}.html"><b>{n}</b>{esc(by[n]["title"])}</a>'
                for n in ns.split() if n in by) + '</div></div>'
        for q, ns in rows)


# ------------------------------------------------------------ the front page
def build_index(moves, stages):
    """One question, one answer.

    The answer is rendered by the build, not by script. Move 01 with nothing
    ticked is not a fallback - it is the correct answer for every reader on a
    first visit. JavaScript only substitutes a later Move once there is a tick
    to substitute it from.
    """
    by = {m['num']: m for m in moves}
    first, then = moves[0], moves[1:3]

    # Looked up by key rather than zipped by position: a Part that WHERE has not
    # been taught should fail the build, not render half a route drawn from the
    # Part next to it.
    by_stage = {s['layer']: s for s in stages}
    routes = ''.join(
        f'<button type="button" class="route" data-floor="{by_stage[k]["first"]}" '
        f'data-part="{LAYERS[k]["key"]}">'
        f'<span class="rt-s">{esc(where)}</span>'
        f'<span class="rt-m">Stage {LAYERS[k]["stage"]} &middot; '
        f'{esc(LAYERS[k]["doing"])} &middot; '
        f'Moves {by_stage[k]["first"]}&ndash;{by_stage[k]["last"]}'
        f'</span></button>'
        for k, where in WHERE)
    noscript = ''.join(
        f'<a class="route" data-part="{LAYERS[k]["key"]}" href="s/{LAYERS[k]["key"]}.html">'
        f'<span class="rt-s">{esc(where)}</span></a>' for k, where in WHERE)

    tail = ''.join(
        f'<a href="{h}"><span class="tl-t">{t}</span>'
        f'<span class="tl-s">{s}</span></a>' for h, t, s in [
            ('kit.html', 'Kit and what it costs',
             'The reference build, the homelab on-ramp and the arithmetic'),
            ('replaces.html', 'What replaces what',
             'Every managed service, on all three clouds, and what you run instead'),
            ('about.html', 'How this is made',
             'One source, two gates, and how to correct it')])

    body = f"""{masthead(moves)}
{chrome(0, moves, stages, 'index.html', crumb=[(None, 'What to do next')])}
<div class="shell">
{rail(moves, stages, 0, None, 'index.html')}
<main class="main" id="main">
  <div class="phead">
    <p class="lbl" id="q-where">Stage {first['l']['stage']} of {len(ORDER)}</p>
    <h1 class="d">What to do next</h1>
  </div>
  {answer(first, then)}
  {data_block(moves)}
  <script src="assets/next.js?v={VERSION}"></script>

  <section class="sec">
    <div class="sec-h"><h2 class="d">If that is not where you are</h2>
      <span class="lbl s-w">Pick the line that sounds like your estate</span></div>
    <fieldset class="routes jsonly"><legend class="vh">Where you are starting from</legend>
      {routes}</fieldset>
    <noscript><div class="routes">{noscript}</div></noscript>
  </section>

  <section class="sec" id="symptoms">
    <div class="sec-h"><h2 class="d">Where do I start</h2>
      <span class="lbl s-w">The real index</span></div>
    <p class="sec-b">When something on the bill or the pager has become intolerable and
    you do not want to read seven stages first, find it here and go straight to the Move.</p>
    <div class="syms">{symptom_index(by, 0, 6)}</div>
    <p class="actions"><a class="btn" href="symptoms.html">All {len(SYMPTOMS)} symptoms</a></p>
  </section>

  <div class="tail">{tail}</div>
</main>
</div>
{footer(0)}"""
    (SITE / 'index.html').write_text(shell(
        f'{IMP.TITLE} - what to do next', body, 0,
        f'The next Move to make in a migration off AWS, Google Cloud or Azure onto '
        f'Kubernetes you run yourself, out of {len(moves)} in seven stages.',
        core=False), encoding='utf-8')


# --------------------------------------------------------------- a checklist
def ck_row(m, depth=0):
    """One row: a tick box, a number, a title and - only where the fact changes
    what the reader does - one flag. A Move that cannot be undone says so; a Move
    that takes the site off the air says how long. Almost every row says neither,
    which is the correct rendering of nothing happening."""
    up = '../' * depth
    need = DEPS.get(m['num'], [])
    n = m['num']
    if m['oneway']:
        flag = '<span class="ck-flag warn">no way back</span>'
    elif m['cutover']:
        flag = f'<span class="ck-flag">{m["cutover"]} min down</span>'
    else:
        flag = ''
    rest = ''.join([
        (f'<span class="ck-need" data-need="{",".join(need)}">'
         f'after {", ".join(need)}</span>') if need else '',
        f'<span>{m["cutover"]} min</span>',
        f'<span class="r-{m["risk"].lower()}">{m["risk"]}</span>',
        f'<span>{esc(m["figures"][4])}</span>',
        (f'<span>+{esc(m["figures"][5])} wait</span>'
         if m['figures'][5] not in ('—', '') else ''),
    ])
    return (
        f'<li id="m-{n}" data-n="{n}" data-part="{m["l"]["key"]}" '
        f'data-stage="{m["l"]["stage"]}" data-deps="{",".join(need)}">'
        f'<label class="ck-b"><input type="checkbox" data-move="{n}" '
        f'aria-labelledby="n{n} t{n}">'
        f'<span class="ck-n" id="n{n}">{n}</span></label>'
        f'<a class="ck-t" id="t{n}" href="{up}m/{slug(m)}.html">{esc(m["title"])}</a>'
        f'{flag}<span class="ck-r">{rest}</span></li>')


def nums_toggle():
    """The figures strip's control. It is a checkbox the CSS reads, so it works
    with no script at all - and it has to be emitted beside every list of rows,
    or the figures those rows carry have nothing that can reveal them."""
    return ('<input type="checkbox" id="nums">'
            '<p class="nums-l"><label for="nums">Show the figures on every row</label>'
            '<span>Downtime, risk, effort, wait and what has to be done first</span></p>')


def lead_line(rows_in):
    """Lead times are the figure that wrecks a plan, and the only one worth
    promoting out of the hidden strip: nobody is working during a wait, so a Move
    ordered late holds up everything behind it."""
    early = [m for m in rows_in if RM.wait_days(m) >= 20]
    if not early:
        return ''
    return ('<p class="stg-lead"><b>Order early</b>' + ' &middot; '.join(
        f'{m["num"]} waits {esc(m["figures"][5])}' for m in early) + '</p>')


def build_checklist(moves, stages):
    """Every Move, in order, with a tick box each.

    The six figures that used to sit on every row are still built; they are hidden
    until the reader asks for them, because a column that reads `0 min` on a
    hundred and ten rows out of a hundred and twenty-two is not information."""
    first = moves[0]

    blocks = ''
    for st in stages:
        k = st['layer']
        info = LAYERS[k]
        rows_in = [x for x in moves if x['layer'] == k]
        rows = ''.join(ck_row(m) for m in rows_in)
        blocks += (
            f'<details class="stg" id="{info["key"]}" open '
            f'data-part="{info["key"]}" data-stage="{info["stage"]}">'
            f'<summary class="stg-h"><span class="stg-mk"></span>'
            f'<span class="lbl lbl-c">Stage {info["stage"]}</span>'
            f'<h2 class="d">{esc(info["doing"])}</h2>'
            f'<span class="lbl">{info["roman"]} &middot; Moves '
            f'{st["first"]}&ndash;{st["last"]}</span>'
            f'<span class="stg-prog"><span class="track"><i></i></span>'
            f'<span class="cnt">0/{st["count"]}</span></span>'
            f'</summary>'
            f'<p class="stg-done"><b>Done when</b>{esc(info["done"])}</p>'
            f'{lead_line(rows_in)}'
            f'<ol class="ck">{rows}</ol></details>')

    chips = ''.join(
        f'<button class="chip" type="button" data-part="{LAYERS[k]["key"]}" '
        f'data-stage="{LAYERS[k]["stage"]}" aria-pressed="false">'
        f'{LAYERS[k]["stage"]}</button>' for k in ORDER)

    body = f"""{chrome(0, moves, stages, 'checklist.html', crumb=[(None, 'The checklist')])}
<div class="shell">
{rail(moves, stages, 0, None, 'checklist.html', True)}
<main class="main" id="main">
  {page_head('The checklist', 'Work down it in order. The page remembers where you got '
             'to, in this browser and nowhere else.', f'All {len(moves)} Moves')}
  <p class="ck-lede" id="now-next">Nothing is ticked yet. The first Move is
    <a href="m/{slug(first)}.html"><b>{first['num']}</b>
    {esc(first['title'])}</a>, and it needs nothing before it.</p>
  <div class="filters jsonly">
    <span class="lbl">Stage</span>{chips}
    <button class="chip" type="button" data-todo aria-pressed="false">Not done</button>
    <button class="clear" type="button" id="ck-fold">Collapse all</button>
    <span class="fcount" id="ck-count">{len(moves)} of {len(moves)}</span>
  </div>
  {nums_toggle()}
  {blocks}
  <div class="ck-tools">
    <a class="btn" href="index.html">Back to what to do next</a>
    <button class="btn btn-w jsonly" id="ck-reset" type="button">Clear every tick</button>
    <button class="btn jsonly" id="ck-restart" type="button" hidden>Start from the beginning</button>
  </div>
</main>
</div>
<script src="assets/next.js?v={VERSION}"></script>
{footer(0)}"""
    (SITE / 'checklist.html').write_text(shell(
        f'The checklist - {IMP.TITLE}', body, 0,
        f'All {len(moves)} Moves for a migration off AWS, Google Cloud or Azure onto '
        f'Kubernetes you run yourself, in order, with a tick box each.',
        core=False), encoding='utf-8')


# --------------------------------------------------------------- a stage page
def build_stage(k, moves, stages):
    """The book's organising unit, given an address.

    The rail, the front page's routes and every Move's breadcrumb used to point at
    a fragment of one seven-thousand-pixel document. They point here."""
    info = LAYERS[k]
    st = next(s for s in stages if s['layer'] == k)
    rows_in = [m for m in moves if m['layer'] == k]
    idx = ORDER.index(k)
    prev = ORDER[idx - 1] if idx else None
    nxt = ORDER[idx + 1] if idx + 1 < len(ORDER) else None

    figs = ''.join(f'<div><b>{v}</b><span>{lab}</span></div>' for v, lab in [
        (st['count'], 'Moves'),
        (f'{st["person_days"]:.0f}', 'Person-days'),
        (f'{st["start_week"]}&ndash;{st["end_week"]}', 'Weeks'),
        (st['cutover'], 'Minutes of outage'),
        (sum(1 for m in rows_in if m['oneway']), 'Cannot be undone')])

    nav = ''.join(x for x in [
        (f'<a href="{LAYERS[prev]["key"]}.html"><b>Previous stage</b>'
         f'{LAYERS[prev]["stage"]} &middot; {esc(LAYERS[prev]["doing"])}</a>')
        if prev else '<span></span>',
        (f'<a href="{LAYERS[nxt]["key"]}.html"><b>Next stage</b>'
         f'{LAYERS[nxt]["stage"]} &middot; {esc(LAYERS[nxt]["doing"])}</a>')
        if nxt else '<span></span>'])

    body = f"""{chrome(1, moves, stages, '',
                       crumb=[('checklist.html', 'The checklist'),
                              (None, f'Stage {info["stage"]} · {info["doing"]}')],
                       here=k)}
<div class="shell">
{rail(moves, stages, 1, k, '', True)}
<main class="main" id="main" data-part="{info['key']}">
  {page_head(esc(info['doing']), esc(info['done']),
             f'Stage {info["stage"]} of {len(ORDER)} · {info["roman"]} · {k}')}
  <div class="figs">{figs}</div>
  {lead_line(rows_in)}
  <div class="sec">
    <div class="sec-h c"><h2 class="d">The {st['count']} Moves</h2>
      <span class="lbl s-w">Moves {st['first']}&ndash;{st['last']}</span></div>
    {nums_toggle()}
    <ol class="ck">{''.join(ck_row(m, 1) for m in rows_in)}</ol>
  </div>
  <nav class="mvnav" aria-label="Stage">{nav}</nav>
</main>
</div>
{footer(1)}"""
    (SITE / 's' / f'{info["key"]}.html').write_text(shell(
        f'Stage {info["stage"]} · {info["doing"]} - {IMP.TITLE}', body, 1,
        f'Stage {info["stage"]} of the migration: {info["doing"].lower()}. '
        f'{st["count"]} Moves, {info["done"]}'), encoding='utf-8')


# ------------------------------------------------------------- the roadmap page
def build_roadmap(moves, stages):
    sched = RM.schedule(moves, DEFAULT_CREW)
    cp = RM.critical_path(moves)
    zero = sum(1 for m in moves if m['cutover'] == 0)
    oneway = sum(1 for m in moves if m['oneway'])

    picks = ''
    for w in CREWS:
        picks += (f'<input type="radio" name="crew" id="w{w}"'
                  f'{" checked" if w == DEFAULT_CREW else ""}>')
    labels = ''.join(
        f'<label for="w{w}">{w} engineer{"" if w == 1 else "s"}</label>' for w in CREWS)
    views = ''
    for w in CREWS:
        sc = RM.schedule(moves, w)
        views += (
            f'<figure class="v{w}">'
            f'<p class="rm-ans">{sc["weeks"]:.0f} working weeks '
            f'<span>&mdash; about {sc["weeks"] / 46:.1f} years with {w} '
            f'engineer{"" if w == 1 else "s"}</span></p>'
            f'<div class="rm-wrap">'
            f'{RM.svg(moves, w, href=lambda m: "m/" + slug(m) + ".html")}</div>'
            f'<figcaption class="rm-cap">'
            f'<span><i class="out"></i>Critical path outlined</span>'
            f'<span>{sc["utilisation"]:.0%} utilisation</span></figcaption></figure>')

    figs = ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for v, k in [
        (len(moves), 'Moves'), (f'{sched["person_days"]:.0f}', 'Person-days'),
        (f'{cp["days"] / RM.WEEK:.0f}', 'Weeks, critical path'),
        (zero, 'At zero downtime'),
        (sum(m['cutover'] for m in moves), 'Minutes of outage'),
        (oneway, 'Cannot be undone')])

    # The same schedule as rows. Twenty-nine bars are too narrow to carry their
    # own number at three engineers, and a drawing is not reachable by keyboard.
    order = sorted(moves, key=lambda m: (sched['start'][m['num']], int(m['num'])))
    trows = ''.join(
        f'<tr data-part="{m["l"]["key"]}">'
        f'<td class="w">{int(sched["start"][m["num"]] // RM.WEEK) + 1}</td>'
        f'<td class="n">{m["num"]}</td>'
        f'<td><a href="m/{slug(m)}.html">{esc(m["title"])}</a></td>'
        f'<td class="w">{esc(m["figures"][4])}</td></tr>' for m in order)

    body = f"""{chrome(0, moves, stages, 'roadmap.html', crumb=[(None, 'How long it takes')])}
<div class="shell">
{rail(moves, stages, 0, None, 'roadmap.html')}
<main class="main" id="main">
  {page_head('How long it takes', f'''Every Move states its own effort, and every dependency
  points at an earlier Move, so this is calculated rather than drawn by hand: the critical
  path is {cp['days'] / RM.WEEK:.0f} weeks, and with {DEFAULT_CREW} engineers the whole book
  is about {sched['weeks']:.0f}. None of it is a promise &mdash; effort figures are estimates,
  and the constraint is usually the overlap window rather than the calendar.''',
             'Computed from the Moves, not asserted')}
  {picks}
  <fieldset class="rm-pick"><legend class="lbl">How many engineers</legend>{labels}</fieldset>
  <div class="rm-views">{views}</div>
  <div class="figs">{figs}</div>
  <details class="fold"><summary>The schedule as a table</summary>
    <table class="rm-table"><thead><tr><th scope="col">Week</th><th scope="col">Move</th>
      <th scope="col">Title</th><th scope="col">Effort</th></tr></thead>
      <tbody>{trows}</tbody></table>
    <p class="pnote">Weeks are for {DEFAULT_CREW} engineers. The drawing above follows the
    control; this table does not.</p></details>
</main>
</div>
{footer(0)}"""
    (SITE / 'roadmap.html').write_text(shell(
        f'How long it takes - {IMP.TITLE}', body, 0,
        'A computed schedule for the whole migration, and the critical path through it.'),
        encoding='utf-8')


# ---------------------------------------------------------------- a Move
def build_move(m, prev, nxt, by, moves, stages, sched):
    c = m['l']
    pres = ''
    for g in m['pre_groups']:
        pres += '<div class="pregroup">'
        if g['name']:
            pres += f'<p class="pre-h">{inline(g["name"])}</p>'
        pres += ('<ul class="prelist">' + ''.join(
            f'<li><label><input type="checkbox"><span>{inline(x)}</span></label></li>'
            for x in g['items']) + '</ul></div>')

    origins = ''.join(
        f'<div class="orow"><span class="oc">{esc(o["cloud"])}</span>'
        f'<span class="os">{inline(o["service"])}</span>'
        f'<span class="on">{inline(o["note"])}</span></div>' for o in m['origins'])

    # The ordinal in the gutter becomes the tick control, and it stays a plain
    # span until app.js can honour it. Rendering ARIA toggle buttons that cannot
    # be pressed is the one control on this page that would lie with no script.
    steps = ''.join(
        f'<li class="step"><span class="sdone" data-step="{i}">{i + 1:02d}</span>'
        f'<div class="stext">{inline(s)}</div></li>'
        for i, s in enumerate(m['steps']))

    notes = ''.join(f'<div class="note"><b>{inline(t)}</b><p>{inline(b)}</p></div>'
                    for t, b in m['notes'])

    labels = ['Was', 'Now', 'Saved', 'Cutover', 'Effort', 'Wait']
    figs = ''.join(f'<div><b>{esc(v)}</b><span>{k}</span></div>'
                   for v, k in zip(m['figures'], labels)
                   if str(v).strip() not in ('—', '', '-'))

    def deplinks(items, label, note):
        if not items:
            return ''
        return (f'<p class="pre-h">{label}</p><div class="deplist">' + ''.join(
            f'<a href="{slug(p)}.html" data-part="{p["l"]["key"]}">'
            f'<i>{p["num"]}</i><span>{esc(p["title"])}</span></a>' for p in items) +
            f'</div><p class="pnote">{note}</p>')

    wk = int(sched['start'][m['num']] // RM.WEEK) + 1
    rows_in = [x for x in moves if x['layer'] == m['layer']]
    pos = rows_in.index(m) + 1
    idx = moves.index(m)

    # Four cells, not six, and a cell whose value is an em dash says nothing
    # twice. Sixty-five of the 122 Moves used to render three blanks.
    cells = [('Part', f'<span data-part="{c["key"]}" style="color:var(--c)">'
                      f'{icon(c["key"], "1em", 1.7)}</span> {c["label"].upper()}', False)]
    if m['leaving'].strip() not in ('—', '', '-'):
        cells.append(('Leaving', esc(m['leaving']), False))
    cells.append(('Risk', f'{risk_bars(m["risk"], "currentColor", "1em")}'
                          f'{m["risk"].upper()}', False))
    if m['cutover']:
        cells.append(('Cutover', f'{m["cutover"]} MIN', False))
    cells.append(('Back out for',
                  'CANNOT BE UNDONE' if m['oneway'] else esc(m['reversible']).upper(),
                  m['oneway']))
    cells.append(('Roadmap', f'<a href="../roadmap.html">WEEK {wk}</a>', False))
    spec = ''.join(f'<div{" class=" + chr(34) + "warn" + chr(34) if w else ""}>'
                   f'<div class="k">{k}</div><div class="v">{v}</div></div>'
                   for k, v, w in cells)

    noway = ''
    if m['oneway']:
        noway = (f'<p class="noway"><b>No way back</b>Once this Move is finished there '
                 f'is no undo. Read the rollback section below before step one, and do '
                 f'not start it on the same day as anything else on this list.</p>')

    body = f"""{chrome(1, moves, stages, '',
                       crumb=[(f's/{c["key"]}.html', f'Stage {c["stage"]} · {c["doing"]}'),
                              (None, f'{m["num"]} · {m["title"]}')],
                       here=m['layer'],
                       prevnext=((f'{slug(prev)}.html', f'Move {prev["num"]}') if prev else None,
                                 (f'{slug(nxt)}.html', f'Move {nxt["num"]}') if nxt else None))}
<div class="shell">
{rail(moves, stages, 1, m['layer'], '', False, '')}
<main class="main" id="main" data-part="{c['key']}">
  <div class="mv-head">
    <div class="mv-pos">
      <span class="lbl">Move {m['num']} of {len(moves)}</span>
      <span class="lbl">{pos} of {len(rows_in)} in this stage</span>
    </div>
    <div class="mv-hd"><span class="mv-n">{m['num']}</span>
      <h1 class="d">{esc(m['title'])}</h1></div>
    <div class="mv-spec">{spec}</div>
  </div>
  <p class="hook">{inline(m['hook'])}</p>
  {noway}
  <p class="ans-act jsonly"><button class="btn" type="button" id="mv-tick"
    data-n="{m['num']}">Mark {m['num']} done</button></p>

  <section class="sec">
    <h2 class="blab" id="prep">Before you start</h2>
    <div class="precols">{pres}</div>
    {deplinks(dep_needs(m['num'], by), 'Needs first',
              'These must be finished before step one.')}
  </section>

  <section class="sec">
    <h2 class="blab blab-hi" id="runbook">The runbook
      <span class="lbl" id="step-count">0 of {len(m['steps'])} done</span></h2>
    <ol class="steps" id="steps" data-move="{m['num']}">{steps}</ol>
    <div class="rollback{' warn' if m['oneway'] else ''}"><b>Rollback</b>
      <p>{inline(m['rollback'])}</p></div>
  </section>

  <hr class="cut">
  <p class="lbl">Reference &mdash; everything below is read rather than run</p>
  <div class="work">
  <div>
    <h2 class="blab" id="why">Why this works</h2>
    <p class="why">{inline(m['why'])}</p>
    <h2 class="blab" id="leaving">Leaving from</h2>
    {origins}
    <h2 class="blab" id="notes">Operator&rsquo;s notes</h2>
    <div class="notes">{notes}</div>
    <h2 class="blab" id="turnoff">What you can turn off</h2>
    <p class="turnoff">{inline(m['turnoff'])}</p>
  </div>
  <aside>
    <h2 class="blab" id="numbers" style="margin-top:0">The numbers</h2>
    <div class="figs">{figs}</div>
    {deplinks(dep_unlocks(m['num'], by), 'Unlocks',
              'These become possible once this Move is done.')}
  </aside>
  </div>

  <nav class="mvnav" aria-label="Move">
    {f'<a href="{slug(prev)}.html"><b>Previous</b>{esc(prev["num"])} &middot; {esc(prev["title"])}</a>' if prev else '<span></span>'}
    {f'<a href="{slug(nxt)}.html"><b>Next</b>{esc(nxt["num"])} &middot; {esc(nxt["title"])}</a>' if nxt else '<span></span>'}
  </nav>
</main></div>
{footer(1)}"""
    (SITE / 'm' / f'{slug(m)}.html').write_text(shell(
        f'{m["num"]} · {m["title"]} - {IMP.TITLE}', body, 1, m['hook']),
        encoding='utf-8')

    # The numeric address. A Move had none: `m/87.html` is typeable, speakable
    # over a phone in a datacentre, and resolves with no script and from a
    # file:// URL. location.replace leaves no history entry, so Back from the
    # Move does not land here and get thrown forward again.
    (SITE / 'm' / f'{m["num"]}.html').write_text(
        f'<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
        f'<title>{esc(m["num"])} · {esc(m["title"])} - {esc(IMP.TITLE)}</title>\n'
        f'<link rel="canonical" href="{slug(m)}.html">\n'
        f'<meta name="robots" content="noindex">\n'
        f'<script>location.replace("{slug(m)}.html")</script>\n'
        f'<noscript><meta http-equiv="refresh" content="0;url={slug(m)}.html"></noscript>\n'
        f'</head>\n<body><p><a href="{slug(m)}.html">Move {esc(m["num"])} &mdash; '
        f'{esc(m["title"])}</a></p></body>\n</html>\n', encoding='utf-8')


# ---------------------------------------------------------------- the planner
def build_plan(moves, stages):
    picker = ''
    for k in ORDER:
        rows = [m for m in moves if m['layer'] == k]
        if not rows:
            continue
        picker += (f'<div class="pk-h" data-part="{LAYERS[k]["key"]}">'
                   f'<span class="lbl lbl-c">{LAYERS[k]["roman"]}</span>'
                   f'<h2 class="d">{esc(k)}</h2>'
                   f'<button class="clear" type="button" data-all="{LAYERS[k]["key"]}">'
                   f'Select all {len(rows)}</button></div>')
        for m in rows:
            # Sentence case, and only the figures that are not the same on every
            # row: 110 of 122 Moves print `0 min`, which is not information.
            bits = [esc(m['leaving'])] if m['leaving'].strip() not in ('—', '', '-') else []
            if m['cutover']:
                bits.append(f'{m["cutover"]} min down')
            if m['risk'] == 'High':
                bits.append('high risk')
            sub = f'<small>{" &middot; ".join(bits)}</small>' if bits else ''
            picker += (
                f'<label class="pk" data-layer="{LAYERS[k]["key"]}" '
                f'data-part="{m["l"]["key"]}">'
                f'<input type="checkbox" value="{m["num"]}">'
                f'<span class="pn">{m["num"]}</span>'
                f'<span><b>{esc(m["title"])}</b>{sub}</span></label>')

    body = f"""{chrome(0, moves, stages, 'plan.html', crumb=[(None, 'Plan yours')])}
<div class="shell">
{rail(moves, stages, 0, None, 'plan.html')}
<main class="main" id="main">
  {page_head('Plan yours', 'Tick the Moves you actually run. The planner pulls in everything '
             'those Moves depend on, orders it so nothing is asked for before it exists, and '
             'totals the downtime, the effort and the saving.', 'A subset, ordered')}
  <p class="pnote jsonly" style="margin-top:0">The selection lives in the address bar, so a
  plan is a link you can send to whoever has to approve it.</p>
  <p class="ans-nojs">The planner needs JavaScript to close the dependency set and total the
  figures. <a href="checklist.html">The checklist</a> has all {len(moves)} Moves in order
  without it, and every Move page names what it needs first.</p>
  <div class="planwrap work jsonly">
  <div class="picker">{picker}</div>
  <aside><div class="planout">
    <div class="sec-h"><h2 class="d">Your migration</h2></div>
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
    <div class="actions jsonly">
      <button class="btn" id="p-clear" type="button">Clear</button>
      <button class="btn" id="p-print" type="button">Print</button>
    </div>
  </div></aside>
  </div>
  {data_block(moves)}
</main></div>
{footer(0)}"""
    (SITE / 'plan.html').write_text(shell(
        f'Plan yours - {IMP.TITLE}', body, 0,
        'Pick the Moves you need and get an ordered plan with the downtime, the effort and '
        'the saving totalled.', scripts=('plan.js',)), encoding='utf-8')


# ------------------------------------------------------------- the symptom index
def build_symptoms(moves, stages):
    by = {m['num']: m for m in moves}
    body = f"""{chrome(0, moves, stages, 'symptoms.html', crumb=[(None, 'Where do I start')])}
<div class="shell">
{rail(moves, stages, 0, None, 'symptoms.html')}
<main class="main" id="main">
  {page_head('Where do I start', 'Nobody sits down at nine in the morning thinking in stages. '
             'They think &ldquo;the bill went up forty per cent and nobody can say why&rdquo;. '
             'Find the line that sounds like your week and go straight to the Move.',
             'The real index')}
  <div class="syms">{symptom_index(by)}</div>
  <p class="pnote">Every number here is checked against the built book, so a Move that is
  renumbered or removed turns the build red rather than leaving a dead reference on this page.</p>
</main></div>
{footer(0)}"""
    (SITE / 'symptoms.html').write_text(shell(
        f'Where do I start - {IMP.TITLE}', body, 0,
        'The symptom index: which Move answers which problem on the bill or the pager.'),
        encoding='utf-8')


def build_kit(moves, stages):
    shelves = ''.join(
        f'<div class="shelf" data-kit="{attr(name)}"><h3>{esc(name)}'
        f'<span class="cnt">0/{len(items)}</span></h3><div class="shelf-list">' +
        ''.join(f'<label><input type="checkbox"><span>{esc(i)}</span></label>'
                for i in items) + '</div></div>'
        for name, items in SHELVES)
    R = REFERENCE
    n = R['sites'] * R['nodes_per_site']
    o = COSTS.owned_month(R['sites'], R['nodes_per_site'])
    d = COSTS.dedicated_month(n)
    vcpu = n * R['cores_per_node'] * 2
    aws = vcpu * COSTS.AWS['ec2_vcpu_hour'] * 730
    mny = lambda v: f'${v:,.0f}'
    body = f"""{chrome(0, moves, stages, 'kit.html', crumb=[(None, 'Kit')])}
<div class="shell">
{rail(moves, stages, 0, None, 'kit.html')}
<main class="main" id="main">
  {page_head('Kit', f'''Every Move is written against one cluster, so a runbook can name a
  real thing rather than a category: {R["sites"]} sites, {R["nodes_per_site"]} nodes each,
  {R["cores_per_node"]} cores and {R["ram_gb_per_node"]} GB a node. Scale the numbers; do not
  scale away the redundancy.''', 'The reference build')}
  <section class="sec">
    <div class="sec-h"><h2 class="d">What to buy</h2>
      <span class="lbl s-w">Tick it off against a quote</span></div>
    <div class="shelves" id="kit">{shelves}</div>
  </section>
  <p class="pnote jsonly">Ticks are kept in this browser and go no further.
    <button class="lnk" type="button" id="kit-reset">Clear them</button></p>

  <section class="sec" data-part="iron">
    <div class="sec-h c"><h2 class="d">The on-ramp</h2>
      <span class="lbl s-w">Build this one first</span></div>
    <p class="sec-b">Almost nobody should sign a facility contract before they have run this
    stack once. {HOMELAB['nodes']} refurbished machines on a managed switch under a desk will
    run every Move in the Cluster and Platform stages unchanged &mdash; about
    {mny(COSTS.homelab_capex())} once and {mny(COSTS.homelab_month())} a month in electricity.
    It saves nothing, and that is not what it is for. What it cannot teach you is the Site
    stage, because a homelab has one power feed, one switch, no cross-connect and no second
    site.</p>
    <div class="shelves"><div class="shelf wide" data-kit="On-ramp">
      <h3>Under the desk<span class="cnt">0/{len(HOMELAB_KIT)}</span></h3>
      <div class="shelf-list">{''.join(
        f'<label><input type="checkbox"><span>{esc(k)}</span></label>'
        for k in HOMELAB_KIT)}</div></div></div>
  </section>

  <section class="sec" data-part="watch">
    <div class="sec-h c"><h2 class="d">What it costs</h2>
      <span class="lbl s-w">With the salary in it</span></div>
    <div class="grid2">
      <div class="gcard"><h3>On the cloud, compute alone</h3><p>{vcpu:,} vCPU on demand is
        <b>{mny(aws)}</b> a month before a gigabyte of storage, a load balancer or a byte of
        egress. 100 TB a month of egress is {mny(COSTS.egress_month(100))} on top.</p></div>
      <div class="gcard"><h3>Owned, two facilities</h3><p>{mny(o['infrastructure'])} of
        infrastructure plus {mny(o['people'])} of additional salaried time.
        <b>{mny(o['total'])}</b> a month, with redundancy the cloud figure does not
        include.</p></div>
      <div class="gcard"><h3>Rented by the month</h3><p>Dedicated hosts are
        {mny(d['infrastructure'])} and remove the racking, the spares and half a person:
        <b>{mny(d['total'])}</b> all in, with a supplier you can leave in thirty days.</p></div>
      <div class="gcard"><h3>What the difference buys</h3><p>About {mny(aws - o['total'])} a
        month against a capital outlay of {mny(n * COSTS.HARDWARE['node_capex'])}, paying for
        itself in roughly {n * COSTS.HARDWARE['node_capex'] / max(aws - o['total'], 1):.0f}
        months.</p></div>
    </div>
  </section>

  <section class="sec">
    <div class="sec-h"><h2 class="d">Ten rules</h2>
      <span class="lbl s-w">The spine of the argument</span></div>
    <div class="rules">{''.join(
      f'<div class="rule-i"><div class="rn">{i + 1:02d}</div>'
      f'<p><b>{esc(t)}</b> {esc(b)}</p></div>' for i, (t, b) in enumerate(RULES))}</div>
  </section>
</main></div>
{footer(0)}"""
    (SITE / 'kit.html').write_text(shell(f'Kit - {IMP.TITLE}', body, 0,
        'The reference build, the homelab on-ramp, what it costs with the salary in it, and '
        'the ten rules.'), encoding='utf-8')


def build_rollback(moves, stages):
    # Sequential advice, so it is numbered. The first point is the argument and
    # runs full width; the rest are a numbered list, not an anonymous matrix.
    lead, rest = RB_POINTS[0], RB_POINTS[1:]
    cards = ''.join(
        f'<div class="rule-i"><div class="rn">{i + 2:02d}</div>'
        f'<p><b>{esc(t)}</b> {esc(b)}</p></div>' for i, (t, b) in enumerate(rest))
    ow = [m for m in moves if m['oneway']]
    owblock = ''
    if ow:
        rows = ''.join(
            f'<tr data-part="{m["l"]["key"]}"><td class="c-n">{m["num"]}</td>'
            f'<td class="c-t"><a href="m/{slug(m)}.html">{esc(m["title"])}</a>'
            f'<p>{esc(m["hook"])}</p></td></tr>' for m in ow)
        owblock = (f'<section class="sec"><div class="sec-h">'
                   f'<h2 class="d">The Moves you cannot undo</h2>'
                   f'<span class="lbl s-w">{len(ow)} of {len(moves)}</span></div>'
                   f'<p class="sec-b">Everything else in this book has a way back. These do '
                   f'not, and each says so in its own Rollback section as well as here. '
                   f'Every one of them is High risk, because a Move you cannot undo is High '
                   f'by definition, so the risk is not printed against each row.</p>'
                   f'<table class="mv"><tbody>{rows}</tbody></table></section>')
    body = f"""{chrome(0, moves, stages, 'rollback.html',
                       crumb=[(None, 'Before you touch anything')])}
<div class="shell">
{rail(moves, stages, 0, None, 'rollback.html')}
<main class="main" id="main">
  {page_head('Before you touch anything', esc(rb_intro(len(ow))), 'Rollback and safety')}
  <div class="rules">
    <div class="rule-i"><div class="rn">01</div>
      <p><b>{esc(lead[0])}</b> {esc(lead[1])}</p></div>
    {cards}
  </div>
  {owblock}
  <p class="pnote">{esc(RB_DISC)}</p>
</main></div>
{footer(0)}"""
    (SITE / 'rollback.html').write_text(shell(
        f'Before you touch anything - {IMP.TITLE}', body, 0,
        'How to roll back, what a point of no return is, and the rule that a backup nobody '
        'restored is not a backup.'), encoding='utf-8')


def build_replaces(moves, stages):
    by = {m['num']: m for m in moves}
    heads = list(EQ_CLOUDS) + ['What you run instead']
    rows = ''.join(
        f'<tr class="{"keep" if r[3].lower().startswith("keep paying") else ""}">'
        + ''.join(f'<td data-h="{attr(heads[i])}">{esc(r[i])}</td>' for i in range(3))
        + f'<td class="yours" data-h="{attr(heads[3])}">{esc(r[3])}'
        + (f' <a href="m/{slug(by[r[4]])}.html">&rarr; {r[4]}</a>'
           if r[4] and r[4] in by else '')
        + '</td></tr>' for r in EQ_ROWS)
    body = f"""{chrome(0, moves, stages, 'replaces.html',
                       crumb=[(None, 'What replaces what')])}
<div class="shell">
{rail(moves, stages, 0, None, 'replaces.html')}
<main class="main" id="main">
  {page_head('What replaces what', 'Find the row you are paying for, then read the Move. '
             'Where the last column says keep paying, that is a conclusion rather than a gap.',
             'Every managed service, mapped')}
  <p class="pnote" style="margin-top:var(--s5)">Three rows are set in red. A global content
  network, scrubbing capacity at the edge and outbound mail deliverability are not technical
  problems nobody has solved. They are businesses, and you are not in them.</p>
  <div class="tablewrap" tabindex="0" role="region"
       aria-label="What replaces what, a scrollable table">
    <table class="eq">
    <caption class="lbl">{len(EQ_ROWS)} services &middot; scrolls sideways on a narrow
      screen, and stacks on a phone</caption>
    <thead><tr>{''.join(f'<th scope="col">{esc(h)}</th>' for h in heads)}</tr></thead>
    <tbody>{rows}</tbody></table></div>
</main></div>
{footer(0)}"""
    (SITE / 'replaces.html').write_text(shell(
        f'What replaces what - {IMP.TITLE}', body, 0,
        'Every managed service, its equivalent on all three clouds, and what you run instead.'),
        encoding='utf-8')


def build_about(moves, stages):
    paras = ''.join(f'<p>{p}</p>' for p in MISSION.paras(
        f'<a href="{GH_URL}">{IMP.REPO}</a>', len(moves)))
    pp = pdf_pages()
    facts_list = ''.join(f'<li>{k}<b>{v}</b></li>' for k, v in [
        ('Version', f'v{VERSION}'), ('Moves', len(moves)), ('Stages', len(ORDER)),
        ('Interior', f'{pp} pages' if pp else 'PDF'),
        ('Software', 'MIT'), ('Text', 'CC BY 4.0')])
    body = f"""{chrome(0, moves, stages, 'about.html', crumb=[(None, 'About')])}
<div class="shell">
{rail(moves, stages, 0, None, 'about.html',
      page_links=f'<div class="r-pages"><p class="lbl r-h">The edition</p>'
                 f'<ul class="facts">{facts_list}</ul></div>')}
<main class="main" id="main">
  {page_head(esc(' '.join(MISSION.HEADING_LINES)),
             'A handbook, not an argument. The argument has been had.',
             esc(MISSION.KICKER))}
  <div class="prose">{paras}</div>
  <section class="sec">
    <div class="sec-h"><h2 class="d">How it is made</h2>
      <span class="lbl s-w">Two gates, one source</span></div>
    <div class="grid2">
      <div class="gcard"><h3>One source of truth</h3><p>{len(moves)} markdown files are the
        whole book. A Python toolchain turns them into a {f"{pp}-page " if pp else ""}print
        interior, an EPUB and this site. Every number in any of them &mdash; page numbers,
        totals, the roadmap, the planner here &mdash; is derived from those files.</p></div>
      <div class="gcard"><h3>The schedule is computed</h3><p>The roadmap is not drawn by hand.
        It is list-scheduled from each Move&rsquo;s stated effort and the dependency graph, so
        it cannot drift from the Moves, and the critical path falls out of the same
        calculation.</p></div>
      <div class="gcard"><h3>Two gates</h3><p><code>verify.py</code> checks the shape of every
        Move: the sections, the three-cloud block, the cost arithmetic, and that no Move moving
        persistent state ships without saying how the state comes back. <code>audit.py</code>
        checks the content. Both must be clean.</p></div>
      <div class="gcard"><h3>Corrections</h3><p>The most valuable contribution is a correction.
        If you ran a runbook and it did not work as written, or a price is wrong for your
        region, that is worth an issue on its own.</p></div>
      <div class="gcard"><h3>Disclosure</h3><p>{esc(IMP.DISCLOSURE)}</p></div>
    </div>
  </section>
  <div class="actions"><a class="btn btn-p" href="{GH_URL}">View the repository</a>
    <a class="btn" href="{GH_URL}/blob/main/CONTRIBUTING.md">Add a Move</a></div>
</main></div>
{footer(0)}"""
    (SITE / 'about.html').write_text(shell(f'About - {IMP.TITLE}', body, 0,
        'Why the book exists, how it is built, and how to correct it.'), encoding='utf-8')


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
            page, _, frag = href.partition('#')
            page = page.partition('?')[0]      # the asset cache-buster
            target = (f.parent / page).resolve() if page else f.resolve()
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
    # One page per Move, so one slug per Move. verify.py checks this too; the
    # assertion is here because this is where the damage would happen - a
    # collision silently overwrites a page and the only symptom is a Move that
    # is not on the website.
    collisions = {}
    for m in moves:
        collisions.setdefault(slug(m), []).append(m['num'])
    clash = {s: ns for s, ns in collisions.items() if len(ns) > 1}
    assert not clash, f'moves share a slug and would overwrite each other: {clash}'
    # A Move whose title reduces to a bare number would collide with its own
    # numeric stub, which is the one filename in m/ the build writes twice.
    numeric = [s for s in collisions if s.isdigit()]
    assert not numeric, f'a Move slug is a bare number and collides with a stub: {numeric}'

    (SITE / 'm').mkdir(parents=True)
    (SITE / 's').mkdir(parents=True)
    ASSETS.mkdir(parents=True)

    (ASSETS / 'style.css').write_text(
        fonts_css() + (HERE / 'web' / 'style.css').read_text() + parts_css(),
        encoding='utf-8')
    for js in ('app.js', 'next.js', 'plan.js'):
        shutil.copy(HERE / 'web' / js, ASSETS / js)
    (ASSETS / 'moves-index.js').write_text(moves_index_js(moves), encoding='utf-8')

    by = {m['num']: m for m in moves}
    sched = RM.schedule(moves, DEFAULT_CREW)
    stages = RM.stages(moves, sched)
    build_index(moves, stages)
    build_checklist(moves, stages)
    build_roadmap(moves, stages)
    for k in ORDER:
        build_stage(k, moves, stages)
    for i, m in enumerate(moves):
        build_move(m, moves[i - 1] if i else None,
                   moves[i + 1] if i + 1 < len(moves) else None, by, moves, stages, sched)
    build_plan(moves, stages)
    build_symptoms(moves, stages)
    build_kit(moves, stages)
    build_rollback(moves, stages)
    build_replaces(moves, stages)
    build_about(moves, stages)

    for src, name in ((PDF_SRC, PDF_NAME), (EPUB_SRC, EPUB_NAME)):
        if src.exists():
            shutil.copy(src, SITE / name)

    bad = check_links()
    if bad:
        sys.exit(f'site: {len(bad)} dead links\n  ' + '\n  '.join(bad[:20]))

    n = sum(1 for _ in SITE.rglob('*') if _.is_file())
    mb = sum(f.stat().st_size for f in SITE.rglob('*') if f.is_file()) / 1e6
    print(f'site: {len(moves)} moves -> {n} files, {mb:.2f} MB in {SITE.name}/')


if __name__ == '__main__':
    main()
