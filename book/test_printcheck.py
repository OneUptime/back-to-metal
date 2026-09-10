"""Rendered regressions for small text hidden by CSS or SVG scaling."""
import unittest

from playwright.sync_api import sync_playwright

from printcheck import (MEASURE_PRINT_JS, MEASURE_TEXT_MARGINS_JS,
                        text_margin_violations, violations)


class PrintCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def measure(self, body):
        page = self.browser.new_page()
        try:
            page.set_content('<main class="sheet">' + body + '</main>')
            return page.evaluate(MEASURE_PRINT_JS)
        finally:
            page.close()

    def measure_margins(self, body, side='recto'):
        page = self.browser.new_page()
        try:
            page.set_content(
                '<style>.page{position:relative;width:8.375in;height:11.25in;'
                'font:10pt Arial}.inner{position:absolute;inset:20mm}</style>'
                f'<section class="page" data-side="{side}">{body}</section>')
            return page.evaluate(MEASURE_TEXT_MARGINS_JS)
        finally:
            page.close()

    def test_checks_parent_text_and_ignores_hidden_text(self):
        measured = self.measure(
            '<p id="small" style="font-size:6pt">Before '
            '<b style="font-size:8pt">Large</b> after</p>'
            '<p id="good" style="font-size:7pt">Readable</p>'
            '<p style="display:none;font-size:1pt">Hidden</p>'
            '<script>Hidden text</script>')
        bad = violations(measured)
        self.assertEqual([m['text'] for m in bad], ['Before', 'after'])
        self.assertTrue(all(m['selector'] == 'p#small' for m in bad))
        self.assertAlmostEqual(next(m['pt'] for m in measured if m['selector'] == 'p#good'),
                               7, places=4)

    def test_measures_svg_viewbox_and_nested_css_transforms(self):
        measured = self.measure(
            '<div style="transform:scale(.5);transform-origin:top left">'
            '<p id="scaled" style="font-size:12pt">Scaled down</p></div>'
            '<svg width="100" height="100" viewBox="0 0 200 200">'
            '<title>Not printed</title>'
            '<text id="svg-small" x="0" y="30" font-size="12">Small</text>'
            '<text id="svg-good" x="0" y="70" font-size="20">Large</text>'
            '</svg>')
        self.assertEqual({m['selector'] for m in violations(measured)},
                         {'p#scaled', 'text#svg-small'})
        sizes = {m['selector']: m['pt'] for m in measured}
        self.assertAlmostEqual(sizes['p#scaled'], 6)
        self.assertAlmostEqual(sizes['text#svg-small'], 4.5)
        self.assertAlmostEqual(sizes['text#svg-good'], 7.5)

    def test_checks_effective_rules_and_non_scaling_strokes(self):
        measured = self.measure(
            '<p style="font-size:7pt;border-bottom:1px solid black">Text</p>'
            '<div class="hrule" style="height:.5px;background:black"></div>'
            '<svg width="100" height="100" viewBox="0 0 200 200">'
            '<line id="thin" x1="0" y1="10" x2="190" y2="10" '
            'stroke="black" stroke-width="1"/>'
            '<line id="fixed" x1="0" y1="30" x2="190" y2="30" '
            'stroke="black" stroke-width="1" vector-effect="non-scaling-stroke"/>'
            '</svg>')
        self.assertEqual({m['selector'] for m in violations(measured)},
                         {'div.hrule', 'line#thin'})
        sizes = {m['selector']: m['pt'] for m in measured if m['kind'] != 'font'}
        self.assertAlmostEqual(sizes['line#thin'], .375)
        self.assertAlmostEqual(sizes['line#fixed'], .75)

    def test_rejects_fore_edge_text_outside_inner_on_both_page_sides(self):
        # This is the layout that passed the old .inner-only check and was
        # rejected by KDP. A margin check must see the sibling tab's text.
        for side, edge in (('recto', 'right'), ('verso', 'left')):
            with self.subTest(side=side):
                measured = self.measure_margins(
                    '<div class="inner">Safe body text</div>'
                    f'<span id="tab" style="position:absolute;{edge}:0;top:70mm;'
                    'width:9mm;height:26mm;display:flex;align-items:center;'
                    'justify-content:center;writing-mode:vertical-rl">BUY</span>', side)
                bad = text_margin_violations(measured['items'], measured['pages'])
                self.assertEqual({(m['selector'], m['edge']) for m in bad},
                                 {('span#tab', 'outer')})

    def test_checks_top_and_bottom_furniture_and_allows_text_free_bleed(self):
        measured = self.measure_margins(
            '<div style="position:absolute;inset:0;background:gray"></div>'
            '<div class="inner">Safe body text</div>'
            '<span id="head" style="position:absolute;left:20mm;top:5mm">Title</span>'
            '<span id="folio" style="position:absolute;left:20mm;bottom:8mm">Runbook</span>'
            '<span id="page" style="position:absolute;right:20mm;bottom:13.25mm">37</span>'
            '<span style="display:none;position:absolute;top:0">Hidden</span>')
        bad = text_margin_violations(measured['items'], measured['pages'])
        self.assertEqual({(m['selector'], m['edge']) for m in bad},
                         {('span#head', 'top'), ('span#folio', 'bottom')})

    def test_svg_text_is_measured_after_rotation_and_viewbox_scaling(self):
        measured = self.measure_margins(
            '<svg style="position:absolute;left:20mm;top:20mm;overflow:visible" '
            'width="100" height="100" viewBox="0 0 200 200">'
            '<title>Not printed</title><desc>Not printed either</desc>'
            '<text id="rotated" transform="translate(40 -100) rotate(90)" '
            'font-size="20">Rotated label</text></svg>')
        bad = text_margin_violations(measured['items'], measured['pages'])
        self.assertEqual({(m['selector'], m['edge']) for m in bad},
                         {('text#rotated', 'top')})
        self.assertTrue(all(m['text'] == 'Rotated label' for m in measured['items']))

    def test_preserved_spaces_count_towards_the_margin(self):
        for text in ('Word            ', '            '):
            with self.subTest(text=text):
                measured = self.measure_margins(
                    '<span id="spaces" style="position:absolute;right:10mm;top:20mm;'
                    f'white-space:pre">{text}</span>')
                bad = text_margin_violations(measured['items'], measured['pages'])
                self.assertEqual({(m['selector'], m['edge']) for m in bad},
                                 {('span#spaces', 'outer')})
                self.assertAlmostEqual(bad[0]['outer'], 10, delta=.01)

    def test_gutter_requirement_increases_with_page_count(self):
        for side, edge in (('recto', 'left'), ('verso', 'right')):
            with self.subTest(side=side):
                measured = self.measure_margins(
                    f'<span style="position:absolute;{edge}:14mm;top:20mm">'
                    'Gutter text</span>', side)['items']
                self.assertEqual(text_margin_violations(measured, 300), [])
                for count, minimum in ((301, 15.875), (501, 19.05), (701, 22.225)):
                    bad = text_margin_violations(measured, count)
                    self.assertEqual(len(bad), 1)
                    self.assertEqual(bad[0]['edge'], 'gutter')
                    self.assertEqual(bad[0]['minimum'], minimum)


if __name__ == '__main__':
    unittest.main()
