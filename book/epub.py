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
from kit import SHELVES, KIT, RULES
from rollback_data import intro as rb_intro, POINTS as RB_POINTS, DISCLAIMER as RB_DISC
from equivalents import ROWS as EQ_ROWS, CLOUDS
from version import VERSION
import imprint as IMP
import mission as MISSION

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
body { font-family: serif; font-size: 1em; line-height: 1.5; margin: 0 5%; }
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


def move_xhtml(m):
    pres = ''
    for g in m['pre_groups']:
        if g['name']:
            pres += f'<p class="group">{esc(g["name"])}</p>\n'
        pres += '<ul>\n' + ''.join(f'<li>{rich(x)}</li>\n' for x in g['items']) + '</ul>\n'
    steps = '<ol>\n' + ''.join(f'<li>{rich(s)}</li>\n' for s in m['steps']) + '</ol>\n'
    notes = ''.join(f'<p class="note"><b>{esc(t)}:</b> {rich(b)}</p>\n' for t, b in m['notes'])
    was, now, saved, cut, eff, wait = m['figures']
    deps = DEPS.get(m['num'], [])
    depline = (f'<p class="small">Needs first: '
               f'{", ".join("Move " + d for d in deps)}.</p>\n') if deps else ''
    body = f"""<h1>{esc(m['num'])} &#183; {esc(m['title'])}</h1>
<p class="meta">{esc(m['layer'])} &#183; leaving {esc(m['leaving'])} &#183;
 {esc(m['risk'])} risk &#183; {esc(m['cutover'])} min cutover &#183;
 back out for {esc(m['reversible'])}</p>
<p class="hook">{rich(m['hook'])}</p>
{depline}<h2>Why this works</h2>
<p>{rich(m['why'])}</p>
<div class="rollback">
<h3>Rollback &#8212; read this first</h3>
<p>{rich(m['rollback'])}</p>
</div>
<h2>Before you start</h2>
{pres}<h2>The runbook</h2>
{steps}<h2>Operator&#8217;s notes</h2>
{notes}<h2>The numbers</h2>
<p class="numbers">Was {esc(was)} &#183; now {esc(now)} &#183; saved {esc(saved)}
 &#183; cutover {esc(cut)} &#183; effort {esc(eff)} &#183; wait {esc(wait)}</p>
<p class="turnoff">What you can turn off: {rich(m['turnoff'])}</p>"""
    return XHTML.format(title=esc(m['title']), up='../', body=body)


def build():
    moves = load_all()
    if not moves:
        sys.exit('epub: no Move files in moves/ yet')

    cover_jpg = ROOT / 'dist' / 'cover-kindle.jpg'
    if not cover_jpg.exists():
        sys.exit('epub: build the covers first (make covers)')

    files = {}

    # ---- front matter -------------------------------------------------------
    files['OEBPS/cover.xhtml'] = XHTML.format(
        title='Cover', up='',
        body=f'<div style="text-align:center"><img src="img/cover.jpg" '
             f'style="max-width:100%" alt="{esc(IMP.TITLE)}"/></div>').encode()

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

    files['OEBPS/why.xhtml'] = XHTML.format(
        title=esc(MISSION.KICKER), up='',
        body=(f'<div class="front"><h1>{esc(" ".join(MISSION.HEADING_LINES))}</h1>'
              + ''.join(f'<p>{rich(p)}</p>' for p in MISSION.paras(IMP.REPO, len(moves)))
              + '</div>')).encode()

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
              + ''.join(f'<h3>{esc(n)}</h3><ul>'
                        + ''.join(f'<li>{esc(i)}</li>' for i in items) + '</ul>'
                        for n, items in SHELVES)
              + '<h2>Ten rules for leaving the cloud</h2><ol>'
              + ''.join(f'<li><b>{esc(t)}</b> {esc(b)}</li>' for t, b in RULES)
              + '</ol><h2>On the laptop</h2><p>'
              + ', '.join(esc(k) for k in KIT) + '.</p>')).encode()

    eqrows = ''.join(
        f'<tr><td>{esc(r[0])}</td><td>{esc(r[1])}</td><td>{esc(r[2])}</td>'
        f'<td>{esc(r[3])}</td></tr>' for r in EQ_ROWS)
    files['OEBPS/replaces.xhtml'] = XHTML.format(
        title='What replaces what', up='',
        body=('<h1>What replaces what</h1>'
              '<p>Every Move names the real service on all three clouds and the one thing that '
              'differs on each, so this table is the map rather than the content. Find the row '
              'you are paying for and then read the Move.</p>'
              f'<table><tr><th>{CLOUDS[0]}</th><th>{CLOUDS[1]}</th><th>{CLOUDS[2]}</th>'
              f'<th>What you run instead</th></tr>{eqrows}</table>')).encode()

    for m in moves:
        files[f"OEBPS/m/{m['num']}.xhtml"] = move_xhtml(m).encode()
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
             ('rollback.xhtml', 'Before you touch anything'),
             ('kit.xhtml', 'The reference build'),
             ('replaces.xhtml', 'What replaces what')]
    nav_body = ('<nav epub:type="toc" id="toc"><h1>Contents</h1>\n<ol>\n'
                + ''.join(f'<li><a href="{h}">{esc(t)}</a></li>\n' for h, t in FRONT)
                + nav_items + '</ol>\n</nav>')
    files['OEBPS/nav.xhtml'] = XHTML.format(title='Contents', up='', body=nav_body).encode()

    ncx_points = ''.join(
        f'<navPoint id="n{i}" playOrder="{i}"><navLabel><text>{esc(m["num"])} - '
        f'{esc(m["title"])}</text></navLabel>'
        f'<content src="m/{m["num"]}.xhtml"/></navPoint>\n'
        for i, m in enumerate(moves, 1))
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
        '<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>',
    ]
    spine = ['<itemref idref="cover"/>']
    for i, (h, _) in enumerate(FRONT):
        fid = f'f{i}'
        manifest.append(f'<item id="{fid}" href="{h}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{fid}"/>')
    manifest.append('<item id="copy" href="copyright.xhtml" '
                    'media-type="application/xhtml+xml"/>')
    spine.insert(1, '<itemref idref="copy"/>')
    spine.append('<itemref idref="nav"/>')
    for m in moves:
        manifest.append(f'<item id="m{m["num"]}" href="m/{m["num"]}.xhtml" '
                        f'media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="m{m["num"]}"/>')

    modified = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    files['OEBPS/content.opf'] = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
        'unique-identifier="pub-id">\n'
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        f'<dc:identifier id="pub-id">{uid}</dc:identifier>\n'
        f'<dc:title>{esc(IMP.TITLE)}</dc:title>\n'
        f'<dc:creator>{esc(IMP.AUTHOR)}</dc:creator>\n'
        '<dc:language>en</dc:language>\n'
        f'<dc:description>{esc(IMP.SUBTITLE)}</dc:description>\n'
        f'<dc:date>{IMP.YEAR}-01-01</dc:date>\n'
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
