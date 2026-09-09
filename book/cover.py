"""Build the covers.

Three artefacts, sharing only the artwork:

  paperback  a single full-wrap PDF - back cover, spine, front cover, with bleed
             on all four sides. Rendered as vector through the same Chromium
             pipeline as the interior, so the type stays crisp.
  kindle     a front-cover raster, 1600x2560, RGB JPEG.
  hardback   the case, IF its dimensions have been measured. KDP publishes no
             hardcover formula and defers to its own Cover Calculator; the case
             is materially larger than the paperback wrap in both axes, because
             the sheet wraps a board that overhangs the text block, plus two
             hinge channels. Any formula short of the calculator's template is
             guesswork, so this prints the numbers to feed it rather than
             inventing a size.

The spine comes from the real page count in the built interior, not a constant,
because it changes whenever the book does - and from the interior KDP prints it
on, because standard and premium colour are different thicknesses of paper.
"""
import asyncio, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from parse import load_all
import build as B
import imprint as IMP
from flatten import mix
from printcheck import check_print

BLEED = 0.125          # inches, all four sides on a cover
TRIM_W, TRIM_H = 8.25, 11.0
SAFE = 0.25            # inches: keep all type this far inside the trim
SPINE_TEXT_MIN_PAGES = 80  # KDP prints spine text only above 79 pages.
SPINE_TEXT_MARGIN = 0.0625
SPINE_TEXT_MIN_PT = 7

# Inches of spine per page. KDP publishes one multiplier per interior stock:
#
#   "Standard Color paper: page count x 0.002252" (0.0572 mm)"
#   "Premium Color paper: page count x 0.002347" (0.0596 mm)"
#
# - Create a Paperback Cover, https://kdp.amazon.com/en_US/help/topic/G201953020.
# KDP's older Paperback Submission Guidelines page still lumps every colour book
# together as "Color paper: page count x 0.002347""; that row predates the
# standard/premium split and is wrong for a standard-colour interior.
SPINE_PER_PAGE = {
    'standard colour': 0.002252,
    'premium colour':  0.002347,
}

# The hardcover case. UNSET until it has been measured, because KDP publishes no
# formula and the numbers are only correct at one page count. Once the interior's
# page count is settled, open KDP's Cover Calculator, enter 8.25x11 at that page
# count in premium colour on white paper, and fill these in:
#
#   sheet_w/sheet_h  the full printed sheet
#   panel_w/panel_h  one cover panel
#   spine            the spine width (far wider than the paperback's)
#   wrap             the turn-in - nothing here survives on the visible face
#   hinge            the channel either side of the spine, where type creases
#
# Check the arithmetic before trusting it: 2*panel_w + spine + 2*wrap should
# equal sheet_w, and panel_h + 2*wrap should equal sheet_h.
HC = None

PDF = ROOT / 'dist' / IMP.PDF_NAME
INK = '#14171C'

SAFE_AREA_JS = '''() => {
  const IN = 96, sheet = document.querySelector('.sheet');
  const s = sheet.getBoundingClientRect(), out = [];
  sheet.querySelectorAll('*').forEach(e => {
    const range = document.createRange();
    range.selectNodeContents(e);
    const r = range.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) return;
    if (e.children.length) return;            // measure leaves, not wrappers
    if (!e.textContent.trim()) return;        // ignore spacers and rules
    out.push({cls: String(e.className).slice(0, 26),
              l: (r.left - s.left) / IN, t: (r.top - s.top) / IN,
              r: (s.right - r.right) / IN, b: (s.bottom - r.bottom) / IN});
  });
  return out;
}'''


def spine_text(pages, width, preferred_pt=12):
    """Keep text off short/narrow spines, including the binding tolerance.

    KDP's cover guidance requires more than 79 pages and 0.0625in clear on
    either side. The minimum cover type size is 7pt. Reserve a full line box,
    rather than sizing from the nominal type height alone.
    https://kdp.amazon.com/en_US/help/topic/G201857950 (2026-09-09)
    https://kdp.amazon.com/en_US/help/topic/G201113520 (2026-09-09)
    """
    size = min(preferred_pt, (width - 2 * SPINE_TEXT_MARGIN) * 72 / 1.2)
    if pages < SPINE_TEXT_MIN_PAGES or size < SPINE_TEXT_MIN_PT:
        return ''
    author_size = max(SPINE_TEXT_MIN_PT, size * 0.78)
    return (f'<div class="spine-txt" style="font-size:{size:.3f}pt;line-height:1.2">'
            f'<span class="t d">{IMP.TITLE}</span>'
            f'<span class="a" style="font-size:{author_size:.3f}pt">{IMP.AUTHOR}</span></div>')


def page_count():
    if not PDF.exists():
        sys.exit('cover: build the interior first (make book)')
    return len(re.findall(rb'/Type\s*/Page[^s]', PDF.read_bytes()))


def geometry(pages):
    """The paperback wrap. Its spine depends on the interior KDP will print it on."""
    if IMP.INK_CHOICE not in SPINE_PER_PAGE:
        sys.exit(f'cover: no KDP spine multiplier for a {IMP.INK_CHOICE!r} interior')
    spine = pages * SPINE_PER_PAGE[IMP.INK_CHOICE]
    return {'pages': pages, 'spine': spine,
            'width': 2 * BLEED + 2 * TRIM_W + spine,
            'height': 2 * BLEED + TRIM_H}


def back_panel_html(moves):
    """The back-cover copy. Shared by the paperback wrap and the hardback case."""
    zero = sum(1 for m in moves if m['cutover'] == 0)
    import roadmap as RM
    effort = sum(RM.effort_days(m) for m in moves)
    return f"""
    <div class="inner">
      <p class="bk-k">For a company &nbsp;&middot;&nbsp; AWS, Google Cloud and Azure out</p>
      <h2 class="bk-h d">Leaving is a method,<br><em>not a decision.</em></h2>
      <p class="bk-p">The reason leaving the cloud fails is rarely the technology. It is that it
      is attempted as one decision, executed as one project, and abandoned in the middle with two
      platforms running and nobody able to say whether it is going well.</p>
      <p class="bk-p">This book is {len(moves)} Moves. Each is one job with a stated cutover, a
      stated risk and a rollback with explicit limits. Rehearse the return path before moving
      traffic or data; purchases and account deletion have their own points of no return.
      One of them tells you to keep paying somebody else, and another gives you permission
      to read three Moves, do the arithmetic and stop.</p>
      <p class="bk-p">Every Move covers all three clouds: it names the real service on AWS,
      Google Cloud and Azure, and the one thing that is different on each.</p>
      <div class="bk-rule"></div>
      <div class="bk-list">
        <div><b>{len(moves)}</b> Moves</div><div><b>{len({m['layer'] for m in moves})}</b> Stages</div>
        <div><b>{zero}</b> plan zero downtime</div><div><b>{effort:.0f}</b> person-days estimated</div>
        <div><b>3</b> clouds, every Move</div><div><b>1</b> closes the account</div>
      </div>
      <p class="bk-os"><b>The whole book is open source.</b> Every Move, and the software that
      typesets them into this book, is published under an open licence at {IMP.REPO}. Correct it,
      extend it, add the services your own estate runs. Infrastructure knowledge this practical
      should not sit behind a consulting invoice.</p>
      <p class="bk-by">{IMP.BYLINE} &nbsp;&middot;&nbsp; {IMP.ONEUPTIME_SITE}</p>
      <div class="bk-foot"><span>{IMP.SITE}</span><span>{IMP.PUBLISHER_SITE}</span></div>
    </div>
    <div class="barcode"></div>"""


def panel_css(mid, faint, blurb_rule):
    return f"""
    .bk-k{{font-size:8.2pt;letter-spacing:.24em;text-transform:uppercase;
      font-weight:600;color:#8FB4D6}}
    .bk-h{{font-size:26pt;line-height:1.14;font-weight:500;letter-spacing:-.02em;margin-top:5mm}}
    .bk-h em{{font-style:italic;color:#8FB4D6}}
    .bk-p{{font-size:11pt;line-height:1.62;color:{mid};margin-top:6mm;max-width:104mm}}
    .bk-rule{{height:1px;background:{blurb_rule};margin:8mm 0}}
    .bk-list{{display:grid;grid-template-columns:1fr 1fr;gap:2.6mm 8mm;font-size:9.6pt;
      color:{mid}}}
    .bk-list b{{color:#8FB4D6;font-weight:600}}
    .bk-os{{margin-top:9mm;padding-top:6mm;border-top:1px solid {blurb_rule};
      font-size:9.4pt;line-height:1.6;color:{mid};max-width:104mm}}
    .bk-os b{{color:#8FB4D6;font-weight:600}}
    .bk-by{{margin-top:auto;padding-top:8mm;font-family:'JetBrains Mono',monospace;
      font-size:8.4pt;letter-spacing:.18em;text-transform:uppercase;color:#8FB4D6}}
    .bk-foot{{margin-top:5mm;display:flex;flex-direction:column;gap:1.5mm;align-items:flex-start;
      padding-right:2.2in;
      font-size:8pt;letter-spacing:.14em;text-transform:uppercase;color:{faint}}}
    .spine-txt{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(90deg);
      transform-origin:center;white-space:nowrap;display:flex;align-items:baseline;gap:7mm;
      font-size:12pt;letter-spacing:.06em}}
    .spine-txt .t{{font-variation-settings:'wdth' 84;font-weight:750;
      text-transform:uppercase}}
    .spine-txt .a{{font-size:9.4pt;color:{mid};letter-spacing:.16em;text-transform:uppercase}}
    """


def wrap_html(moves, g):
    front = B.cover_front_html(moves)
    blurb_rule = mix('#FBFAF7', INK, .28)
    faint = mix('#FBFAF7', INK, .55)
    mid = mix('#FBFAF7', INK, .74)
    css = f"""
    @page{{size:{g['width']}in {g['height']}in;margin:0}}
    *{{margin:0;padding:0;box-sizing:border-box}}
    html,body{{background:{INK}}}
    .sheet{{position:relative;width:{g['width']}in;height:{g['height']}in;
      background:{INK};color:#FBFAF7;overflow:hidden}}
    .panel{{position:absolute;top:0;height:{g['height']}in}}
    .back {{left:0;width:{BLEED + TRIM_W}in}}
    .spine{{left:{BLEED + TRIM_W}in;width:{g['spine']}in}}
    .front{{left:{BLEED + TRIM_W + g['spine']}in;width:{TRIM_W + BLEED}in}}
    .front .inner{{position:absolute;inset:0;
      padding:{BLEED + 0.55}in {BLEED + 0.62}in {BLEED + 0.5}in 0.62in;
      display:flex;flex-direction:column}}
    .back .inner{{position:absolute;inset:0;
      padding:{BLEED + 0.72}in 0.62in {BLEED + 0.5}in {BLEED + 0.62}in;
      display:flex;flex-direction:column}}
    /* KDP prints the barcode over the lower right of the back cover: keep it clear */
    .barcode{{position:absolute;right:{BLEED + SAFE}in;bottom:{BLEED + SAFE}in;
      width:2in;height:1.2in}}
    """ + panel_css(mid, faint, blurb_rule)
    spine_txt = spine_text(g['pages'], g['spine'])
    return (f'<!doctype html><html><head><meta charset="utf-8">'
            f'<style>{B.FONTS}{B.CSS}{css}</style></head><body>'
            f'<div class="sheet">'
            f'<div class="panel back cover">{back_panel_html(moves)}</div>'
            f'<div class="panel spine">{spine_txt}</div>'
            f'<div class="panel front cover"><div class="inner">{front}</div></div>'
            f'</div></body></html>')


def hardback_html(moves, h):
    """The hardback case: one sheet wrapping board, hinges and all.

    Panels left to right for a left-to-right book: turn-in, back cover, spine,
    front cover, turn-in. Nothing in the turn-in survives on the visible face, and
    type in a hinge channel gets creased, so both are dead space.
    """
    front = B.cover_front_html(moves)
    blurb_rule = mix('#FBFAF7', INK, .28)
    faint = mix('#FBFAF7', INK, .55)
    mid = mix('#FBFAF7', INK, .74)
    spine_x = h['wrap'] + h['panel_w']
    front_x = spine_x + h['spine']
    outer_pad = h['wrap'] + 0.5          # clear of the turn-in
    vert_pad = h['wrap'] + 0.55
    hinge_pad = h['hinge'] + 0.25        # clear of the hinge channel
    css = f"""
    @page{{size:{h['sheet_w']}in {h['sheet_h']}in;margin:0}}
    *{{margin:0;padding:0;box-sizing:border-box}}
    html,body{{background:{INK}}}
    .sheet{{position:relative;width:{h['sheet_w']}in;height:{h['sheet_h']}in;
      background:{INK};color:#FBFAF7;overflow:hidden}}
    .panel{{position:absolute;top:0;height:{h['sheet_h']}in}}
    .back {{left:0;width:{spine_x}in}}
    .spine{{left:{spine_x}in;width:{h['spine']}in}}
    .front{{left:{front_x}in;width:{h['sheet_w'] - front_x}in}}
    .front .inner{{position:absolute;inset:0;
      padding:{vert_pad + 0.05}in {outer_pad}in {vert_pad}in {hinge_pad}in;
      display:flex;flex-direction:column}}
    .back .inner{{position:absolute;inset:0;
      padding:{vert_pad + 0.2}in {hinge_pad}in {vert_pad}in {outer_pad}in;
      display:flex;flex-direction:column}}
    .barcode{{position:absolute;right:{outer_pad}in;bottom:{vert_pad}in;width:2in;height:1.2in}}
    """ + panel_css(mid, faint, blurb_rule)
    spine_txt = spine_text(h['pages'], h['spine'], preferred_pt=15)
    return (f'<!doctype html><html><head><meta charset="utf-8">'
            f'<style>{B.FONTS}{B.CSS}{css}</style></head><body>'
            f'<div class="sheet">'
            f'<div class="panel back cover">{back_panel_html(moves)}</div>'
            f'<div class="panel spine">{spine_txt}</div>'
            f'<div class="panel front cover"><div class="inner">{front}</div></div>'
            f'</div></body></html>')


async def render(html_str, out_pdf, g, safe=None, label='cover'):
    """Render a cover sheet to PDF.

    `safe['edges']` is (left, top, right, bottom) in inches: the margin every
    piece of type must stay inside. On the hardback that is the turn-in, which is
    glued down out of sight; on the paperback it is the bleed plus KDP's 0.25in
    rule. `safe['keepout']` is a list of (x0, x1) bands from the left of the sheet
    - the hardback's hinge channels, where type would be creased.

    Measured from the live layout rather than the finished PDF, so it needs no
    rasteriser and fails before a bad cover is ever written.
    """
    from playwright.async_api import async_playwright
    src = ROOT / 'build' / (label + '.html')
    src.parent.mkdir(exist_ok=True)
    src.write_text(html_str, encoding='utf-8')
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--font-render-hinting=none'])
        pg = await b.new_page(viewport={'width': 1600, 'height': 1100})
        await pg.goto(src.as_uri(), wait_until='networkidle')
        await pg.evaluate('document.fonts.ready')
        await pg.wait_for_timeout(1200)
        await check_print(pg, label)
        if safe:
            els = await pg.evaluate(SAFE_AREA_JS)
            L, T, R, Bm = safe['edges']
            viol = [(e, 'outside the safe margin') for e in els
                    if e['l'] < L - 0.01 or e['t'] < T - 0.01
                    or e['r'] < R - 0.01 or e['b'] < Bm - 0.01]
            for x0, x1 in safe.get('keepout', []):
                for e in els:
                    left, right = e['l'], g['width'] - e['r']
                    if left < x1 - 0.01 and right > x0 + 0.01:
                        viol.append((e, f'in the hinge channel {x0:.3f}-{x1:.3f}in'))
            barcode = await pg.locator('.barcode').bounding_box()
            if barcode:
                x0, y0 = barcode['x'] / 96, barcode['y'] / 96
                x1, y1 = x0 + barcode['width'] / 96, y0 + barcode['height'] / 96
                for e in els:
                    right, bottom = g['width'] - e['r'], g['height'] - e['b']
                    if e['l'] < x1 and right > x0 and e['t'] < y1 and bottom > y0:
                        viol.append((e, 'in the reserved ISBN barcode area'))
            if viol:
                print(f'  {label}: TYPE OUTSIDE THE SAFE AREA, {len(viol)} element(s):')
                for e, why in viol[:6]:
                    print(f"    .{e['cls']:<26} l {e['l']:.3f} t {e['t']:.3f} "
                          f"r {e['r']:.3f} b {e['b']:.3f} in - {why}")
                await b.close()
                raise SystemExit(1)
        await pg.pdf(path=str(out_pdf), print_background=True,
                     margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
                     prefer_css_page_size=True)
        await b.close()


async def render_kindle(moves, out_jpg):
    """Front cover only: 1600x2560, RGB, no bleed, no spine."""
    from playwright.async_api import async_playwright
    front = B.cover_front_html(moves)
    html_str = (
        f'<!doctype html><html><head><meta charset="utf-8"><style>{B.FONTS}{B.CSS}'
        f'*{{margin:0;padding:0;box-sizing:border-box}}'
        f'html,body{{background:{INK}}}'
        f'.kc{{width:1600px;height:2560px;position:relative;background:{INK};color:#FBFAF7}}'
        f'.kc .inner{{position:absolute;inset:0;padding:120px 104px 104px;'
        f'display:flex;flex-direction:column}}'
        # A store cover is read as a thumbnail, so the twelve-Move list that works
        # on a printed jacket becomes unreadable noise. Drop it and let the title,
        # the promise and the numbers carry the whole cover.
        f'.kc .menu-k,.kc .menu{{display:none}}'
        f'.kc h1{{font-size:160pt;margin-top:0}}'
        f'.kc .cover-sub{{font-size:29pt;max-width:none;margin-top:52px}}'
        f'.kc .cover-author{{font-size:30pt;margin-top:30px}}'
        f'.kc .promise p{{font-size:33pt;line-height:1.6}}'
        f'.kc .stats{{margin-top:20px}}'
        f'.kc .stat{{padding:40px 24px 34px}}'
        f'.kc .stat .sv{{font-size:58pt}}.kc .stat .sl{{font-size:14pt}}'
        f'.kc .cover-foot{{font-size:17pt}}'
        f'.kc .cover-rule{{height:2px}}'
        f'</style></head><body>'
        f'<div class="kc cover"><div class="inner">{front}</div></div></body></html>')
    src = ROOT / 'build' / 'cover-kindle.html'
    src.parent.mkdir(exist_ok=True)
    src.write_text(html_str, encoding='utf-8')
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--font-render-hinting=none'])
        pg = await b.new_page(viewport={'width': 1600, 'height': 2560})
        await pg.goto(src.as_uri(), wait_until='networkidle')
        await pg.evaluate('document.fonts.ready')
        await pg.wait_for_timeout(1200)
        await pg.locator('.kc').screenshot(path=str(out_jpg), type='jpeg', quality=92)
        await b.close()


def hardback_instructions(pages):
    print()
    print('cover: the hardback case has NOT been generated, because KDP publishes no')
    print('       formula for it and this build refuses to guess a jacket size.')
    print()
    print("       Open KDP's Cover Calculator and enter:")
    print(f'         trim         8.25 x 11 in')
    print(f'         page count   {pages}')
    print(f'         binding      hardcover, case laminate')
    print(f'         ink/paper    premium colour, white')
    print('       then fill HC at the top of book/cover.py with the sheet, panel, spine,')
    print('       turn-in and hinge it returns, and run make covers again. Check that')
    print('       2*panel_w + spine + 2*wrap == sheet_w before trusting it.')


def main():
    require_hb = '--require-hardback' in sys.argv
    moves = load_all()
    if not moves:
        sys.exit('cover: no Move files in moves/ yet')
    g = geometry(page_count())
    (ROOT / 'build').mkdir(exist_ok=True)
    (ROOT / 'dist').mkdir(exist_ok=True)

    pb = ROOT / 'dist' / 'cover-paperback.pdf'
    asyncio.run(render(wrap_html(moves, g), pb, g,
                       safe={'edges': (BLEED + SAFE,) * 4}, label='cover-paperback'))

    kc = ROOT / 'dist' / 'cover-kindle.jpg'
    asyncio.run(render_kindle(moves, kc))

    print(f"cover: {g['pages']} pages -> spine {g['spine']:.4f}in ({g['spine'] * 25.4:.2f}mm)")
    print(f"       paperback wrap {g['width']:.4f} x {g['height']:.4f}in -> {pb.name} "
          f"({pb.stat().st_size / 1e6:.2f} MB)")
    print(f"       kindle front 1600x2560 -> {kc.name} ({kc.stat().st_size / 1e6:.2f} MB)")

    if HC is None:
        hardback_instructions(g['pages'])
        if require_hb:
            sys.exit(1)
        return
    if g['pages'] != HC['pages']:
        sys.exit(f"cover: the hardback case was measured at {HC['pages']} pages but the book "
                 f"is now {g['pages']}. Re-measure it in KDP's Cover Calculator and update HC.")
    hb = ROOT / 'dist' / 'cover-hardback.pdf'
    spine_l = HC['wrap'] + HC['panel_w']
    spine_r = spine_l + HC['spine']
    asyncio.run(render(hardback_html(moves, HC), hb,
                       {'width': HC['sheet_w'], 'height': HC['sheet_h']},
                       safe={'edges': (HC['wrap'],) * 4,
                             'keepout': [(spine_l - HC['hinge'], spine_l),
                                         (spine_r, spine_r + HC['hinge'])]},
                       label='cover-hardback'))
    print(f"       hardback case {HC['sheet_w']} x {HC['sheet_h']}in, spine {HC['spine']}in "
          f"-> {hb.name} ({hb.stat().st_size / 1e6:.2f} MB)")


if __name__ == '__main__':
    main()
