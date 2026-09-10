"""build/book.html -> dist/Leaving-the-Cloud.pdf, vertically justified.

Every Move occupies exactly two pages, and Moves vary a lot in length. Before
printing, this runs a justification pass in the browser: for each page it
binary-searches one parameter that expands or tightens a set of levers - leading
between steps and prerequisites, panel padding, and on the densest pages the body
size itself - until the content sits a consistent 4.5 mm above the footer block.

It then refuses to write a PDF whose type falls outside KDP's safe area, because
a cover that looks fine on screen and wrong in the hand is the expensive kind of
mistake.
"""
import asyncio, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from playwright.async_api import async_playwright
import imprint as IMP
from printcheck import check_print, check_text_margins

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist' / IMP.PDF_NAME

JUSTIFY = """() => {
  const MM = 96 / 25.4, TARGET = 4.5 * MM;
  // Each lever: b = the value the stylesheet actually sets, hi = how far it may
  // expand, lo = how far it may tighten. `b` MUST match style.css: the first
  // apply() writes every lever at once, so a baseline that disagrees makes the
  // page jump before the search has done anything. Ordered least visible first.
  const SETUP = [
    {s:'.rhead',    prop:'marginBottom',  b:0,    hi:9,   lo:0},
    {s:'.orow',     prop:'paddingTop',    b:1.9,  hi:1.4, lo:0.9},
    {s:'.orow',     prop:'paddingBottom', b:1.9,  hi:1.4, lo:0.9},
    {s:'.origins',  prop:'marginTop',     b:5.5,  hi:4,   lo:2.6},
    {s:'.spec>div', prop:'paddingTop',    b:2.2,  hi:1.4, lo:1.3},
    {s:'.spec>div', prop:'paddingBottom', b:2.2,  hi:1.4, lo:1.3},
    {s:'.pre',      prop:'fontSize',      b:8.1,  hi:1.2, lo:7.5, u:'pt'},
    {s:'.why',      prop:'fontSize',      b:8.7,  hi:1.4, lo:8.0, u:'pt'},
    {s:'.orow .on', prop:'fontSize',      b:7.7,  hi:0.7, lo:7.0, u:'pt'},
    {s:'.pre',      prop:'marginBottom',  b:1.7,  hi:2.2, lo:0.7},
    {s:'.why',      prop:'marginBottom',  b:6,    hi:8,   lo:2.8},
    {s:'.rbody',    prop:'marginTop',     b:6,    hi:7,   lo:2.8},
    {s:'.hook',     prop:'marginTop',     b:5.5,  hi:5,   lo:2.8},
    {s:'.spec',     prop:'marginTop',     b:4,    hi:3,   lo:2.2},
    {s:'.blab',     prop:'marginBottom',  b:2.8,  hi:2.6, lo:1.3},
    {s:'.pre-group:not(:first-child)', prop:'marginTop', b:3, hi:2.2, lo:1.4},
    {s:'.rfoot',    prop:'paddingTop',    b:6,    hi:7,   lo:3.0},
    {s:'.notes',    prop:'paddingTop',    b:3.4,  hi:4,   lo:2.0},
    {s:'.turnoff',  prop:'marginTop',     b:3,    hi:2,   lo:1.8},
    {s:'.needs',    prop:'marginTop',     b:2.4,  hi:1.8, lo:1.4},
    {s:'.strip',    prop:'marginTop',     b:5,    hi:3,   lo:2.6},
    {s:'.note',     prop:'fontSize',      b:7.5,  hi:1.0, lo:7.0, u:'pt'}
  ];
  const RUNBOOK = [
    {s:'.mstep',    prop:'marginBottom',  b:6,    hi:26,  lo:1.6},
    {s:'.mmark',    prop:'paddingTop',    b:0.6,  hi:2.5, lo:0.2},
    {s:'.mtext',    prop:'fontSize',      b:9.8,  hi:2.4, lo:8.6, u:'pt'},
    {s:'.snum',     prop:'fontSize',      b:10.5, hi:2,   lo:9,   u:'pt'},
    {s:'.mhead',    prop:'paddingBottom', b:3,    hi:7,   lo:2.0},
    {s:'.mblab',    prop:'marginTop',     b:6,    hi:13,  lo:2.4},
    {s:'.blab',     prop:'marginBottom',  b:2.8,  hi:2.6, lo:1.3},
    {s:'.rb',       prop:'paddingTop',    b:3.4,  hi:3,   lo:2.4},
    {s:'.rb',       prop:'paddingBottom', b:3.6,  hi:3,   lo:2.4},
    {s:'.rb',       prop:'marginBottom',  b:4.5,  hi:3,   lo:2.4},
    {s:'.rfoot',    prop:'paddingTop',    b:6,    hi:3,   lo:2.8}
  ];
  const FRONT = [{s:'.rbody', prop:'marginTop', b:6, hi:8, lo:3.0}];
  document.querySelectorAll('.page').forEach(pgEl => {
    const body = pgEl.querySelector('.rbody'), foot = pgEl.querySelector('.rfoot');
    if (!body || !foot) return;
    const L = pgEl.querySelector('.pre-panel') ? SETUP
            : pgEl.querySelector('.msteps')    ? RUNBOOK : FRONT;
    const gap = () => foot.getBoundingClientRect().top - body.getBoundingClientRect().bottom;
    const apply = t => L.forEach(l => pgEl.querySelectorAll(l.s).forEach(e => {
      e.style[l.prop] = (t >= 0 ? l.b + l.hi * t : l.b - (l.b - l.lo) * (-t)) + (l.u || 'mm');
    }));
    const g0 = gap();
    if (Math.abs(g0 - TARGET) < 2) return;
    let lo, hi;
    if (g0 > TARGET) { apply(1); if (gap() >= TARGET) return; lo = 0; hi = 1; }
    else             { apply(-1); if (gap() < 0) return;      lo = -1; hi = 0; }
    for (let k = 0; k < 24; k++) {
      const m = (lo + hi) / 2; apply(m);
      if (gap() >= TARGET) lo = m; else hi = m;
    }
    apply(lo);
  });
}"""

OVERFLOW = """() => {
  const out = [];
  document.querySelectorAll('.page').forEach((pgEl, i) => {
    const inner = pgEl.querySelector('.inner');
    const ib = inner.getBoundingClientRect();
    let deepest = ib.top;
    inner.querySelectorAll('*').forEach(e => {
      const r = e.getBoundingClientRect();
      if (r.height > 0 && r.bottom > deepest) deepest = r.bottom;
    });
    const limit = ib.bottom - parseFloat(getComputedStyle(inner).paddingBottom);
    const kind = pgEl.querySelector('.pre-panel') ? 'SETUP'
               : pgEl.querySelector('.msteps')    ? 'RUNBOOK' : 'FRONT';
    let label = (pgEl.querySelector('.rtitle,.ptitle,.mh-title,h1') || {}).textContent || '';
    out.push({i: i + 1, label: (kind + ' ' + label).trim().slice(0, 46),
              spill: Math.round((deepest - limit) * 100) / 100,
              scroll: inner.scrollHeight - inner.clientHeight});
  });
  return out;
}"""

# Measured from the TRIM edge. The gutter carries no bleed, so the page box edge
# is the trim edge there; the outer, top and bottom edges each sit 3.175mm of
# bleed outside trim. This measures inner content/diagram bounds. The separate
# text-margin gate covers every printed text fragment, including page furniture.
SAFE = """() => {
  const MM = 96 / 25.4, BLEED = 3.175, out = [];
  document.querySelectorAll('.page').forEach((p, i) => {
    const pb = p.getBoundingClientRect();
    const inner = p.querySelector('.inner'); if (!inner) return;
    let minL = 1e9, maxR = -1e9;
    inner.querySelectorAll('*').forEach(e => {
      const q = e.getBoundingClientRect();
      if (q.width > 0 && q.height > 0) {
        if (q.left < minL) minL = q.left;
        if (q.right > maxR) maxR = q.right;
      }
    });
    if (minL > 1e8) return;                       // a blank page has no ink
    const recto = p.dataset.side === 'recto';
    const fromL = (minL - pb.left) / MM, fromR = (pb.right - maxR) / MM;
    out.push({i: i + 1,
              gutter: +(recto ? fromL : fromR).toFixed(2),
              outer:  +((recto ? fromR : fromL) - BLEED).toFixed(2)});
  });
  return out;
}"""

GAPS = """() => { const o = [];
  document.querySelectorAll('.page').forEach(p => {
    const b = p.querySelector('.rbody'), f = p.querySelector('.rfoot'); if (!b || !f) return;
    o.push(Math.round((f.getBoundingClientRect().top - b.getBoundingClientRect().bottom)
           * 25.4 / 96 * 10) / 10);
  }); return o; }"""

GUTTER_MIN, OUTER_MIN = 12.7, 6.35     # KDP, 151-300pp, measured from trim


async def main(write_pdf=True):
    src = ROOT / 'build' / 'book.html'
    if not src.exists():
        sys.exit('render: build/book.html not found - run book/build.py first')
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--font-render-hinting=none'])
        pg = await b.new_page(viewport={'width': 1200, 'height': 1600})
        await pg.goto(src.as_uri(), wait_until='networkidle')
        await pg.evaluate('document.fonts.ready')
        await pg.wait_for_timeout(1500)

        await pg.evaluate(JUSTIFY)
        await pg.wait_for_timeout(400)
        await check_print(pg)
        await check_text_margins(pg)

        over = await pg.evaluate(OVERFLOW)
        bad = [o for o in over if o['spill'] > 0.5 or o['scroll'] > 1]
        print(f"pages: {len(over)} | overflowing: {len(bad)}")
        for o in bad:
            print(f"  p{o['i']:>3} spill {o['spill']:>7}px  scroll {o['scroll']:>4}  {o['label']}")
        # AND IT FAILS, which it did not until 4.1.1. This block computed the
        # list of pages whose content runs past the text area, printed it, and
        # then wrote the PDF anyway - so two editions shipped a cost page with
        # 165px of the five-year table hanging off the bottom, and the only
        # evidence was a line of output nobody was reading. A check that
        # reports and does not gate is a check that has already failed.
        if bad:
            print(f'  CONTENT RUNS OFF {len(bad)} page(s) - the interior is not '
                  f'printable until they fit.')
            await b.close()
            raise SystemExit(1)
        print('closest to the edge:')
        for o in sorted(over, key=lambda o: -o['spill'])[:5]:
            print(f"  p{o['i']:>3} spill {o['spill']:>8}px  {o['label']}")

        safe = await pg.evaluate(SAFE)
        tight = [s for s in safe if s['gutter'] < GUTTER_MIN or s['outer'] < OUTER_MIN]
        g = min(s['gutter'] for s in safe)
        o = min(s['outer'] for s in safe)
        print(f'inner content bounds mm from trim | tightest gutter {g} (min {GUTTER_MIN})'
              f' | tightest outer {o} (min {OUTER_MIN})')
        if tight:
            print(f'  KDP SAFE AREA VIOLATED on {len(tight)} page(s):')
            for s in tight[:10]:
                print(f"    p{s['i']:>3} gutter {s['gutter']}mm outer {s['outer']}mm")
            await b.close()
            raise SystemExit(1)

        gaps = sorted(await pg.evaluate(GAPS))
        print('body-to-footer slack mm | min', gaps[0], '| median', gaps[len(gaps) // 2],
              '| max', gaps[-1])



        if write_pdf:
            OUT.parent.mkdir(exist_ok=True)
            await pg.pdf(path=str(OUT), width='8.375in', height='11.25in',
                         print_background=True,
                         margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
                         prefer_css_page_size=True)
            print(f'wrote {OUT.name} ({OUT.stat().st_size / 1e6:.2f} MB)')
        await b.close()


if __name__ == '__main__':
    asyncio.run(main('--nopdf' not in sys.argv))
