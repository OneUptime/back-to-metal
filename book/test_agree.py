"""Regression checks for omitted content in otherwise valid publications."""
import unittest

import agree
import epub
from parse import load_all, inline


class AgreementTests(unittest.TestCase):
    def setUp(self):
        self.use_move(load_all()[0])

    def use_move(self, move):
        self.move = move
        self.number = self.move['num']
        text = ''.join(f'<p>{inline(value)}</p>'
                       for _, value in agree.move_fragments(self.move))
        risk, reversible = move['risk'], move['reversible']
        cutover = f'{move["cutover"]} min'
        figures = ''.join(
            f'<div class="fig"><div class="v">{inline(value)}</div>'
            f'<div class="k">{label}</div></div>'
            for label, value in zip(('Was', 'Now', 'Saved', 'Cutover', 'Effort', 'Wait'),
                                    move['figures']))
        spec = (f'<div class="k">Risk</div><div class="v">{risk.upper()}</div>'
                f'<div class="k">Reversible</div><div class="v">{reversible.upper()}</div>'
                f'<div class="mk">Cutover</div><div class="mv">{move["cutover"]}<i>MIN</i></div>'
                + figures)
        self.print = (f'<section data-side="verso" data-move="{self.number}">{spec}{text}</section>'
                      f'<section data-side="recto" data-move="{self.number}"></section>')
        backout = 'Cannot be undone' if reversible == 'No' else reversible
        facts = (f'<dt class="lbl">Risk</dt><dd>{risk}</dd>'
                 f'<dt class="lbl">Back out</dt><dd>{backout}</dd>'
                 f'<dt class="lbl">Cutover</dt><dd>{cutover}</dd>')
        self.site = {self.number: facts + text}

    def problems_with(self, output, markup):
        book = markup if output == 'print' else self.print
        site = {self.number: markup} if output == 'website' else self.site
        electronic = markup if output == 'EPUB' else epub.move_xhtml(self.move)
        return agree.content_problems([self.move], book, site, {self.number: electronic})

    def metadata_cases(self, key):
        risk, reversible = self.move['risk'], self.move['reversible']
        cutover = str(self.move['cutover'])
        backout = 'Cannot be undone' if reversible == 'No' else reversible
        needles = {
            'reversible': (
                f'<div class="k">Reversible</div><div class="v">{reversible.upper()}</div>',
                f'<dt class="lbl">Back out</dt><dd>{backout}</dd>',
                f'reversible: {reversible}'),
            'risk': (
                f'<div class="k">Risk</div><div class="v">{risk.upper()}</div>',
                f'<dt class="lbl">Risk</dt><dd>{risk}</dd>',
                f'{risk} risk'),
            'Cutover': (
                f'<div class="mk">Cutover</div><div class="mv">{cutover}<i>MIN</i></div>',
                f'<dt class="lbl">Cutover</dt><dd>{cutover} min</dd>',
                f'{cutover} min cutover'),
        }
        for output, markup, needle in zip(
                ('print', 'website', 'EPUB'),
                (self.print, self.site[self.number], epub.move_xhtml(self.move)),
                needles[key]):
            yield output, markup, needle

    def test_cloud_extraction_is_present_in_real_epub_renderer(self):
        markup = epub.move_xhtml(self.move)
        self.assertEqual(agree.content_problems(
            [self.move], self.print, self.site, {self.number: markup}), [])

    def test_missing_cloud_warning_fails_even_when_hidden_copy_exists(self):
        markup = epub.move_xhtml(self.move)
        warning = inline(self.move['origins'][0]['note'])
        markup = markup.replace(warning, '') + f'<script>{warning}</script>'
        problems = agree.content_problems(
            [self.move], self.print, self.site, {self.number: markup})
        self.assertIn(f'Move {self.number}: EPUB missing or stale AWS extraction', problems)

    def test_missing_rollback_is_reported_for_its_output(self):
        self.site[self.number] = self.site[self.number].replace(
            inline(self.move['rollback']), '')
        problems = agree.content_problems(
            [self.move], self.print, self.site,
            {self.number: epub.move_xhtml(self.move)})
        self.assertIn(f'Move {self.number}: website missing or stale rollback', problems)

    def test_irreversible_move_accepts_web_backout_label(self):
        self.use_move(next(m for m in load_all() if m['reversible'] == 'No'))
        self.assertEqual(self.problems_with('EPUB', epub.move_xhtml(self.move)), [])

    def test_wrong_or_missing_reversibility_cannot_hide_in_other_text(self):
        self.use_move(next(m for m in load_all() if m['reversible'] == 'No'))
        for output, markup, needle in self.metadata_cases('reversible'):
            for replacement in ('', needle.replace('NO', 'IMMEDIATELY')
                                .replace('No', 'Immediately')
                                .replace('Cannot be undone', 'Immediately')):
                with self.subTest(output=output, replacement=replacement):
                    altered = markup.replace(needle, replacement)
                    # The old substring check accepted "No" in ordinary prose.
                    altered += '<p>No data loss; do not proceed blindly.</p>'
                    problems = self.problems_with(output, altered)
                    self.assertIn(
                        f'Move {self.number}: {output} missing or stale reversible metadata',
                        problems)

    def test_risk_and_zero_cutover_must_match_their_labelled_values(self):
        for key in ('risk', 'Cutover'):
            for output, markup, needle in self.metadata_cases(key):
                with self.subTest(key=key, output=output):
                    replacement = (needle.replace('LOW', 'HIGH').replace('Low', 'High')
                                   if key == 'risk' else needle.replace('0', '10'))
                    altered = markup.replace(needle, replacement)
                    altered += '<p>Low risk, 0 min cutover in another context.</p>'
                    self.assertIn(
                        f'Move {self.number}: {output} missing or stale {key} metadata',
                        self.problems_with(output, altered))

    def test_cutover_figure_is_checked_separately_from_header(self):
        cases = (
            ('print', self.print, '<div class="v">0 min</div>'),
            ('EPUB', epub.move_xhtml(self.move), 'cutover 0 min'),
        )
        for output, markup, needle in cases:
            with self.subTest(output=output):
                altered = markup.replace(needle, needle.replace('0', '10'))
                self.assertIn(
                    f'Move {self.number}: {output} missing or stale Cutover figure metadata',
                    self.problems_with(output, altered))

    def test_hidden_metadata_cannot_repair_missing_visible_field(self):
        for output, markup, needle in self.metadata_cases('reversible'):
            with self.subTest(output=output):
                altered = markup.replace(needle, '') + f'<script>{needle}</script>'
                self.assertIn(
                    f'Move {self.number}: {output} missing or stale reversible metadata',
                    self.problems_with(output, altered))


if __name__ == '__main__':
    unittest.main()
