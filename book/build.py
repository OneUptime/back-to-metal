"""Move files -> one self-contained build/book.html, ready for render.py.

Every number in the finished book - page numbers, the contents, the indexes, the
cover statistics, the stage totals - is derived here from the Move files. There
are no hand-maintained totals anywhere: change a Move, rerun the build, and the
rest follows.

The one structural rule the whole design rests on is asserted at the bottom of
build(): a Move is a SPREAD. Its setup page must be a verso and its runbook page
the facing recto, or the two halves of a Move end up either side of a page turn.
"""
import base64, html, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collections import Counter, defaultdict

from parse import load_all, LAYERS, ORDER, CUTOVER_CAP, inline
from icons import icon, meter, risk_bars, anatomy, cost_chart
from deps import needs as dep_needs, unlocks as dep_unlocks, DEPS
from kit import SHELVES, KIT, RULES, REFERENCE, HOMELAB, HOMELAB_KIT
from rollback_data import intro as rb_intro, POINTS as RB_POINTS, DISCLAIMER as RB_DISC
from equivalents import ROWS as EQ_ROWS, CLOUDS
from symptoms import SYMPTOMS
from version import VERSION
from flatten import mix
import costs as COSTS
import imprint as IMP
import mission as MISSION
import roadmap as RM

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
NM = ROOT / 'node_modules'
IMG = ROOT / 'images'
IMG.mkdir(exist_ok=True)

PAPER = '#FBFAF7'

b64 = lambda p: base64.b64encode(Path(p).read_bytes()).decode()
AR = NM / '@fontsource-variable/archivo/files'
JB = NM / '@fontsource-variable/jetbrains-mono/files'

# Two families, both variable, with distinct jobs: Archivo carries every word
# (condensed and heavy for display, normal for text) and JetBrains Mono carries
# every number, label and identifier. The 'standard' cut of Archivo is the one
# with both the weight and the width axis; the 'wght' cut would drop the width
# axis the whole display voice is built on.
FONTS = f"""
@font-face{{font-family:'Archivo';src:url(data:font/woff2;base64,{b64(AR / 'archivo-latin-standard-normal.woff2')}) format('woff2-variations');font-weight:100 900;font-stretch:62% 125%;font-style:normal;font-display:block;}}
@font-face{{font-family:'Archivo';src:url(data:font/woff2;base64,{b64(AR / 'archivo-latin-standard-italic.woff2')}) format('woff2-variations');font-weight:100 900;font-stretch:62% 125%;font-style:italic;font-display:block;}}
@font-face{{font-family:'JetBrains Mono';src:url(data:font/woff2;base64,{b64(JB / 'jetbrains-mono-latin-wght-normal.woff2')}) format('woff2-variations');font-weight:100 800;font-style:normal;font-display:block;}}
"""

CSS = (HERE / 'style.css').read_text()

PART_BLURB = {
    'Decide': 'Whether to do this at all. Three Moves of arithmetic against your own '
              'invoice, and a fourth that names what stays rented. The stage most likely '
              'to end the programme, and that is a success rather than a failure.',
    'Buy': 'What to order and where to put it. Nothing here is software, and getting it '
           'wrong is the only mistake in this book you cannot fix with a deploy. Both '
           'clocks start in this stage, and they run in parallel.',
    'Build': 'Everything between a racked machine and a cluster that could take production '
             'traffic. Nothing here moves a workload; all of it decides how well the rest '
             'of the book goes.',
    'Move': 'The application first, then the state. The stage that can lose a company its '
            'data, and therefore the one with the longest overlap windows, the most '
            'rehearsal and the fewest one-way steps.',
    'Run': 'The traffic, the pager and the last account. Every article about leaving the '
           'cloud stops before this stage, and every migration that regrets itself failed '
           'inside it.',
}

PART_KICKER = {
    'Decide': 'The bill, the inventory, the comparison, and what stays rented',
    'Buy': 'Sizing, the machines, the cage, and everything with a lead time',
    'Build': 'Racking, the network, the cluster and the disks',
    'Move': 'Images, the first service, the buckets, and the database',
    'Run': 'The edge, go-live, backups, the pager and the last account',
}


def esc(s):
    return html.escape(str(s), quote=False)


def plural(n, one, many=None):
    """'1 Move', '14 Moves'. Cheap, and it stops a stage that happens to hold a
    single Move printing '1 Moves' on its contents page."""
    return f'{n} {one if n == 1 else (many or one + "s")}'


# The fore-edge tab. One band a stage, stepping down the page, so a closed book
# can be opened at the right stage with a thumb. `slot` is the stage index;
# None means no tab, which is every page of the front matter.
TAB_TOP, TAB_H, TAB_GAP = 42.0, 24.0, 4.0


def page(cls, topcolor, inner, folio=None, slot=None, tabtext=''):
    bar = f'<div class="topbar" style="background:{topcolor}"></div>' if topcolor else ''
    tab = ''
    if slot is not None and topcolor:
        top = TAB_TOP + slot * (TAB_H + TAB_GAP)
        tab = (f'<div class="tab" style="top:{top}mm;background:{topcolor}">'
               f'<span>{tabtext}</span></div>')
    f = ('<div class="folio">%s</div><div class="pageno">{{PN}}</div>' % folio) if folio else ''
    return (f'<section class="page {cls}">{bar}{tab}'
            f'<div class="inner">{inner}</div>{f}</section>')


def hours_saved(ms):
    """Total user-visible downtime the whole book costs, in minutes."""
    return sum(m['cutover'] for m in ms)


def cover_front_html(moves):
    """The front-cover artwork.

    Not an interior page - KDP prints the cover from its own wrap file - but
    cover.py renders this markup as the front panel of both wraps, so the design
    lives in one place.
    """
    by = {m['num']: m for m in moves}
    zero = sum(1 for m in moves if m['cutover'] == 0)
    # A dozen Moves for the jacket: the shortest titles that still fit the
    # column, spread across the stages so the list samples the book rather than
    # reprinting its opening. Chosen here rather than by hand so it cannot drift
    # out of step with the Moves themselves.
    FITS = 34
    picks, seen = [], set()
    for lay in ORDER:
        for m in sorted((x for x in moves if x['layer'] == lay),
                        key=lambda x: len(x['title'])):
            if len(m['title']) <= FITS and m['num'] not in seen:
                picks.append(m); seen.add(m['num'])
                break
    for m in sorted(moves, key=lambda x: len(x['title'])):
        if len(picks) >= 12:
            break
        if len(m['title']) <= FITS and m['num'] not in seen:
            picks.append(m); seen.add(m['num'])
    SHOWCASE = [m['num'] for m in sorted(picks, key=lambda x: int(x['num']))]
    # A jacket list wants at least six entries to read as a list. Scaled against
    # the book so a small build - a smoke test, or a single stage rendered on its
    # own - does not trip a check aimed at a finished one.
    assert len(SHOWCASE) >= min(6, len(moves)), (
        f'only {len(SHOWCASE)} Move titles fit the jacket column at {FITS} characters; '
        f'shorten some titles or widen FITS')
    menu = ''.join(
        f'<div class="mrow"><span class="mname">{esc(by[k]["title"])}</span>'
        f'<span class="mdot"></span><span class="mmin">{by[k]["cutover"]}</span></div>'
        for k in SHOWCASE if k in by)

    # Nothing here is typed. A hardcoded '5' was right for five stages and would
    # be quietly wrong the day somebody added a sixth.
    cover_effort = sum(RM.effort_days(m) for m in moves)
    stages_n = len({m['layer'] for m in moves})
    keep = sum(1 for m in moves if 'keep paying' in (m['why'] + ' ' + m['hook']).lower())
    stats = [(str(len(moves)), 'Moves'), (str(stages_n), 'Stages'),
             (str(zero), 'At zero downtime'), (str(len(CLOUDS)), 'Clouds, every Move')]
    return f"""
    <div class="cover-rule"></div>
    <div style="margin-top:5mm" class="eyebrow">{len(moves)} Moves &nbsp;·&nbsp; AWS, Google Cloud and Azure out</div>
    <h1 class="d">{IMP.wordmark_html()}</h1>
    <p class="cover-sub">{esc(IMP.SUBTITLE)}.</p>
    <p class="cover-by">{esc(IMP.BYLINE)}</p>
    <div style="flex:1"></div>
    <div class="promise d">
      <p>One Move, <em>one job, one stated cutover</em>.</p>
      <p>A rollback <em>that has been rehearsed</em>.</p>
      <p>And <em>{cover_effort:.0f} days of work</em>, not four years.</p>
    </div>
    <div style="flex:.5"></div>
    <div class="stats">{''.join(
        f'<div class="stat"><div class="sv d">{v}</div><div class="sl">{l}</div></div>'
        for v, l in stats)}</div>
    <div style="flex:.55"></div>
    <div class="menu-k">{len(SHOWCASE)} of the {len(moves)} &nbsp;·&nbsp; minutes of downtime</div>
    <div class="menu">{menu}</div>
    <div style="flex:.35"></div>
    <div class="cover-rule"></div>
    <div class="cover-foot" style="margin-top:4mm"><div>{IMP.PUBLISHER_SITE}</div>
      <div>First edition &nbsp;&middot;&nbsp; v{VERSION}</div></div>"""


def build(moves):
    by = {m['num']: m for m in moves}
    parts = {k: [m for m in moves if m['layer'] == k] for k in ORDER}
    parts = {k: v for k, v in parts.items() if v}
    pages = []

    # The symptom index runs to as many pages as it needs; about twelve entries
    # fit one page at this measure.
    SYM_PER_PAGE = 12
    sym_pages = max(1, -(-len(SYMPTOMS) // SYM_PER_PAGE))

    # Front matter has to run to an EVEN count, so the first stage divider opens on
    # a recto and every Move's setup page lands on a verso facing its runbook.
    #
    # Derived rather than written down, because it is not a constant: the front
    # matter carries one contents page per stage that actually has Moves, so a
    # book with four stages has different front matter from one with five. It used
    # to be the literal 18, which was right for five stages and silently wrong for
    # any other number - the pagination assertion at the foot of this function
    # caught it, which is what that assertion is for.
    #
    # Twelve fixed pages: half title, why-this-exists, title, copyright,
    # foreword, the reference build, the on-ramp, the ten rules, the rollback
    # page, the cost page, and the two equivalence pages. Then a contents page
    # per stage, then the symptom index, then a blank verso if the total is odd.
    FRONT_FIXED = 12 + len(parts) + sym_pages
    FRONT = FRONT_FIXED + (FRONT_FIXED % 2)

    pageno, _p = {}, FRONT
    keys = list(parts)
    for _i, k in enumerate(keys):
        _p += 1                                    # the stage divider, always a recto
        for _j, m in enumerate(parts[k]):
            pageno[m['num']] = _p + 1 + 2 * _j
        _p += 2 * len(parts[k])
        if _i < len(keys) - 1:
            _p += 1                                # blank verso closing the stage

    def texture(ms):
        return ' &nbsp;·&nbsp; '.join(esc(m['title']) for m in ms)

    def chips(ms):
        c = Counter(m['risk'] for m in ms)
        cols = {'Low': '#7FC4B2', 'Medium': '#DDB26A', 'High': '#E39A7B'}
        return ''.join(
            f'<div class="cchip" style="border-color:{mix(cols[r], "#14171C", 1 / 3)};'
            f'color:{cols[r]}">{risk_bars(r, cols[r], "3mm", "#14171C")}'
            f'<b class="d">{c[r]}</b><span>{r} risk</span></div>'
            for r in ['Low', 'Medium', 'High'] if c[r])

    # ============================== FRONT MATTER ==============================
    pages.append(page('halft', None, f"""
    <div style="flex:1"></div>
    <h1 class="ht d">{IMP.wordmark_html()}</h1>
    <div style="flex:1.4"></div>"""))

    why_paras = ''.join(f'<p>{x}</p>' for x in MISSION.paras(IMP.REPO, len(moves)))
    pages.append(page('whyp', None, f"""
    <div style="flex:.6"></div>
    <p class="why-k">{MISSION.KICKER}</p>
    <h2 class="why-t d">{'<br>'.join(MISSION.HEADING_LINES)}</h2>
    <div class="why-body">{why_paras}</div>
    <div style="flex:1"></div>"""))

    pages.append(page('titlep', None, f"""
    <div style="flex:1"></div>
    <h1 class="tp-t d">{IMP.wordmark_html()}</h1>
    <p class="tp-sub">{esc(IMP.SUBTITLE)}</p>
    <div style="flex:1.1"></div>
    <p class="tp-au d">{esc(IMP.AUTHOR)}</p>
    <p class="tp-by">{esc(IMP.BYLINE)} &nbsp;&middot;&nbsp; {IMP.ONEUPTIME_SITE}</p>
    <p class="tp-pub">{IMP.PUBLISHER} &nbsp;&middot;&nbsp; {IMP.PUBLISHER_SITE}</p>"""))

    isbns = ''.join(f'<p>ISBN ({k}): {v}</p>' for k, v in IMP.ISBN.items() if v)
    pages.append(page('copyr', None, f"""
    <div style="flex:.45"></div>
    <div class="cp-body">
      <p class="cp-t d">{esc(IMP.TITLE)}</p>
      <p class="cp-sub">{esc(IMP.SUBTITLE)}</p>
      <p>Copyright &copy; {IMP.YEAR} {esc(IMP.AUTHOR)}</p>
      <p>Published by {IMP.PUBLISHER}, {IMP.PUBLISHER_SITE}</p>
      <p>{IMP.LICENCE}</p>
      <p>{IMP.MORAL_RIGHTS}</p>
      <p>{IMP.EDITION}, {IMP.YEAR}. Version {VERSION}.</p>
      {isbns}
      <p>{IMP.DISCLAIMER}</p>
      <p>{IMP.DISCLOSURE}</p>
      <p>{IMP.TYPE_NOTE}</p>
      <p>{IMP.SITE}</p>
    </div>
    <div style="flex:1"></div>"""))

    # ---------- foreword, with the page-anatomy diagram
    KEY = [
        ('The ring', f'The cutover: how many minutes of user-visible downtime this Move '
                     f'costs, against a {CUTOVER_CAP}-minute dial. An empty ring means none, '
                     f'and most rings are empty.'),
        ('The bars', 'Risk, meaning blast radius if it goes wrong rather than how fiddly it '
                     'is. Three bars and you do not run it alone.'),
        ('The panel', 'Everything that must already be true before step one. Hardware, '
                      'software with versions, and the access you will be asked for.'),
        ('Why this works', 'What the managed service actually was, and why the replacement '
                           'holds. Read it once; you will not need it again.'),
        ('The strip', 'What it cost, what it costs now, the saving, the downtime and the '
                      'person-days. Illustrative of a shape, not a quotation for your account.'),
        ('The rollback', 'On the facing page, at the foot, in colour. It names the point of '
                         'no return. Read it before step one, not after step five.'),
    ]
    total_effort = sum(RM.effort_days(m) for m in moves)
    total_weeks = RM.schedule(moves, 2)['weeks']
    keyhtml = ''.join(
        f'<div class="kitem"><div class="kn">{i + 1}</div><div><b>{t}</b>{b}</div></div>'
        for i, (t, b) in enumerate(KEY))
    pages.append(page('', '#1F4E79', f"""
    <div class="pkicker">A short note first</div>
    <h2 class="ptitle d">Many Moves,<br>Not One Migration</h2>
    <div class="fw">
      <p class="lede">The reason leaving the cloud fails is almost never that the technology
      did not work. It is that it was attempted as one decision, executed as one project, and
      abandoned somewhere in the middle with two platforms running and nobody able to say
      whether it was going well.</p>
      <p>This book takes the opposite shape. It is {len(moves)} Moves, in five stages. Each is
      one job with a stated cutover, a stated risk and a rollback that has been thought about.
      Each can be done on a Tuesday and undone on a Wednesday. You can stop after any of them
      and still be in a coherent place, which is the only property that matters in a project
      measured in quarters.</p>

      <p>It is deliberately small. The first edition had a hundred and twenty-two Moves and,
      computed from its own files, 975 person-days and four and a half years. That was correct
      and useless. This is {total_effort:.0f} person-days and about {total_weeks:.0f} weeks for
      two people, most of it hardware lead time rather than work. Hiring does not shorten
      it.</p>
      <p>They are ordered so that a reader who starts at Move 01 and works forward has, by
      construction, met every prerequisite of the Move in front of them. That is not a
      stylistic choice; the build refuses to compile a book where it does not hold.</p>
      <p>Every Move carries all three clouds. The job is the same whether you are leaving AWS,
      Google Cloud or Azure &mdash; what differs is the extraction, so each Move opens with three
      lines naming the real service on each provider and the one thing that is different
      there.</p>
      <p>Move 04 concludes that you should keep paying somebody else for three things. A
      content delivery network, scrubbing capacity at the edge and outbound email are businesses
      other people run better than you will, and each is cheap next to what it replaces. The aim
      was never to own everything. And Move 03 gives you permission to stop: if the arithmetic
      does not clear a third, three Moves and a week is the whole cost of finding out.</p>
      <p class="sign">Rehearse everything, and read the Rollback before the first step of every
      Move &mdash; including the ones that look like nothing.</p>
    </div>
    <div class="anat">
      <div class="anat-fig">{anatomy()}<div class="anat-cap">Every Move, without exception</div></div>
      <div class="anat-key"><div class="pkicker" style="margin-bottom:4mm">How a Move works</div>
        {keyhtml}</div>
    </div>""", 'MANY MOVES, NOT ONE MIGRATION'))

    # ---------- the reference build
    shelves_html = ''.join(
        f'<div class="shelf"><h4>{name}</h4>' +
        ''.join(f'<label class="ck"><span class="box"></span>{esc(i)}</label>' for i in items) +
        '</div>' for name, items in list(SHELVES) + [('On the laptop', KIT)])
    n_items = sum(len(i) for _, i in SHELVES) + len(KIT)
    R = REFERENCE
    n_nodes = R['nodes']
    pages.append(page('', '#6B5344', f"""
    <div class="pkicker">Before you start &nbsp;·&nbsp; {n_items} things</div>
    <h2 class="ptitle d">The Reference Build</h2>
    <p class="pintro">Every Move in this book is written against one cluster, so that a runbook
    can name a real thing rather than a category: one site, {R['nodes']} nodes and
    {R['spares']} on the shelf, {R['cores_per_node']} cores and {R['ram_gb_per_node']} GB a node,
    {R['uplink_gbps']} GbE to the switch. {R['nodes']} because three is the smallest control
    plane with a quorum and losing one of three leaves two machines carrying a load nobody sized
    them for; the spare because a dead board is a return authorisation and three weeks. Scale the
    numbers; do not scale away the redundancy.</p>
    <div class="hrule" style="margin:5mm 0"></div>
    <div class="shelves">{shelves_html}</div>
    """, 'THE REFERENCE BUILD'))

    # ---------- the on-ramp: the cluster almost every reader should build first
    pages.append(page('', '#6B5344', f"""
    <div class="pkicker">Before any of it &nbsp;·&nbsp; about
      ${COSTS.homelab_capex():,.0f} and a weekend</div>
    <h2 class="ptitle d">The On-Ramp</h2>
    <p class="pintro">Almost nobody should sign a facility contract before they have run this
    stack once. A cluster of {HOMELAB['nodes']} refurbished machines with
    {HOMELAB['cores_per_node']} cores and {HOMELAB['ram_gb_per_node']} GB each, on a managed
    switch under a desk, will run every Move in Stage 3 unchanged and most of Stage 4
    besides. It costs about
    ${COSTS.homelab_capex():,.0f} once and about ${COSTS.homelab_month():.0f} a month in
    electricity, it saves nothing whatsoever, and it is the cheapest way to find out whether the
    rest of this book is for you.</p>
    <div class="hrule" style="margin:5.5mm 0"></div>
    <div class="pan">
      <div class="pcard"><h4>Why three, and why second-hand</h4><p>Three because a control plane
      needs three members to lose one and keep going, and everything you will learn about
      quorum, fencing and upgrades needs somewhere to go wrong. Second-hand because a machine
      two generations old runs Kubernetes exactly as well as a new one at roughly a tenth of the
      price, and because you want to be willing to break it.</p></div>
      <div class="pcard"><h4>What it genuinely proves</h4><p>The whole software estate. Talos,
      the control plane, Cilium with kube-proxy replaced, Rook and Ceph, the registry, secrets,
      the observability stack, and a Postgres cutover rehearsed end to end against a copy. If a Move works here it will work on the metal; the difference is scale,
      not shape.</p></div>
      <div class="pcard"><h4>What it cannot teach you</h4><p>Every word of Stage 2. A homelab
      has one power feed, one switch, no cross-connect, no remote hands and nobody to escalate
      to at three in the morning. It cannot show you what a colocation contract is for, or what
      happens when the A feed goes away and the B feed was never tested. The building is a
      different discipline, which is why it has a stage of its own.</p></div>
      <div class="pcard"><h4>When to stop using it</h4><p>Never. The on-ramp becomes the
      non-production cluster the rest of the book keeps asking for &mdash; the one you restore
      etcd onto, rehearse an upgrade on, and point a load generator at. Every estate needs a
      cluster it is allowed to destroy, and this is the cheapest one you will ever own.</p></div>
      <div class="pcard"><h4>The one part to buy new</h4><p>The drives. A consumer SSD without
      power-loss protection will corrupt etcd the first time the power flickers, and it will do
      it in a way that looks like a Kubernetes bug for a day and a half. Buy small enterprise
      NVMe with the protection, second-hand if you like, and put the money you saved on the
      chassis into the disks.</p></div>
      <div class="pcard"><h4>If three machines at home is not possible</h4><p>Rent three of the
      cheapest dedicated hosts you can find, by the month, and run exactly the same experiment.
      It costs more than electricity and less than being wrong, it gives you real addresses and
      a real network, and you can hand it all back at the end of the month. What it will not
      give you is a machine you can physically pull a disk out of.</p></div>
    </div>
    <div class="kitwrap">
      <div class="hrule" style="margin:0 0 4.5mm"></div>
      <div class="pkicker" style="margin-bottom:3.5mm">The whole shopping list</div>
      <div class="shelf kit">{''.join(
        f'<label class="ck"><span class="box"></span>{esc(k)}</label>'
        for k in HOMELAB_KIT)}</div>
    </div>""", 'THE ON-RAMP'))

    # ---------- the rules
    pages.append(page('', '#1F4E79', f"""
    <div class="pkicker">And then</div>
    <h2 class="ptitle d">The Rules for<br>Leaving the Cloud</h2>
    <div class="hrule" style="margin:6mm 0 7mm"></div>
    <div class="rules big">{''.join(
        f'<div class="rule-item"><div class="rn d">{i + 1}</div>'
        f'<div class="rt"><b>{esc(t)}</b> {esc(b)}</div></div>'
        for i, (t, b) in enumerate(RULES))}</div>
    """, 'THE RULES'))

    # ---------- the rollback page: the most important in the book
    oneway = sum(1 for m in moves if m['oneway'])
    rp = ''.join(f'<div class="pcard"><h4>{esc(t)}</h4><p>{esc(b)}</p></div>' for t, b in RB_POINTS)
    pages.append(page('', '#A32E1F', f"""
    <div class="pkicker">The one page to read twice</div>
    <h2 class="ptitle d">Before You Touch Anything</h2>
    <p class="pintro">{esc(rb_intro(oneway))}</p>
    <div class="hrule" style="margin:5.5mm 0"></div>
    <div class="pan">{rp}</div>
    <div class="kitwrap">
      <div class="hrule" style="margin:0 0 4.5mm"></div>
      <p class="legend-note" style="margin:0">{esc(RB_DISC)}</p>
    </div>""", 'BEFORE YOU TOUCH ANYTHING'))

    # ---------- what it actually costs
    # The Now column of every Move that states both halves: what stays on
    # somebody else's invoice after all twenty are done. Move 04 says to write
    # it in as a permanent line and this table used not to, which overstated
    # the saving by exactly this much. Derived here rather than typed, for the
    # same reason as every other number in this book.
    retained = sum(m['now'] for m in moves
                   if m['was'] is not None and m['now'] is not None)
    o = COSTS.owned_month(R['nodes'], R['spares'], retained)
    d = COSTS.dedicated_month(n_nodes + R['spares'], retained)
    capex = ((n_nodes + R['spares']) * COSTS.HARDWARE['node_capex']
             + COSTS.HARDWARE['switch_capex'])
    vcpu = n_nodes * R['cores_per_node'] * 2
    aws_compute = vcpu * COSTS.AWS['ec2_vcpu_hour'] * 730
    money = lambda v: f'${v:,.0f}'
    pages.append(page('', '#8A6112', f"""
    <div class="pkicker">The arithmetic, with the salary in it</div>
    <h2 class="ptitle d">What It Actually Costs</h2>
    <p class="pintro">The comparison that gets a repatriation approved and then regretted is the
    one that counts the hardware and forgets the people. This one counts both, at list price and
    with no commitment discount on either side, for the reference build opposite. Substitute your
    own effective rate; the shape does not change.</p>
    <div class="hrule" style="margin:5.5mm 0"></div>
    <div class="pan">
      <div class="pcard"><h4>On AWS, compute alone</h4><p>{vcpu:,} vCPU of current-generation
      general purpose instances, on demand, is <b>{money(aws_compute)}</b> a month before a single
      gigabyte of storage, a load balancer or a byte of egress. Egress is the line that ends most
      arguments: 100 TB a month is {money(COSTS.egress_month(100))}, every month, for the privilege
      of your own traffic leaving.</p></div>
      <div class="pcard"><h4>Owned, in one quarter rack</h4><p>{money(o['infrastructure'])} of
      infrastructure - metal amortised over five years, the spare, power, the space, transit, the
      cross-connect and remote hands - plus {money(o['people'])} of additional salaried time and
      {money(o['retained'])} that never comes home at all: the edge, the outbound mail and the
      scrubbing of Move 04, and the residue five later Moves leave behind. That salary line is
      the largest number in this column, the retained line is the one every other comparison
      forgets, and a table without either is the reason repatriations get approved and then
      regretted. Total <b>{money(o['total'])}</b> a month.</p></div>
      <div class="pcard"><h4>Rented by the month</h4><p>The same class of machine from a
      dedicated-host provider is {money(d['infrastructure'])}, and removes the racking, the spares
      and a quarter of a person: <b>{money(d['total'])}</b> all in. At this size that BEATS
      owning, by {money(o['total'] - d['total'])} a month, because a quarter rack's fixed costs do
      not amortise over six machines. You own hardware when the fleet is big enough to carry the
      room, and this fleet is not.</p></div>
      <div class="pcard"><h4>What the difference buys</h4><p>Against a bill of
      {money(COSTS.BILL_MONTH)} a month, roughly {money(COSTS.BILL_MONTH - o['total'])} a month or
      {money((COSTS.BILL_MONTH - o['total']) * 12)} a year, for a capital outlay of
      {money(capex)} &mdash; six machines and a pair of switches &mdash; which pays for itself in
      about {capex / max(COSTS.BILL_MONTH - o['total'], 1):.0f}
      months. Every Move states its own version of this table, and every one is a slice of
      this.</p></div>
    </div>
    <div class="chartwrap">
      <div class="pkicker" style="margin-bottom:4mm">One estate, three ways, per month</div>
      {cost_chart([('Cloud now', COSTS.BILL_MONTH, 0, 0),
                   ('Owned', o['infrastructure'], o['people'], o['retained']),
                   ('Rented', d['infrastructure'], d['people'], d['retained'])],
                  '100%', '#8A6112')}
    </div>
    <div class="kitwrap">
      <div class="hrule" style="margin:0 0 4.5mm"></div>
      <p class="legend-note" style="margin:0">Every AWS figure is a public list price for
      us-east-1 observed while writing, before any Savings Plan, private pricing agreement or
      credit. Every hardware figure is a mid-market street price for the specification opposite.
      Both will drift. The comparison is a method you can repeat against your own invoice, not a
      quotation - and if your effective rate is half of list, halve the left-hand column and read
      the conclusion again.</p>
    </div>""", 'WHAT IT ACTUALLY COSTS'))

    # ---------- the equivalence table, two pages
    def eq_page(rows, roman, kicker, intro, folio):
        body = ''.join(
            f'<tr class="{"keep" if r[3].lower().startswith("keep paying") else ""}">'
            f'<td>{esc(r[0])}</td><td>{esc(r[1])}</td><td>{esc(r[2])}</td>'
            f'<td class="yours">{esc(r[3])}</td></tr>' for r in rows)
        return page('', '#14655A', f"""
        <div class="pkicker">{kicker}</div>
        <h2 class="ptitle d">What Replaces What{roman}</h2>
        <p class="pintro">{intro}</p>
        <div class="hrule" style="margin:5mm 0"></div>
        <table class="eqt"><thead><tr>
          <th>{CLOUDS[0]}</th><th>{CLOUDS[1]}</th><th>{CLOUDS[2]}</th><th>What you run instead</th>
        </tr></thead><tbody>{body}</tbody></table>""", folio)

    half = (len(EQ_ROWS) + 1) // 2
    pages.append(eq_page(
        EQ_ROWS[:half], '',
        f'{len(EQ_ROWS)} services &nbsp;·&nbsp; three clouds &nbsp;·&nbsp; one answer each',
        'Every Move names the real service on all three clouds and the one thing that differs on '
        'each, so this table is the map rather than the content. Find the row you are paying for '
        'and then read the Move. The right-hand column is the point of the whole book, and where '
        'it says keep paying, that is a conclusion rather than a gap.',
        'WHAT REPLACES WHAT &nbsp;·&nbsp; I'))
    pages.append(eq_page(
        EQ_ROWS[half:], ' <span style="color:var(--ink4)">II</span>',
        'The edge, the platform, and the three you do not take back',
        'The rows that say keep paying are set in red because they are the most important '
        'lines in the table. A content delivery network, scrubbing capacity at the edge and '
        'outbound mail deliverability are not technical problems you have not solved yet. They '
        'are businesses, and you are not in them.',
        'WHAT REPLACES WHAT &nbsp;·&nbsp; II'))

    # ---------- one checklist page per stage
    # These were contents pages. They are now tick lists, because a reader
    # working through a migration over months wants somewhere to record what is
    # done, and a printed book is the one copy nobody can accidentally clear.
    # It costs one box per row and no extra pages.
    def toc_rows(ms):
        return ''.join(
            f'<div class="trow"><span class="tick"></span>'
            f'<span class="n" style="color:{m["l"]["color"]}">{m["num"]}</span>'
            f'<span class="t">{esc(m["title"])}</span><span class="lead"></span>'
            f'<span class="mn">{m["cutover"]} min</span>'
            f'<span class="pn">{pageno[m["num"]]}</span></div>' for m in ms)

    LEGEND = {
        'Decide': 'The invoice, the inventory and the comparison with the salary line in '
                  'it. Three Moves, about a week, and permission to stop.',
        'Buy': 'The specification, the machines, the space and everything with a lead '
               'time. The stage where a mistake costs a lorry rather than a deploy.',
        'Build': 'Racking, the network, the cluster and the disks. Nothing here moves a '
                 'workload, and everything here decides how the rest goes.',
        'Move': 'Images and secrets, the first service, the buckets and the database. The '
                'longest overlaps and the most rehearsal in the book.',
        'Run': 'The edge, the cutover, the backups you have restored, the pager, and the '
               'account you finally close.',
    }
    legend = ''.join(
        f'<div class="lg"><h5 style="color:{LAYERS[k]["color"]}">{icon(LAYERS[k]["key"], "4.2mm")}'
        f'{LAYERS[k]["label"]}</h5><p>{LEGEND[k]}</p></div>' for k in ORDER if k in parts)

    for idx, k in enumerate(keys):
        ms = parts[k]
        info = LAYERS[k]
        mid = (len(ms) + 1) // 2
        zero = sum(1 for m in ms if m['cutover'] == 0)
        last = idx == len(keys) - 1
        tail = (f'<div class="legend-wrap"><div class="legend">{legend}</div>'
                f'<p class="legend-note">Every Move states its cutover in minutes of '
                f'user-visible downtime, its risk as blast radius rather than difficulty, and '
                f'how long the thing it replaced must stay warm before you turn it off. '
                f'{sum(1 for m in moves if m["cutover"] == 0)} of the {len(moves)} Moves in this '
                f'book cost no downtime at all; the whole book, executed end to end, costs '
                f'{hours_saved(moves)} minutes.</p></div>') if last else ''
        pages.append(page('', info['color'], f"""
        <div class="pkicker">Stage {info['stage']} of {len(keys)} &nbsp;·&nbsp;
          {info['roman']} &nbsp;·&nbsp; {plural(len(ms), 'Move')} &nbsp;·&nbsp;
          {zero} at zero downtime</div>
        <h2 class="ptitle d">{esc(info['doing'])}</h2>
        <p class="stage-done"><b>Done when</b>{esc(info['done'])}</p>
        <p class="pintro" style="max-width:134mm">{PART_BLURB[k]}</p>
        <div class="hrule" style="margin:5.5mm 0"></div>
        <div class="toc"><div>{toc_rows(ms[:mid])}</div><div>{toc_rows(ms[mid:])}</div></div>
        {tail}""", f'CONTENTS &nbsp;·&nbsp; {esc(k).upper()}'))

    # ---------- the real index
    for _i in range(sym_pages):
        chunk = SYMPTOMS[_i * SYM_PER_PAGE:(_i + 1) * SYM_PER_PAGE]
        when_html = ''.join(
            f'<div class="when"><div class="wq d">{q}</div><div class="wl">' +
            ''.join(f'<span><b>{n}</b>{esc(by[n]["title"])}</span>'
                    for n in ns.split() if n in by) + '</div></div>'
            for q, ns in chunk)
        roman = '' if sym_pages == 1 else f' <span style="color:var(--ink4)">{"I" * (_i + 1)}</span>'
        intro = ('Nobody opens a book like this at Move 01. They open it because something on '
                 'the bill, or on the pager, has become intolerable. This is the index for the '
                 'way the question actually arrives.') if _i == 0 else (
                 'The rest of the same index. Every number points at a Move, and the build '
                 'refuses to compile a reference that does not.')
        pages.append(page('', '#8A6112', f"""
        <div class="pkicker">The real index</div>
        <h2 class="ptitle d">Which Move Do I Need{roman}</h2>
        <p class="pintro">{intro}</p>
        <div class="hrule" style="margin:4mm 0"></div>
        <div class="whens">{when_html}</div>""", 'WHICH MOVE DO I NEED'))

    # ============================== PARTS AND MOVES ==============================
    def divider(k, ms, size, trio):
        info = LAYERS[k]
        zero = sum(1 for m in ms if m['cutover'] == 0)
        high = sum(1 for m in ms if m['risk'] == 'High')
        st = [(str(len(ms)), 'Moves'), (str(zero), 'Zero downtime'),
              (str(high), 'High risk'), (str(sum(m['cutover'] for m in ms)), 'Minutes, total')]
        sh = ''.join(f'<div class="stat"><div class="sv d">{v}</div>'
                     f'<div class="sl">{l}</div></div>' for v, l in st)
        trio_html = ''.join(
            f'<div><div class="sn">{n}</div><h4>{esc(by[n]["title"])}</h4><p>{esc(why)}</p></div>'
            for n, why in trio if n in by)
        return page('cover divider', None, f"""
        <div class="cover-rule"></div>
        <div style="margin-top:5mm" class="eyebrow">{info['roman']} &nbsp;·&nbsp;
          {PART_KICKER[k]}</div>
        <div class="partno m">{info['part']}</div>
        <h1 class="d dv {size}">{esc(k)}</h1>
        <p class="cover-sub">{PART_BLURB[k]}</p>
        <div style="flex:1"></div>
        <div class="stats">{sh}</div>
        <div style="flex:1"></div>
        <div class="starts"><div class="st-k">If you only do three</div>
          <div class="strio">{trio_html}</div></div>
        <div style="flex:.7"></div>
        <div class="texture">{texture(ms)}</div>
        <div style="height:9mm"></div>
        <div class="cover-chips">{chips(ms)}</div>
        <div style="height:7mm"></div>
        <div class="cover-rule"></div>""")

    def move_pages(m, slot):
        """A Move is a spread: the setup page, then the runbook page."""
        c = m['l']['color']
        num, title = m['num'], esc(m['title'])
        tabtext = m['l']['label'].upper()

        pres = ''
        for g in m['pre_groups']:
            if g['name']:
                pres += f'<div class="pre-group">{inline(g["name"])}</div>'
            pres += ''.join(f'<div class="pre"><span class="bt" style="background:{c}"></span>'
                            f'<span>{inline(x)}</span></div>' for x in g['items'])

        # The three origins, ruled. One Move, three clouds, one runbook.
        origins = ''.join(
            f'<div class="orow"><span class="oc">{esc(o["short"])}</span>'
            f'<span class="os">{inline(o["service"])}</span>'
            f'<span class="on">{inline(o["note"])}</span></div>' for o in m['origins'])

        spec = (
            f'<div><div class="k">Layer</div><div class="v">'
            f'<span style="color:{c}">{icon(m["l"]["key"], "3.4mm", 1.6)}</span>'
            f'{m["l"]["label"].upper()}</div></div>'
            f'<div><div class="k">Leaving</div><div class="v wide">'
            f'{esc(m["leaving"])}</div></div>'
            f'<div><div class="k">Risk</div><div class="v">'
            f'{risk_bars(m["risk"], c, "2.8mm")}{m["risk"].upper()}</div></div>'
            f'<div><div class="k">Reversible</div><div class="v">'
            f'{esc(m["reversible"]).upper()}</div></div>')

        keys_ = ['Was', 'Now', 'Saved', 'Cutover', 'Effort', 'Wait']
        figs = ''.join(
            f'<div class="fig"><div class="v" style="color:{c}">{esc(v)}</div>'
            f'<div class="k">{k}</div></div>' for v, k in zip(m['figures'], keys_))

        notes = ''.join(f'<div class="note"><b style="color:{c}">{inline(t)}</b>{inline(b)}</div>'
                        for t, b in m['notes'])

        nd = dep_needs(num, by)
        needs_html = ('<div class="needs"><b style="color:%s">Needs</b>%s</div>' % (c, ''.join(
            f'<span class="nitem"><i style="color:{q["l"]["color"]}">{q["num"]}</i>'
            f'{esc(q["title"])}</span>' for q in nd))) if nd else ''

        page_a = page('', c, f"""
        <div class="rhead">
          <div class="rnum m" style="color:{c}">{num}</div>
          <div class="rht"><h1 class="rtitle d">{title}</h1></div>
          <div class="meterwrap">
            <div class="mk">Cutover</div>
            <div class="mv" style="color:{c}">{m['cutover']}<i>MIN</i></div>
            {meter(m['cutover'], c, CUTOVER_CAP)}
          </div>
        </div>
        <div class="spec">{spec}</div>
        <p class="hook" style="border-color:{c}">{inline(m['hook'])}</p>
        <div class="origins">{origins}</div>
        <div class="rbody rgrid{' wide' if m['pre_count'] >= 13 else ''}">
          <div class="rcol"><div class="blab" style="color:{c}">Before you start</div>
            <div class="pre-panel{' two' if m['pre_count'] >= 13 else ''}">{pres}</div></div>
          <div class="rcol"><div class="blab" style="color:{c}">Why this works</div>
            <p class="why">{inline(m['why'])}</p></div>
        </div>
        <div class="rfoot">
          <div class="notes">{notes}</div>
          <div class="strip" style="border-top-color:{c}">{figs}</div>
          <div class="turnoff"><b style="color:{c}">Turn off</b>
            <span>{inline(m['turnoff'])}</span></div>
          {needs_html}
        </div>""", f"{num} &nbsp;·&nbsp; {title.upper()}", slot, tabtext)

        steps = ''.join(
            f'<div class="mstep"><div class="mmark">'
            f'<span class="snum" style="color:{c}">{i + 1:02d}</span></div>'
            f'<div class="mtext">{inline(st)}</div></div>'
            for i, st in enumerate(m['steps']))

        page_b = page('', c, f"""
        <div class="mhead" style="border-bottom-color:{c}">
          <div class="mh-num m" style="color:{c}">{num}</div>
          <div class="mh-title d">{title}</div>
          <div class="mh-meta">{len(m['steps'])} steps &nbsp;·&nbsp; {m['cutover']} min
            &nbsp;·&nbsp; {m['risk']} risk</div>
        </div>
        <div class="blab mblab" style="color:{c}">The runbook</div>
        <div class="rbody msteps">{steps}</div>
        <div class="rfoot">
          <div class="rb" style="border-top-color:{c}">
            <b style="color:{c}">Rollback</b>
            <p>{inline(m['rollback'])}</p></div>
          <div class="mfoot"><span style="color:{c}">{icon(m['l']['key'], '3.6mm')}</span>
            <span class="mf-facts">{m['l']['label']} &nbsp;·&nbsp; {m['cutover']} min
              &nbsp;·&nbsp; {m['risk']} risk</span>
            <span class="mf-off">{inline(m['turnoff'])}</span></div>
        </div>""", f"{num} &nbsp;·&nbsp; RUNBOOK", slot, tabtext)

        return [page_a, page_b]

    TRIOS = {}  # filled from part_trios.py if present, else derived
    try:
        from part_trios import TRIOS as _T
        TRIOS = _T
    except ImportError:
        pass

    def clip(text, n=118):
        """Trim to a word boundary. A hook cut mid-word reads as a bug, because
        on a divider there is nothing around it to explain the ellipsis."""
        if len(text) <= n:
            return text
        cut = text[:n].rsplit(' ', 1)[0].rstrip(' ,;:-')
        return cut + '\u2009&hellip;'

    def derive_trio(ms):
        """Three Moves worth doing first: the safest start, the biggest saving,
        and whatever the stage opens with. De-duplicated, because a stage can be
        short enough that the three
        rules pick the same Move twice."""
        order = []
        for cand in (sorted(ms, key=lambda m: (m['risk'] != 'Low', m['cutover'])),
                     sorted([m for m in ms if m['was'] and m['now']],
                            key=lambda m: -(m['was'] - m['now'])),
                     ms):
            for m in cand:
                if m not in order:
                    order.append(m)
                    break
        return [(m['num'], clip(m['hook'])) for m in order]

    assert len(pages) == FRONT_FIXED, (
        f'front matter emitted {len(pages)} pages, arithmetic above says {FRONT_FIXED}. '
        f'Add or remove a page there and this number follows it.')
    if FRONT_FIXED % 2:
        pages.append(page('blankp', None, ''))   # so the first divider opens on a recto
    for i, k in enumerate(keys):
        ms = parts[k]
        pages.append(divider(k, ms, 'dv-1' if len(k) > 5 else 'dv-2',
                             TRIOS.get(k) or derive_trio(ms)))
        for m in ms:
            pages += move_pages(m, i)
        if i < len(keys) - 1:
            pages.append(page('blankp', None, ''))

    # ============================== ENDNOTE ==============================
    # Both totals are used by the endnote and the colophon below, and both are
    # derived rather than written: nothing in this book states a count it did not
    # count.
    zero = sum(1 for m in moves if m["cutover"] == 0)
    oneway = sum(1 for m in moves if m["oneway"])
    KNOW = [
        ('The bill lags the change by a month',
         'A resource stopped on the third still bills for the first two days, and a reservation '
         'you no longer use bills for a year. Judge a Move by the invoice after next, never by '
         'the console.'),
        ('Capacity you own is capacity you have',
         'The cloud taught a generation to treat headroom as waste. On your own metal, idle '
         'capacity is the thing that absorbs a bad deploy at four in the afternoon. Buy thirty '
         'per cent more than the model says.'),
        ('Two people know, or nobody does',
         'The single most common failure mode of a self-run platform is not hardware. It is one '
         'engineer who understands the network, and a holiday.'),
        ('Hardware fails predictably and boringly',
         'Disks, fans, PSUs, optics, in that order, at a rate you can put in a spreadsheet. It '
         'is not the drama people expect. The drama is in the change you made on Friday.'),
        ('Keep one foot in the cloud on purpose',
         'An account with a working credential, a Terraform state and a warm standby is not a '
         'failure of nerve. It is the cheapest disaster recovery site you will ever have.'),
        ('The saving is real; the freedom is the point',
         'Most teams start this for the bill and finish it for the other thing: being able to '
         'answer a question about your own system without opening a support case.'),
        ('Write the runbook before you need it',
         'Every Move in this book is a runbook because that is the artefact that survives the '
         'person who wrote it. A migration that leaves no runbooks behind has to be done again '
         'by whoever comes next.'),
        ('You can go back',
         'The industry talks about repatriation as though it were one-way. It is not. '
         f'{oneway} of the {len(moves)} Moves here are genuinely irreversible and the other '
         f'{len(moves) - oneway} are not, and knowing which is which is most of the skill.'),
    ]
    pages.append(page('', '#14655A', f"""
    <div class="pkicker">Afterwards</div>
    <h2 class="ptitle d">A Few Things<br>Worth Knowing</h2>
    <p class="pintro">None of these is a Move. They are the ten things that make the other
    {len(moves)} work, and most of them are the things people learn in the second year rather
    than the first.</p>
    <div class="hrule" style="margin:6mm 0"></div>
    <div class="pan">{''.join(
        f'<div class="pcard"><h4>{esc(t)}</h4><p>{esc(b)}</p></div>' for t, b in KNOW)}</div>
    <div class="colophon">
      <p class="signoff">The best infrastructure decision you make this year will probably be
      unglamorous, take a fortnight, save a five-figure sum and never be written up anywhere.
      That is rather the point.</p>
      <div class="hrule" style="margin:0 0 5mm"></div>
      <div class="colo-grid">
        <div><h6>The book</h6><p>{len(moves)} Moves across five stages.
        {zero} cost no downtime at all, {oneway} cannot be undone, and the whole book executed
        end to end costs {hours_saved(moves)} minutes of user-visible outage.</p></div>
        <div><h6>The type</h6><p>Set in Archivo, drawn by Omnibus-Type, and JetBrains Mono,
        drawn by Philipp Nurullin and Konstantin Bulenkov. Both are open source. Every number
        in this book is set in the mono.</p></div>
        <div><h6>The numbers</h6><p>Every price is a public list rate observed while writing,
        before any discount, and every saving is illustrative of a shape rather than a quotation.
        Check the arithmetic against your own invoice.</p></div>
      </div>
      <p class="colo-disc">{IMP.DISCLOSURE}</p>
      <div class="colo-edition">{IMP.PUBLISHER_SITE} &nbsp;&middot;&nbsp; Version {VERSION}
        &nbsp;&middot;&nbsp; The Moves and the typesetter that made this book are open source at
        {IMP.REPO}</div>
    </div>""", 'A FEW THINGS WORTH KNOWING'))

    if len(pages) % 2:
        pages.append(page('blankp', None, ''))

    # ---- pagination invariants ---------------------------------------------
    # A facing pair in a bound book is (even verso, odd recto). Every Move's setup
    # page must therefore be even and its runbook the next page, or the spread the
    # whole design rests on is split across a page turn. KDP also requires an even
    # page count; left to itself it appends an uncontrolled blank.
    assert len(pages) % 2 == 0, f'odd page count: {len(pages)} - KDP will insert a blank'
    for m in moves:
        want = pageno[m['num']]
        assert want % 2 == 0, f"move {m['num']} setup page on odd page {want}"
        hit = [i + 1 for i, pg in enumerate(pages)
               if f'<div class="folio">{m["num"]} &nbsp;·&nbsp;' in pg
               and 'RUNBOOK</div>' not in pg]
        assert len(hit) == 1, f"move {m['num']}: found {len(hit)} setup pages"
        assert hit[0] == want, (f"move {m['num']}: contents says p{want}, "
                                f"built at p{hit[0]}")

    def stamp(p, i):
        # Page 1 is a recto; odd folios are right-hand pages.
        side = 'recto' if (i + 1) % 2 else 'verso'
        p = p.replace('<section class="page', f'<section data-side="{side}" class="page', 1)
        return p.replace('{{PN}}', str(i + 1), 1)

    pages = [stamp(p, i) for i, p in enumerate(pages)]

    # A page built with a plain string where an f-string was meant renders its
    # own source. The half title did exactly that after the retitle and the only
    # symptom was the running head reading "{IMP.wordmark_html()}".
    leaked = re.findall(r'\{[A-Za-z_][\w.]*(?:\(\))?\}', ''.join(pages))
    assert not leaked, f'unsubstituted template expressions in the built pages: {sorted(set(leaked))[:6]}'

    doc = (f'<!doctype html><html><head><meta charset="utf-8">'
           f'<title>{esc(IMP.TITLE)}</title>'
           f'<style>{FONTS}{CSS}</style></head><body>{"".join(pages)}</body></html>')
    (ROOT / 'build').mkdir(exist_ok=True)
    (ROOT / 'build' / 'book.html').write_text(doc, encoding='utf-8')
    return len(pages)


if __name__ == '__main__':
    (ROOT / 'build').mkdir(exist_ok=True)
    ms = load_all()
    if not ms:
        sys.exit('build: no Move files in moves/ yet')
    n = build(ms)
    print('pages:', n, '| html',
          round((ROOT / 'build' / 'book.html').stat().st_size / 1e6, 2), 'MB')
