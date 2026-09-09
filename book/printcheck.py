"""Measure KDP's type and rule minimums in the rendered print layout.

An SVG's font-size is in drawing units, so a source-size check misses labels
shrunk by its viewBox. The browser's screen matrix includes that scaling and
nested transforms. These checks run after layout and before writing a PDF.
https://kdp.amazon.com/en_US/help/topic/G201857950
"""

MIN_FONT_PT = 7
MIN_RULE_PT = 0.75
TOLERANCE_PT = 0.01

MEASURE_PRINT_JS = r"""() => {
  const items = [], roots = [...document.querySelectorAll('.page,.sheet')];
  const pxToPt = 72 / 96;
  const vector = (e, x, y) => {
    if (e instanceof SVGGraphicsElement) {
      const m = e.getScreenCTM();
      return m ? Math.hypot(m.a*x + m.c*y, m.b*x + m.d*y) : 0;
    }
    for (let p = e; p; p = p.parentElement) {
      const s = getComputedStyle(p);
      if (s.transform !== 'none') {
        const m = new DOMMatrixReadOnly(s.transform);
        [x, y] = [m.a*x + m.c*y, m.b*x + m.d*y];
      }
      const zoom = parseFloat(s.zoom) || 1;
      x *= zoom; y *= zoom;
    }
    return Math.hypot(x, y);
  };
  const visible = e => {
    if (e.closest('script,style,template,svg title,svg desc,svg defs')) return false;
    const s = getComputedStyle(e);
    if (s.display === 'none' || s.visibility !== 'visible') return false;
    const r = e.getBoundingClientRect();
    return r.width > 0 || r.height > 0;
  };
  roots.forEach((root, i) => {
    const add = (e, kind, value, text = '') => items.push({
      page: i + 1, move: root.dataset.move || '', kind,
      selector: e.tagName.toLowerCase() + (e.id ? '#' + e.id : '')
                + (e.getAttribute('class') ? '.' + e.getAttribute('class').trim().replace(/\s+/g, '.') : ''),
      pt: value * pxToPt, text: text.trim().replace(/\s+/g, ' ').slice(0, 80)
    });
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      const e = node.parentElement;
      if (!node.textContent.trim() || !visible(e)) continue;
      const range = document.createRange(); range.selectNodeContents(node);
      if (![...range.getClientRects()].some(r => r.width > 0 && r.height > 0)) continue;
      add(e, 'font', parseFloat(getComputedStyle(e).fontSize) * vector(e, 0, 1), node.textContent);
    }
    root.querySelectorAll('*').forEach(e => {
      if (!visible(e)) return;
      const s = getComputedStyle(e), r = e.getBoundingClientRect();
      for (const edge of ['Top', 'Right', 'Bottom', 'Left']) {
        if (['none', 'hidden'].includes(s['border' + edge + 'Style'])) continue;
        const width = parseFloat(s['border' + edge + 'Width']);
        if (width > 0) add(e, 'border', width *
          (['Top', 'Bottom'].includes(edge) ? vector(e, 0, 1) : vector(e, 1, 0)));
      }
      if (s.columnRuleStyle !== 'none' && parseFloat(s.columnRuleWidth) > 0
          && parseInt(s.columnCount) > 1)
        add(e, 'column rule', parseFloat(s.columnRuleWidth) * vector(e, 1, 0));
      if (e.matches('.hrule,.cover-rule,.bk-rule,.ci .u') && r.width > 0 && r.height > 0)
        add(e, 'filled rule', Math.min(r.width, r.height));
      if (e instanceof SVGGeometryElement && s.stroke !== 'none'
          && parseFloat(s.strokeWidth) > 0) {
        const scale = s.vectorEffect === 'non-scaling-stroke' ? 1
                      : Math.min(vector(e, 1, 0), vector(e, 0, 1));
        add(e, 'SVG stroke', parseFloat(s.strokeWidth) * scale);
      }
    });
  });
  return items;
}"""


def violations(measurements):
    return [item for item in measurements
            if item['pt'] < (MIN_FONT_PT if item['kind'] == 'font' else MIN_RULE_PT)
            - TOLERANCE_PT]


async def check_print(page, label='interior'):
    """Raise before PDF output if any visible text or rule is too small."""
    measurements = await page.evaluate(MEASURE_PRINT_JS)
    bad = violations(measurements)
    fonts = [m['pt'] for m in measurements if m['kind'] == 'font']
    rules = [m['pt'] for m in measurements if m['kind'] != 'font']
    if not fonts:
        raise SystemExit(f'{label}: no visible print text measured')
    if bad:
        print(f'{label}: {len(bad)} text/rule measurements below KDP minimums')
        for item in bad[:12]:
            print(f'  p{item["page"]} {item["selector"]} {item["kind"]} '
                  f'{item["pt"]:.3f}pt {item["text"]}')
        raise SystemExit(1)
    floor = f'; thinnest rule {min(rules):.3f}pt' if rules else ''
    print(f'{label}: smallest text {min(fonts):.3f}pt{floor}')
