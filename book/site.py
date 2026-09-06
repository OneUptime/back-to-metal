"""Generate the website from the same Move files that make the book.

The front page is a CHECKLIST: seven stages, each a tick list you work through,
remembering what you have done. That is the page somebody halfway through a
migration actually needs. The schedule drawing - which answers "how long", a
different question - lives on roadmap.html.

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
</head>
<body>
{body}
<script src="{up}assets/app.js{v}" defer></script>{more}
</body>
</html>"""


NAV = [('index.html', 'Start here'), ('roadmap.html', 'Roadmap'),
       ('plan.html', 'Plan yours'), ('kit.html', 'Kit'), ('rollback.html', 'Rollback'),
       ('replaces.html', 'What replaces what'), ('about.html', 'About')]


def nav(depth=0, active=''):
    up = '../' * depth
    parts = []
    for h, t in NAV:
        on = ' class="on"' if active and h.startswith(active) else ''
        parts.append(f'<a href="{up}{h}"{on}>{t}</a>')
    dl = ''
    if PDF_SRC.exists():
        dl += f'<a class="sp" href="{up}{PDF_NAME}" download>PDF</a>'
    if EPUB_SRC.exists():
        dl += f'<a href="{up}{EPUB_NAME}" download>EPUB</a>'
    dl += f'<a href="{GH_URL}">Source</a>'
    return f'<nav class="nav">{"".join(parts)}{dl}</nav>'


def masthead(moves, depth=0, sub=None):
    up = '../' * depth
    cp = RM.critical_path(moves)
    sc = RM.schedule(moves, DEFAULT_CREW)
    zero = sum(1 for m in moves if m['cutover'] == 0)
    bits = [f'<span>v{VERSION}</span>',
            f'<span><b>{len(moves)}</b> Moves</span>',
            f'<span><b>{len(ORDER)}</b> Parts</span>',
            f'<span><b>{sc["person_days"]:.0f}</b> person-days</span>',
            f'<span><b>{sc["weeks"]:.0f}</b> weeks at {DEFAULT_CREW}</span>',
            f'<span><b>{zero}</b> at zero downtime</span>',
            f'<span>AWS &middot; Google Cloud &middot; Azure</span>',
            f'<span><a href="https://{IMP.ONEUPTIME_SITE}" style="color:inherit">'
            f'{esc(IMP.BYLINE)}</a></span>']
    lede = sub or ('A step-by-step roadmap off AWS, Google Cloud or Azure and onto '
                   'Kubernetes you run on hardware you control. Every Move states its '
                   'downtime, its risk and the way back.')
    return (f'<header class="mast"><div class="mast-in">'
            f'<a class="wordmark d" href="{up}index.html">{IMP.wordmark_html()}</a>'
            f'<div class="mast-sub"><p>{lede}</p></div></div>'
            f'<div class="edition">{"".join(bits)}</div></header>')


def rail(moves, sched, depth=0, here=None):
    up = '../' * depth
    out = []
    for s in RM.stages(moves, sched):
        on = ' class="on"' if here == s['layer'] else ''
        out.append(
            f'<a{on} href="{up}index.html#{LAYERS[s["layer"]]["key"]}" '
            f'style="--c:{s["color"]}">'
            f'<div class="r-n">Stage {LAYERS[s["layer"]]["stage"]}</div>'
            f'<div class="r-t">{esc(LAYERS[s["layer"]]["doing"])}</div>'
            f'<div class="r-w">{s["first"]}&ndash;{s["last"]} &middot; '
            f'{esc(s["layer"])}</div></a>')
    return f'<aside class="rail">{"".join(out)}</aside>'


def footer(depth=0):
    up = '../' * depth
    shop = ''
    if IMP.on_amazon():
        ps = [f'<a href="{IMP.amazon_url(k)}">{lab}</a>' for k, lab in
              [('paperback', 'paperback'), ('hardback', 'hardcover'), ('kindle', 'Kindle')]
              if IMP.amazon_url(k)]
        shop = f'<p>Also on Amazon in {", ".join(ps)}.</p>'
    return (f'<footer class="foot"><p class="ft">{esc(IMP.TITLE)}</p>'
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


# ------------------------------------------------------- the checklist (front)
def build_index(moves):
    """The front page: seven stages, each a tick list you work through.

    This used to be the roadmap chart, which looked impressive and answered the
    wrong question. A reader halfway through a migration does not need to know
    how long the whole thing takes; they need to know what to do next. The chart
    now lives on its own page and this one is a checklist that remembers where
    you got to.
    """
    by = {m['num']: m for m in moves}
    sched = RM.schedule(moves, DEFAULT_CREW)
    stages = RM.stages(moves, sched)

    entry = ''.join(
        f'<a href="#{LAYERS[k]["key"]}" style="--c:{LAYERS[k]["color"]}">'
        f'<div class="e-k">{esc(where)}</div>'
        f'<div class="e-t">Start at stage {LAYERS[k]["stage"]}, '
        f'{esc(LAYERS[k]["doing"].lower())}.</div></a>'
        for k, where in [
            ('Iron', 'Nothing bought yet'),
            ('Cluster', 'Hardware racked, no cluster'),
            ('Platform', 'Cluster up, nothing on it'),
            ('Data', 'Apps moved, data still rented'),
            ('Watch', 'All moved, still paying'),
        ])

    blocks = ''
    for st in stages:
        k = st['layer']
        info = LAYERS[k]
        rows = ''
        for m in [x for x in moves if x['layer'] == k]:
            need = DEPS.get(m['num'], [])
            after = (f'<span class="ck-need" data-need="{",".join(need)}">'
                     f'after {", ".join(need)}</span>') if need else ''
            rows += (
                f'<li data-n="{m["num"]}" data-deps="{",".join(need)}">'
                f'<label><input type="checkbox" data-move="{m["num"]}">'
                f'<span class="ck-n">{m["num"]}</span>'
                f'<span class="ck-t">{esc(m["title"])}</span></label>'
                f'<span class="ck-r">{after}'
                f'<span>{m["cutover"]} min</span>'
                f'<span class="r-{m["risk"].lower()}">{m["risk"]}</span>'
                f'<span>{esc(m["figures"][4])}</span>'
                + (f'<span>+{esc(m["figures"][5])} wait</span>'
                   if m['figures'][5] not in ('—', '') else '')
                + f'<a href="m/{slug(m)}.html">Open</a></span></li>')
        blocks += (
            f'<section class="stg" id="{info["key"]}" data-stage="{info["stage"]}" '
            f'style="--c:{info["color"]}">'
            f'<header class="stg-h">'
            f'<span class="stg-n">Stage {info["stage"]}</span>'
            f'<h2 class="d">{esc(info["doing"])}</h2>'
            f'<span class="stg-part">{info["roman"]} &middot; {esc(k)} &middot; '
            f'Moves {st["first"]}&ndash;{st["last"]}</span>'
            f'<span class="stg-prog"><span class="track"><i></i></span>'
            f'<span class="cnt">0/{st["count"]}</span></span>'
            f'</header>'
            f'<p class="stg-done"><b>Done when</b>{esc(info["done"])}</p>'
            f'<ol class="ck">{rows}</ol></section>')

    body = f"""{masthead(moves)}
{nav(0, 'index')}
<div class="shell">
{rail(moves, sched)}
<main class="main">
  <section class="now">
    <div class="now-h"><h2 class="d">Where you are</h2>
      <span class="now-k">Ticks are saved in this browser</span></div>
    <p class="now-next" id="now-next">Nothing ticked yet. The first Move is
      <a href="m/{slug(moves[0])}.html"><b>{moves[0]['num']}</b>
      {esc(moves[0]['title'])}</a>, and it needs nothing before it.</p>
    <div class="now-bar"><span class="track"><i id="now-fill"></i></span>
      <span class="pct" id="now-pct">0 of {len(moves)} done</span></div>
    <div class="entry">{entry}</div>
  </section>
  {blocks}
  <div class="ck-tools">
    <button class="btn" id="ck-reset">Clear every tick</button>
    <a class="btn" href="roadmap.html">See how long it takes</a>
    <a class="btn" href="plan.html">Plan a subset</a>
  </div>
</main>
</div>
{footer(0)}"""
    (SITE / 'index.html').write_text(shell(
        f'{IMP.TITLE} - start here', body, 0,
        f'A {len(stages)}-stage checklist for moving off AWS, Google Cloud or Azure onto '
        f'Kubernetes you run yourself. Tick each Move off as you go.'), encoding='utf-8')


# ------------------------------------------------------------- the roadmap page
def build_roadmap(moves):
    by = {m['num']: m for m in moves}
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

    syms = ''.join(
        f'<div class="sym"><div class="sq">{q}</div><div class="sl">' +
        ''.join(f'<a href="m/{slug(by[n])}.html"><b>{n}</b>{esc(by[n]["title"])}</a>'
                for n in ns.split() if n in by) + '</div></div>'
        for q, ns in SYMPTOMS)

    body = f"""{masthead(moves, 0, 'How long the whole thing takes, and which Moves are on '
                'the critical path. The checklist is where you actually work.')}
{nav(0, 'roadmap')}
<div class="shell">
{rail(moves, sched)}
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
  <section class="stg" id="symptoms" style="--c:var(--ink)">
    <header class="stg-h"><span class="stg-n">&sect;</span>
      <h2 class="d">Where do I start</h2>
      <span class="stg-part">The real index</span></header>
    <p class="stg-done"><b>Use this</b>when something on the bill or the pager has become
      intolerable and you do not want to read seven stages first.</p>
    <div class="syms">{syms}</div>
  </section>
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
    all_moves = sorted(by.values(), key=lambda x: x['num'])
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
    payload = [{
        'n': m['num'], 'slug': slug(m), 't': m['title'], 'l': m['layer'],
        'c': m['l']['color'], 'lv': m['leaving'], 'r': m['risk'], 'cut': m['cutover'],
        'rev': m['reversible'], 'was': m['was'], 'now': m['now'],
        'eff': RM.effort_days(m), 'deps': DEPS.get(m['num'], []), 'hook': m['hook'],
    } for m in moves]

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
<div class="shell">
{rail(moves, RM.schedule(moves, DEFAULT_CREW))}
<main class="main"><div class="planwrap">
  <div>{picker}</div>
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
    (ASSETS / 'moves.json').write_text(json.dumps(payload, separators=(',', ':')),
                                       encoding='utf-8')


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
{nav(0, 'kit')}
<div class="shell">
{rail(moves, RM.schedule(moves, DEFAULT_CREW))}
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
<div class="shell">
{rail(moves, RM.schedule(moves, DEFAULT_CREW))}
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
{nav(0, 'replaces')}
<div class="shell">
{rail(moves, RM.schedule(moves, DEFAULT_CREW))}
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
{nav(0, 'about')}
<div class="shell">
{rail(moves, RM.schedule(moves, DEFAULT_CREW))}
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
    for js in ('app.js', 'plan.js'):
        shutil.copy(HERE / 'web' / js, ASSETS / js)

    by = {m['num']: m for m in moves}
    sched = RM.schedule(moves, DEFAULT_CREW)
    build_index(moves)
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
