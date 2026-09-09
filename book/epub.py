"""Build the Kindle edition: a reflowable EPUB3, generated from moves/*.md.

Reflowable rather than fixed-layout, because most Kindle reading happens on a
phone and because this is a book somebody will have open next to a terminal. An
8.25x11 page scaled to a six-inch screen puts the body text well under the cap
height KDP requires of fixed layout, and fixed layout also gives up user font
settings and screen-reader support.

So the print design does not survive, and is not faked: the full-bleed bars, the
two-page spread and the vertical justification are print production, not content.
What carries over is the structure - the meta, why it works, the prerequisites,
the runbook, the rollback, the numbers - as semantic XHTML the reader restyles.

The Rollback section is deliberately placed BEFORE the runbook in this edition.
On paper it sits at the foot of the facing page, where the eye reaches it while
reading; in a linear reflowed document it would otherwise arrive after the reader
has already run the steps.

Built from parse.py, never from build/book.html, which is print geometry.
"""
import html, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from parse import load_all, LAYERS, ORDER, inline
from deps import DEPS
from kit import SHELVES, KIT, RULES, PLATFORM_SCOPE, COST_SCOPE, REFERENCE
from rollback_data import intro as rb_intro, POINTS as RB_POINTS, DISCLAIMER as RB_DISC
from equivalents import ROWS as EQ_ROWS, CLOUDS
from version import VERSION
import imprint as IMP
import mission as MISSION
import costs as COSTS
import roadmap as RM
import why as WHY
import worksheets as WS

OUT = ROOT / 'dist' / IMP.EPUB_NAME

XHTML = ('<?xml version="1.0" encoding="utf-8"?>\n'
         '<!DOCTYPE html>\n'
         '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
         'lang="en" xml:lang="en">\n<head><meta charset="utf-8"/><title>{title}</title>'
         '<link rel="stylesheet" type="text/css" href="{up}style.css"/></head>\n'
         '<body>\n{body}\n</body>\n</html>\n')


def esc(s):
    # Resolve any named entity to its character before escaping: XHTML served as
    # XML defines only &amp; &lt; &gt; &quot; &apos;
    return html.escape(html.unescape(str(s)), quote=False)


def rich(s):
    """inline() escapes &, < and > itself and emits only <strong>/<em>/<code>, so
    it must not be handed pre-escaped text. XML has no named entities beyond the
    big five, so anything arriving as one is resolved to its character first."""
    return inline(html.unescape(str(s))).replace('<br>', '<br/>')


CSS = """/* Reflowable: never set an absolute body size, and set the family on body only.
   Kindle's defaults differ from a browser's, so headings state their alignment. */
body { font-family: sans-serif; font-size: 1em; line-height: 1.5; margin: 0 5%; }
h1, h2, h3 { font-family: sans-serif; text-align: left; page-break-after: avoid; }
h1 { font-size: 1.5em; line-height: 1.25; margin: 1em 0 0.2em; }
h2 { font-size: 1.1em; margin: 1.6em 0 0.4em; text-transform: uppercase;
     letter-spacing: 0.08em; }
h3 { font-size: 1em; margin: 1.2em 0 0.3em; }
p { margin: 0 0 0.8em; text-indent: 0; }
code { font-family: monospace; font-size: 0.92em; }
.meta { font-family: sans-serif; font-size: 0.85em; margin: 0 0 1em; }
.hook { font-style: italic; margin: 0 0 1.2em; }
ul, ol { margin: 0 0 1em 1.2em; padding: 0; }
li { margin: 0 0 0.45em; }
.group { font-family: sans-serif; font-size: 0.85em; text-transform: uppercase;
         letter-spacing: 0.08em; margin: 0.9em 0 0.3em; }
.rollback { border-top: 2px solid #999; border-bottom: 2px solid #999;
            padding: 0.8em 0; margin: 1.4em 0; }
.numbers { font-family: sans-serif; font-size: 0.85em; }
.turnoff { font-size: 0.9em; font-style: italic; }
.note b { font-family: sans-serif; }
nav ol { list-style: none; margin-left: 0; }
.front { margin-top: 2em; }
.small { font-size: 0.82em; }
table { border-collapse: collapse; width: 100%; font-size: 0.8em; }
th, td { text-align: left; padding: 0.25em 0.5em 0.25em 0; vertical-align: top;
         border-bottom: 1px solid #ccc; }
"""


def worksheets_xhtml(moves):
    def source(ref):
        return (f'<p class="small"><a href="m/{ref["move"]}.xhtml">'
                f'{esc(ref["source"])}</a></p>')
    body = f'<h1>{esc(WS.HEADING)}</h1><p>{esc(WS.INTRO)}</p>'
    for sheet in WS.records(moves):
        body += (f'<section id="{sheet["id"]}"><h2>{esc(sheet["title"])}</h2>'
                 f'<p>{rich(sheet["purpose"]["text"])}</p>'
                 + source(sheet['purpose']) + '<ul>'
                 + ''.join(f'<li>{esc(label)}:</li>' for label in WS.RECORD_FIELDS)
                 + '</ul>'
                 + ''.join(f'<h3>{esc(field["label"])}</h3><p>{rich(field["text"])}</p>'
                           + source(field) for field in sheet['fields'])
                 + '</section>')
    return XHTML.format(title=esc(WS.HEADING), up='', body=body)


def mission_xhtml(count):
    # This shared prose uses <b> for emphasis in print and web. Translate that
    # explicit convention before the Markdown renderer escapes literal HTML.
    paragraphs = [rich(p.replace('<b>', '**').replace('</b>', '**'))
                  for p in MISSION.paras(IMP.REPO, count)]
    return XHTML.format(
        title=esc(MISSION.KICKER), up='',
        body=(f'<div class="front"><h1>{esc(" ".join(MISSION.HEADING_LINES))}</h1>'
              + ''.join(f'<p>{p}</p>' for p in paragraphs) + '</div>'))


def move_xhtml(m):
    origins = '<ul>\n' + ''.join(
        f'<li><strong>{esc(o["cloud"])}:</strong> {rich(o["service"])} '
        f'&#8212; {rich(o["note"])}</li>\n' for o in m['origins']) + '</ul>\n'
    pres = ''
    for g in m['pre_groups']:
        if g['name']:
            pres += f'<p class="group">{esc(g["name"])}</p>\n'
        pres += '<ul>\n' + ''.join(f'<li>{rich(x)}</li>\n' for x in g['items']) + '</ul>\n'
    steps = '<ol>\n' + ''.join(f'<li>{rich(s)}</li>\n' for s in m['steps']) + '</ol>\n'
    notes = ''.join(f'<p class="note"><b>{esc(t)}:</b> {rich(b)}</p>\n' for t, b in m['notes'])
    was, now, saved, cut, eff, wait = m['figures']
    deps = DEPS.get(m['num'], [])
    deplinks = ', '.join(f'<a href="{d}.xhtml">Move {d}</a>' for d in deps)
    depline = f'<p class="small">Needs first: {deplinks}.</p>\n' if deps else ''
    body = f"""<h1>{esc(m['num'])} &#183; {esc(m['title'])}</h1>
<p class="meta">{esc(m['layer'])} &#183; leaving {esc(m['leaving'])} &#183;
 {esc(m['risk'])} risk &#183; {esc(m['cutover'])} min cutover &#183;
 reversible: {esc(m['reversible'])}</p>
<p class="hook">{rich(m['hook'])}</p>
{depline}<h2>Leaving from</h2>
{origins}<h2>Why this works</h2>
<p>{rich(m['why'])}</p>
<div class="rollback">
<h3>Rollback &#8212; read this first</h3>
<p>{rich(m['rollback'])}</p>
<p class="small"><a href="../rollback.xhtml">Before you touch anything</a></p>
</div>
<h2>Before you start</h2>
{pres}<h2>The runbook</h2>
{steps}<h2>Operator&#8217;s notes</h2>
{notes}<h2>The numbers</h2>
<p class="numbers">Was {esc(was)} &#183; now {esc(now)} &#183; saved {esc(saved)}
 &#183; cutover {esc(cut)} &#183; effort {esc(eff)} &#183; wait {esc(wait)}</p>
<p class="turnoff">What you can turn off: {rich(m['turnoff'])}</p>"""
    return XHTML.format(title=esc(m['title']), up='../', body=body)


def financials(moves):
    """Use the same rounded components as print and web, then sum the parts."""
    retained = sum(m['now'] for m in moves
                   if m['was'] is not None and m['now'] is not None)
    cloud_people = round(COSTS.cloud_people_month())
    bill = COSTS.BILL_MONTH
    cloud_total = bill + cloud_people
    rows = [{'key': 'cloud', 'label': 'Cloud', 'infrastructure': bill,
             'people': cloud_people, 'retained': 0, 'total': cloud_total}]
    for key, label, parts in (
        ('owned', 'Colocation', COSTS.owned_month(
            REFERENCE['nodes'], REFERENCE['spares'], retained)),
        ('rented', 'Rented metal', COSTS.dedicated_month(
            REFERENCE['nodes'] + REFERENCE['spares'], retained)),
    ):
        infra, delta, kept = (round(parts[k]) for k in
                              ('infrastructure', 'people', 'retained'))
        people = cloud_people + delta
        rows.append({'key': key, 'label': label, 'infrastructure': infra,
                     'people': people, 'retained': kept,
                     'total': infra + people + kept})
    for row in rows:
        row['saved'] = cloud_total - row['total']
    return {'retained': retained, 'rows': rows,
            'five_year': COSTS.five_year(REFERENCE['nodes'], REFERENCE['spares'], retained),
            'days': sum(RM.effort_days(m) for m in moves),
            'weeks': RM.schedule(moves, 2)['weeks']}


def money(value):
    return f'${value:,.0f}'


def decision_xhtml(facts):
    owned = next(r for r in facts['five_year']['rows'] if r['key'] == 'owned')
    fmt = {'five_year_saved': money(owned['saved']),
           'five_year_pct': f'{owned["pct"]:.0f}',
           'egress_100tb': money(COSTS.egress_month(100)),
           'weeks': f'{facts["weeks"]:.0f}', 'days': f'{facts["days"]:.0f}',
           'cloud_hours': COSTS.PEOPLE['cloud_ops_hours_month'],
           'retained': money(facts['retained'])}
    body = (f'<h1>{esc(WHY.HEADING)}</h1><p>{esc(WHY.lede(fmt))}</p>'
            f'<h2>{esc(WHY.OURS_HEADING)}</h2>'
            + ''.join(f'<h3>{esc(h)}</h3><p>{esc(b)}</p>' for h, b in WHY.OURS)
            + f'<p>{esc(WHY.OURS_NOTE)}</p>'
            + ''.join(f'<h2>{esc(h)}</h2><p>{esc(b)}</p><p>{esc(test)}</p>'
                      for h, b, test in WHY.gains(fmt))
            + f'<h2>{esc(WHY.COSTS_HEADING)}</h2><p>{esc(WHY.COSTS_LEDE)}</p>'
            + ''.join(f'<h3>{esc(h)}</h3><p>{esc(b)}</p>' for h, b in WHY.costs(fmt))
            + f'<h2>{esc(WHY.STAY_HEADING)}</h2><ul>'
            + ''.join(f'<li>{esc(p)}</li>' for p in WHY.STAY)
            + f'</ul><p>{esc(WHY.CLOSER)}</p>'
            + '<p><a href="costs.xhtml">Read the financial comparison</a>.</p>')
    return XHTML.format(title=esc(WHY.HEADING), up='', body=body)


def costs_xhtml(facts):
    # Two-column tables remain readable on narrow e-readers. Stable IDs let the
    # cross-output agreement gate check the displayed financial values.
    body = ('<h1>What it costs</h1>'
            f'<p>{esc(COST_SCOPE)}</p>'
            '<p>These are worked assumptions, not quotations. Replace cloud list '
            'rates with your effective invoices, and hardware, facility, support '
            'and rental allowances with matching current quotes. The model keeps '
            'the same operations hours and loaded pay in every option; validate '
            'those hours with your team.</p><h2>Monthly comparison</h2>'
            '<p>The colocation infrastructure line includes amortised capital. '
            'Retained third-party charges come from the Moves and are already '
            'inside the cloud bill.</p>')
    for row in facts['rows']:
        values = [('Infrastructure', 'infrastructure'), ('People', 'people'),
                  ('Retained third-party charges', 'retained'),
                  ('Total a month', 'total'), ('Saved a month', 'saved')]
        body += f'<h3>{esc(row["label"])}</h3><table><tbody>'
        for label, key in values:
            value = ('Already in the bill' if row['key'] == 'cloud' and key == 'retained'
                     else money(row[key]))
            body += (f'<tr><th scope="row">{esc(label)}</th>'
                     f'<td id="monthly-{row["key"]}-{key}">{esc(value)}</td></tr>')
        body += '</tbody></table>'
    fy = facts['five_year']
    body += (f'<h2>The full {fy["months"]}-month cash comparison</h2>'
             '<p>Here capital appears once at purchase, so monthly running cost '
             'excludes amortisation. The residual is an assumed credit at the '
             'end, not guaranteed resale proceeds. These steady-state figures '
             'exclude migration labour, overlap, financing and taxes.</p>')
    for row in fy['rows']:
        body += f'<h3>{esc(row["label"])}</h3><table><tbody>'
        for label, key in [('Capital at purchase', 'capex'), ('Running a month', 'month'),
                           ('Residual credit', 'residual'), ('Total over the period', 'total'),
                           ('Saved against cloud', 'saved')]:
            body += (f'<tr><th scope="row">{esc(label)}</th>'
                     f'<td id="cash-{row["key"]}-{key}">{money(row[key])}</td></tr>')
        body += '</tbody></table>'
    body += (f'<p>The reference plan estimates {facts["days"]:.0f} person-days '
             f'across {facts["weeks"]:.0f} weeks with two engineers. Calendar waits '
             'extend that schedule without consuming engineer-days. Price migration '
             'labour and the overlapping estates separately in '
             '<a href="m/03.xhtml">Move 03</a>.</p>')
    return XHTML.format(title='What it costs', up='', body=body)


def build():
    moves = load_all()
    if not moves:
        sys.exit('epub: no Move files in moves/ yet')

    cover_jpg = ROOT / 'dist' / 'cover-kindle.jpg'
    if not cover_jpg.exists():
        sys.exit('epub: build the covers first (make covers)')

    files = {}

    # ---- front matter -------------------------------------------------------
    # KDP creates the internal cover from the designated cover-image. An extra
    # HTML image page can produce duplicate covers or fail conversion.
    # https://kdp.amazon.com/en_US/help/topic/G6GTK3T3NUHKLEFX

    files['OEBPS/titlepage.xhtml'] = XHTML.format(
        title=esc(IMP.TITLE), up='',
        body=(f'<div class="front"><h1>{esc(IMP.TITLE)}</h1>'
              f'<p>{esc(IMP.SUBTITLE)}</p><p>{esc(IMP.AUTHOR)}</p>'
              f'<p class="small">{esc(IMP.BYLINE)} &#183; {esc(IMP.ONEUPTIME_SITE)}</p>'
              f'<p class="small">{esc(IMP.PUBLISHER)} &#183; {esc(IMP.PUBLISHER_SITE)}</p>'
              f'<p class="small">{esc(IMP.SITE)}</p></div>')).encode()

    files['OEBPS/copyright.xhtml'] = XHTML.format(
        title='Copyright', up='',
        body=('<div class="front small">'
              f'<p>Copyright &#169; {IMP.YEAR} {esc(IMP.AUTHOR)}</p>'
              f'<p>Published by {esc(IMP.PUBLISHER)}, {esc(IMP.PUBLISHER_SITE)}</p>'
              f'<p>{esc(IMP.LICENCE)}</p><p>{esc(IMP.MORAL_RIGHTS)}</p>'
              f'<p>{esc(IMP.EDITION)}, {IMP.YEAR}. Version {VERSION}.</p>'
              + ''.join(f'<p>ISBN ({k}): {esc(v)}</p>' for k, v in IMP.ISBN.items() if v)
              + f'<p>{esc(IMP.DISCLAIMER)}</p><p>{esc(IMP.DISCLOSURE)}</p>'
              + f'<p>{esc(IMP.SITE)}</p></div>')).encode()

    files['OEBPS/why.xhtml'] = mission_xhtml(len(moves)).encode()

    facts = financials(moves)
    files['OEBPS/decision.xhtml'] = decision_xhtml(facts).encode()
    files['OEBPS/costs.xhtml'] = costs_xhtml(facts).encode()

    # The safety page goes early and is linked from every Move's rollback note.
    oneway = sum(1 for m in moves if m['oneway'])
    files['OEBPS/rollback.xhtml'] = XHTML.format(
        title='Before you touch anything', up='',
        body=('<h1>Before you touch anything</h1>'
              f'<p>{esc(rb_intro(oneway))}</p>'
              + ''.join(f'<h3>{esc(t)}</h3><p>{esc(b)}</p>' for t, b in RB_POINTS)
              + f'<p class="small">{esc(RB_DISC)}</p>')).encode()

    files['OEBPS/kit.xhtml'] = XHTML.format(
        title='The reference build', up='',
        body=('<h1>The reference build</h1>'
              + f'<p>{esc(PLATFORM_SCOPE)}</p>'
              + ''.join(f'<h3>{esc(n)}</h3><ul>'
                        + ''.join(f'<li>{esc(i)}</li>' for i in items) + '</ul>'
                        for n, items in SHELVES)
              + f'<h2>{len(RULES)} rules for leaving the cloud</h2><ol id="rules">'
              + ''.join(f'<li><b>{esc(t)}</b> {esc(b)}</li>' for t, b in RULES)
              + '</ol><h2>On the laptop</h2><p>'
              + ', '.join(esc(k) for k in KIT) + '.</p>')).encode()

    eqrows = ''.join(
        f'<tr><td>{esc(r[0])}</td><td>{esc(r[1])}</td><td>{esc(r[2])}</td>'
        f'<td>{esc(r[3])}</td><td>'
        + (f'<a href="m/{r[4]}.xhtml">Move {esc(r[4])}</a>' if r[4] else '&#8212;')
        + '</td></tr>' for r in EQ_ROWS)
    files['OEBPS/replaces.xhtml'] = XHTML.format(
        title='What replaces what', up='',
        body=('<h1>What replaces what</h1>'
              '<p>Every Move names the real service on all three clouds and the one thing that '
              'differs on each, so this table is the map rather than the content. Find the row '
              'you are paying for and then read the Move.</p>'
              f'<table><tr><th>{CLOUDS[0]}</th><th>{CLOUDS[1]}</th><th>{CLOUDS[2]}</th>'
              f'<th>What you run instead</th><th>Move</th></tr>{eqrows}</table>')).encode()

    for m in moves:
        files[f"OEBPS/m/{m['num']}.xhtml"] = move_xhtml(m).encode()
    files['OEBPS/worksheets.xhtml'] = worksheets_xhtml(moves).encode()
    files['OEBPS/img/cover.jpg'] = cover_jpg.read_bytes()
    files['OEBPS/style.css'] = CSS.encode()

    # ---- navigation ---------------------------------------------------------
    # Two levels at most: stage, then Move. Deeper nesting is the single most
    # common reason a Kindle table of contents renders badly.
    nav_items = ''
    for k in ORDER:
        rs = [m for m in moves if m['layer'] == k]
        if not rs:
            continue
        kids = ''.join(f'<li><a href="m/{m["num"]}.xhtml">{esc(m["num"])} &#183; '
                       f'{esc(m["title"])}</a></li>\n' for m in rs)
        nav_items += (f'<li><a href="m/{rs[0]["num"]}.xhtml">{LAYERS[k]["roman"]} &#183; '
                      f'{esc(k)}</a>\n<ol>\n{kids}</ol>\n</li>\n')
    FRONT = [('titlepage.xhtml', 'Title page'), ('why.xhtml', MISSION.KICKER),
             ('decision.xhtml', WHY.HEADING), ('costs.xhtml', 'What it costs'),
             ('rollback.xhtml', 'Before you touch anything'),
             ('kit.xhtml', 'The reference build'),
             ('replaces.xhtml', 'What replaces what')]
    worksheet_nav = (
        f'<li><a href="worksheets.xhtml">{esc(WS.HEADING)}</a><ol>'
        + ''.join(f'<li><a href="worksheets.xhtml#{s["id"]}">{esc(s["title"])}</a></li>'
                  for s in WS.TEMPLATES) + '</ol></li>\n')
    nav_body = ('<nav epub:type="toc" id="toc"><h1>Contents</h1>\n<ol>\n'
                + ''.join(f'<li><a href="{h}">{esc(t)}</a></li>\n' for h, t in FRONT)
                + nav_items + worksheet_nav + '</ol>\n</nav>'
                '<nav epub:type="landmarks" hidden="hidden"><h2>Navigation</h2><ol>'
                '<li><a epub:type="toc" href="nav.xhtml#toc">Contents</a></li>'
                '</ol></nav>')
    files['OEBPS/nav.xhtml'] = XHTML.format(title='Contents', up='', body=nav_body).encode()

    ncx_entries = FRONT + [(f'm/{m["num"]}.xhtml', f'{m["num"]} - {m["title"]}')
                           for m in moves]
    ncx_entries += [(f'worksheets.xhtml#{s["id"]}', s['title']) for s in WS.TEMPLATES]
    ncx_points = ''.join(
        f'<navPoint id="n{i}" playOrder="{i}"><navLabel><text>{esc(title)}</text></navLabel>'
        f'<content src="{href}"/></navPoint>\n'
        for i, (href, title) in enumerate(ncx_entries, 1))
    # Stable for the life of the work, and deliberately not derived from VERSION:
    # see EPUB_ID in imprint.py.
    uid = IMP.EPUB_ID
    files['OEBPS/toc.ncx'] = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n'
        f'<head><meta name="dtb:uid" content="{uid}"/></head>\n'
        f'<docTitle><text>{esc(IMP.TITLE)}</text></docTitle>\n'
        f'<navMap>\n{ncx_points}</navMap>\n</ncx>\n').encode()

    # ---- package ------------------------------------------------------------
    manifest = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '<item id="css" href="style.css" media-type="text/css"/>',
        '<item id="cover-img" href="img/cover.jpg" media-type="image/jpeg" '
        'properties="cover-image"/>',
    ]
    spine = []
    for i, (h, _) in enumerate(FRONT):
        fid = f'f{i}'
        manifest.append(f'<item id="{fid}" href="{h}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{fid}"/>')
    manifest.append('<item id="copy" href="copyright.xhtml" '
                    'media-type="application/xhtml+xml"/>')
    spine.insert(1, '<itemref idref="copy"/>')
    spine.insert(2, '<itemref idref="nav"/>')
    for m in moves:
        manifest.append(f'<item id="m{m["num"]}" href="m/{m["num"]}.xhtml" '
                        f'media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="m{m["num"]}"/>')
    manifest.append('<item id="worksheets" href="worksheets.xhtml" '
                    'media-type="application/xhtml+xml"/>')
    spine.append('<itemref idref="worksheets"/>')

    modified = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    files['OEBPS/content.opf'] = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
        'unique-identifier="pub-id">\n'
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        f'<dc:identifier id="pub-id">{uid}</dc:identifier>\n'
        f'<dc:title>{esc(IMP.TITLE)}</dc:title>\n'
        f'<dc:creator>{esc(IMP.AUTHOR)}</dc:creator>\n'
        f'<dc:publisher>{esc(IMP.PUBLISHER)}</dc:publisher>\n'
        '<dc:language>en</dc:language>\n'
        f'<dc:description>{esc(IMP.SUBTITLE)}</dc:description>\n'
        f'<meta property="dcterms:modified">{modified}</meta>\n'
        '</metadata>\n'
        f'<manifest>\n{chr(10).join(manifest)}\n</manifest>\n'
        f'<spine toc="ncx">\n{chr(10).join(spine)}\n</spine>\n'
        '</package>\n').encode()

    files['META-INF/container.xml'] = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
        '<rootfiles><rootfile full-path="OEBPS/content.opf" '
        'media-type="application/oebps-package+xml"/></rootfiles>\n</container>\n').encode()

    OUT.parent.mkdir(exist_ok=True)
    # Written to one side and moved into place, so a crash mid-build leaves the
    # previous archive intact rather than a truncated one that still opens.
    tmp = OUT.with_name(OUT.name + '.tmp')
    with zipfile.ZipFile(tmp, 'w') as z:
        z.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip',
                   compress_type=zipfile.ZIP_STORED)
        for name in sorted(files):
            z.writestr(name, files[name], compress_type=zipfile.ZIP_DEFLATED)
    tmp.replace(OUT)

    mb = OUT.stat().st_size / 1e6
    print(f'epub: {len(moves)} moves, {len(files) + 1} files -> {OUT.name} ({mb:.2f} MB)')
    print(f'      KDP delivery fee at ${IMP.KDP_DELIVERY_PER_MB}/MB on the converted size: '
          f'about ${mb * IMP.KDP_DELIVERY_PER_MB:.2f} a sale under the 70% option')


if __name__ == '__main__':
    build()
