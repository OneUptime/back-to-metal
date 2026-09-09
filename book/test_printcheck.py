"""Rendered regressions for small text hidden by CSS or SVG scaling."""
import unittest

from playwright.sync_api import sync_playwright

from printcheck import MEASURE_PRINT_JS, violations


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


if __name__ == '__main__':
    unittest.main()
