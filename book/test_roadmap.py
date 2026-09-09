"""Regression checks for calendar waiting and finite-worker scheduling."""
import unittest
from unittest.mock import patch

import roadmap


def move(number, effort='1 day', wait='—'):
    return {'num': number, 'figures': ['—', '—', '—', '0 min', effort, wait]}


class DurationTests(unittest.TestCase):
    def test_calendar_waits_use_equivalent_units(self):
        for days, weeks in [('7 days', '1 week'), ('14 days', '2 weeks'),
                            ('28 days', '4 weeks')]:
            with self.subTest(days=days):
                self.assertAlmostEqual(roadmap.wait_days(move('01', wait=days)),
                                       roadmap.wait_days(move('01', wait=weeks)))
        self.assertAlmostEqual(roadmap.wait_days(move('01', wait='1 month')),
                               roadmap.wait_days(move('01', wait='30.4 days')))
        self.assertAlmostEqual(roadmap.wait_days(move('01', wait='30 days')),
                               30 * 5 / 7)

    def test_ranges_keep_the_pessimistic_end(self):
        for duration, expected in [('6 to 12 weeks', 60), ('7–14 days', 10),
                                   ('1-2 months', 60.8 * 5 / 7)]:
            with self.subTest(duration=duration):
                self.assertAlmostEqual(roadmap.wait_days(move('01', wait=duration)),
                                       expected)

    def test_labour_units_are_unchanged(self):
        for duration, expected in [('7 days', 7), ('2 weeks', 10), ('1 month', 21),
                                   ('3 to 6 days', 6), ('< 1 day', 0.5)]:
            with self.subTest(duration=duration):
                self.assertEqual(roadmap.effort_days(move('01', effort=duration)),
                                 expected)

    def test_absent_wait_is_zero(self):
        for duration in ('—', '-', ''):
            with self.subTest(duration=duration):
                self.assertEqual(roadmap.wait_days(move('01', wait=duration)), 0)
        legacy = move('01')
        legacy['figures'].pop()
        self.assertEqual(roadmap.wait_days(legacy), 0)


class ScheduleTests(unittest.TestCase):
    def test_independent_work_fills_a_lower_numbered_moves_wait(self):
        moves = [move('01', '2 days', '14 days'), move('02', '1 day'),
                 move('03', '3 days')]
        with patch.object(roadmap, 'DEPS', {'02': ['01']}):
            result = roadmap.schedule(moves, workers=1)
            critical = roadmap.critical_path(moves)
        self.assertEqual(result['start'], {'01': 0, '03': 2, '02': 12})
        self.assertEqual(result['finish']['01'], 12)
        self.assertEqual(result['busy_until']['01'], 2)
        self.assertEqual(result['days'], 13)
        self.assertEqual(result['person_days'], 6)
        self.assertEqual(result['wait_days'], 10)
        self.assertEqual(critical['days'], 13)
        self.assertEqual(critical['chain'], ['01', '02'])

    def test_simultaneously_ready_work_uses_book_order(self):
        moves = [move('01', '2 days'), move('02', '4 days'),
                 move('03', '1 day'), move('04', '1 day')]
        with patch.object(roadmap, 'DEPS', {'03': ['01'], '04': ['01']}):
            result = roadmap.schedule(moves, workers=2)
        self.assertEqual(result['start'], {'01': 0, '02': 0, '03': 2, '04': 3})
        self.assertEqual(result['days'], 4)
        self.assertEqual(result['person_days'], 8)

    def test_ready_choice_respects_all_prerequisites_and_worker_capacity(self):
        moves = [move('01', '3 days', '1 week'), move('02', '1 day'),
                 move('03', '1 day'), move('04', '4 days'), move('05', '1 day')]
        dependencies = {'02': ['01'], '03': ['02'], '05': ['01', '04']}
        with patch.object(roadmap, 'DEPS', dependencies):
            result = roadmap.schedule(moves, workers=2)
        self.assertEqual(result['start'], {'01': 0, '04': 0, '02': 8,
                                          '05': 8, '03': 9})
        for number, prerequisites in dependencies.items():
            for prerequisite in prerequisites:
                self.assertGreaterEqual(result['start'][number],
                                        result['finish'][prerequisite])
        for instant in set(result['start'].values()):
            active = sum(start <= instant < result['busy_until'][number]
                         for number, start in result['start'].items())
            self.assertLessEqual(active, 2)
        self.assertEqual(result['person_days'], 10)
        self.assertEqual(result['days'], 10)

    def test_empty_schedule(self):
        result = roadmap.schedule([], workers=2)
        self.assertEqual(result['days'], 0)
        self.assertEqual(result['person_days'], 0)
        self.assertEqual(result['utilisation'], 0)


if __name__ == '__main__':
    unittest.main()
