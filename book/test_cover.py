"""KDP spine text must clear both page eligibility and binding tolerances."""
import unittest

import cover


class SpineTextTests(unittest.TestCase):
    def test_short_books_never_print_spine_text(self):
        self.assertEqual(cover.spine_text(76, 0.5), '')
        self.assertEqual(cover.spine_text(79, 0.5), '')

    def test_page_eligibility_does_not_make_a_narrow_spine_readable(self):
        self.assertEqual(cover.spine_text(80, 80 * 0.002252), '')
        self.assertEqual(cover.spine_text(120, 0.125), '')

    def test_eligible_spine_includes_title_and_author(self):
        text = cover.spine_text(200, 0.5)
        self.assertIn(cover.IMP.TITLE, text)
        self.assertIn(cover.IMP.AUTHOR, text)
        self.assertIn('font-size:12.000pt', text)


if __name__ == '__main__':
    unittest.main()
