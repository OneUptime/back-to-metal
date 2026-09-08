"""The website, driven: does every page actually render what it was built with?

The third gate. verify.py checks the shape of a Move and audit.py checks the
content; neither of them opens the site, and neither of them can, because the
failures this file exists to catch are not in the markup. They are in what the
browser does with it.

WHY IT EXISTS. v3.0.0 shipped with the roadmap on the front page invisible -
the one drawing of the whole schedule, a blank 153px band under its own
heading, for every reader whose scripting worked. The hidden state of that
chart was a `clip-path` on the SVG itself, and an IntersectionObserver measures
its target AFTER the target's own clip, so the observer reported an
intersection of nothing, never saw it arrive, and never revealed it. Every
check that ran before the release passed: the markup was right, the CSS parsed,
the links resolved, the contrast was fine, and the element was in the document
at its final position. It was simply not on the screen.

So this gate asks the only question that would have caught it, and it asks it
of a real browser: after a reader has scrolled the whole page, is anything the
build put on the reveal list still invisible? It also re-checks the two things
that are easy to break and impossible to see in a diff - that no page scrolls
sideways on a phone, and that the reveal is genuinely optional.

It needs Playwright, which the repository already installs for render.py, and
it needs site/ to have been built. It is not part of `make all` for the same
reason render.py is not: it is slow, and it belongs to the site rather than to
the book.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = ROOT / 'site'

# One of each kind of page. Running all twenty-five buys nothing: a Move page
# is a Move page, and the interesting variation is between the five templates.
PAGES = ['index.html', 'cost.html', 'checklist.html', 'start.html', 'about.html',
         'm/01-the-bill-and-the-three-lines-that-are-most-of-it.html',
         'm/16-postgres-the-one-that-matters.html']

WIDE = {'width': 1440, 'height': 950}
PHONE = {'width': 390, 'height': 844}

# How far to scroll before asking. The reveal deliberately holds back anything
# in the bottom eight per cent of the window, so a page has to be walked rather
# than jumped: jumping to the bottom skips the observer past everything in
# between and would let exactly the bug this file exists for through.
STEP = 0.7

# Contrast, in the browser rather than against the token table. Checking the
# tokens proves the palette; checking the page proves what the palette actually
# lands on, which is not the same thing - a colour is only ever correct against
# the background it ends up over, and `--fill` on a hovered row is a background
# the token table does not know about.
#
# `getClientRects().length` is the visibility test, not `display`. An element
# inside a hidden ancestor keeps its own display value: the print block hides
# `.cta`, and a `.btn` inside it still computes `inline-flex` and still reports
# a 1:1 colour pair that nothing will ever print. That false positive cost a
# real investigation once.
CONTRAST = """(onWhite) => {
  const lum = c => { const [r,g,b] = c.match(/\\d+(\\.\\d+)?/g).slice(0,3).map(Number);
    const f = v => { v/=255; return v<=.03928 ? v/12.92 : Math.pow((v+.055)/1.055,2.4) };
    return .2126*f(r)+.7152*f(g)+.0722*f(b) };
  const bgOf = el => { let n = el;
    while (n && n !== document.documentElement) {
      const bg = getComputedStyle(n).backgroundColor;
      if (bg && !/rgba\\(0, 0, 0, 0\\)|transparent/.test(bg)) return bg;
      n = n.parentElement }
    return getComputedStyle(document.documentElement).backgroundColor };
  const bad = [];
  for (const el of document.querySelectorAll('body *')) {
    if (!el.getClientRects().length) continue;
    if (el.closest('.vh')) continue;
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    const cs = getComputedStyle(el);
    if (cs.color === 'rgba(0, 0, 0, 0)') continue;
    const l1 = lum(cs.color);
    const l2 = onWhite ? 1 : lum(bgOf(el));
    const cr = (Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
    const size = parseFloat(cs.fontSize);
    const floor = (size >= 24 || (size >= 18.66 && +cs.fontWeight >= 700)) ? 3 : 4.5;
    if (cr < floor) bad.push(
      `${el.tagName.toLowerCase()}.${(el.className.baseVal ?? el.className).toString()
        .trim().split(/\\s+/).join('.')} at ${cr.toFixed(2)}:1 ` +
      `("${el.textContent.trim().slice(0,32)}")`);
  }
  return [...new Set(bad)];
}"""

STILL_HIDDEN = """(sel) => {
  if (!sel) return ['NO BTM_RISE_SEL: the corpus script did not load'];
  return [...document.querySelectorAll(sel)]
    .filter(e => {
      const cs = getComputedStyle(e);
      if (cs.display === 'none' || cs.visibility === 'hidden') return false;
      const b = e.getBoundingClientRect();
      if (!b.width && !b.height) return false;      /* laid out to nothing */
      return +cs.opacity < 0.9;
    })
    .map(e => `${e.tagName.toLowerCase()}.${(e.className.baseVal ?? e.className)
      .toString().trim().split(/\\s+/).join('.')}`);
}"""


def walk(page):
    """Scroll the whole document the way a reader would, then come back."""
    h = page.evaluate('document.documentElement.scrollHeight')
    vh = page.evaluate('innerHeight')
    y = 0
    while y < h:
        page.evaluate(f'window.scrollTo(0, {y})')
        page.wait_for_timeout(260)
        y += int(vh * STEP)
    page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
    page.wait_for_timeout(900)


def main():
    if not SITE.exists():
        sys.exit('webcheck: no site/ - run `make site` first')
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit('webcheck: playwright is not installed - see `make deps`')

    problems = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()

        # ---- 1. nothing the build hid is still hidden after a read -------
        page = browser.new_page(viewport=WIDE)
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        for rel in PAGES:
            page.goto((SITE / rel).as_uri())
            page.wait_for_timeout(900)
            walk(page)
            sel = page.evaluate('window.BTM_RISE_SEL || ""')
            for what in page.evaluate(STILL_HIDDEN, sel):
                problems.append(f'{rel}: {what} is still invisible after the whole '
                                f'page has been scrolled')
        if errors:
            problems += [f'console: {e}' for e in errors[:5]]

        # ---- 1b. and nothing on any of them is below the floor -----------
        # On screen, and again on paper, where the palette is a different one.
        for rel in PAGES:
            page.goto((SITE / rel).as_uri())
            page.wait_for_timeout(1400)
            walk(page)
            for what in page.evaluate(CONTRAST, False)[:6]:
                problems.append(f'{rel}: {what} on screen')
            page.emulate_media(media='print')
            page.wait_for_timeout(300)
            for what in page.evaluate(CONTRAST, True)[:6]:
                problems.append(f'{rel}: {what} in print')
            page.emulate_media(media='screen')
        page.close()

        # ---- 2. the reveal is optional, three ways -----------------------
        # Reduced motion, and a reader whose app.js never arrives. Both have to
        # leave a complete page: the hidden state may only exist while a script
        # that is known to be running is responsible for undoing it.
        for label, ctx in (
            ('reduced motion', browser.new_context(reduced_motion='reduce', viewport=WIDE)),
            ('app.js blocked', browser.new_context(viewport=WIDE)),
        ):
            pg = ctx.new_page()
            if label == 'app.js blocked':
                pg.route('**/app.js*', lambda r: r.abort())
            pg.goto((SITE / 'index.html').as_uri())
            pg.wait_for_timeout(3200)          # past the 2s failsafe
            sel = pg.evaluate('window.BTM_RISE_SEL || ""')
            for what in pg.evaluate(STILL_HIDDEN, sel):
                problems.append(f'index.html [{label}]: {what} is invisible, and '
                                f'nothing is going to reveal it')
            ctx.close()

        # ---- 3. no page scrolls sideways on a phone ----------------------
        ctx = browser.new_context(viewport=PHONE)
        pg = ctx.new_page()
        for rel in PAGES:
            pg.goto((SITE / rel).as_uri())
            pg.wait_for_timeout(700)
            over = pg.evaluate('document.documentElement.scrollWidth - innerWidth')
            if over > 1:
                problems.append(f'{rel}: {over}px of horizontal overflow at '
                                f'{PHONE["width"]}px')
        ctx.close()
        browser.close()

    if problems:
        print(f'\nwebcheck: {len(problems)} problems')
        for p in problems:
            print('  -', p)
        return 1
    print(f'webcheck: {len(PAGES)} pages, nothing left hidden, nothing under '
          f'contrast on screen or paper, no sideways scroll')
    return 0


if __name__ == '__main__':
    sys.exit(main())
