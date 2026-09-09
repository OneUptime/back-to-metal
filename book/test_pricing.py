"""Worked KDP examples and royalty-band boundaries."""
import unittest

import pricing as P


class PricingTests(unittest.TestCase):
    def test_kdp_print_example_and_threshold(self):
        self.assertAlmostEqual(P.print_rate(9.99) * 9.99 - 4.60, 1.394)
        self.assertAlmostEqual(P.print_rate(9.98) * 9.98 - 4.60, 0.39)
        self.assertEqual(P.print_min_list(5.00, 0), 9.99)
        self.assertEqual(P.print_min_list(4.20, 0.25), 12.00)

    def test_short_premium_printing_band(self):
        self.assertEqual(P.print_cost(24, 'premium colour'), 4.20)
        self.assertEqual(P.print_cost(40, 'premium colour'), 4.20)
        self.assertAlmostEqual(P.print_cost(42, 'premium colour'), 4.36)
        self.assertAlmostEqual(P.print_cost(72, 'standard colour'), 3.8944)

    def test_kindle_delivery_is_inside_royalty_multiplier(self):
        row = P.kindle_row(1, 2.99)
        self.assertAlmostEqual(row['margin'] * 2.99, 0.70 * (2.99 - 0.15))
        self.assertEqual(row['need'], 2.99)

    def test_kindle_minimum_rounds_up_to_a_price_that_clears_target(self):
        required = P.kindle_row(13, None)['need']
        self.assertEqual(required, 3.04)
        self.assertGreaterEqual(P.kindle_row(13, required)['margin'],
                                P.IMP.MIN_KINDLE_MARGIN)
        self.assertLess(P.kindle_row(13, required - 0.01)['margin'],
                        P.IMP.MIN_KINDLE_MARGIN)

    def test_kindle_break_even_floor_also_rounds_up(self):
        floor = P.kindle_row(20.01, None)['floor']
        self.assertEqual(floor, 3.01)
        self.assertGreaterEqual(P.kindle_row(20.01, floor)['margin'], 0)
        self.assertLess(P.kindle_row(20.01, floor - 0.01)['margin'], 0)

    def test_kindle_requires_discount_from_every_physical_edition(self):
        self.assertEqual(P.kindle_price_problems(8.99, {'paperback': 11.99, 'hardback': 33.99}), [])
        self.assertTrue(P.kindle_price_problems(9.99, {'paperback': 11.99, 'hardback': 33.99}))
        self.assertTrue(P.kindle_price_problems(9.99, {'paperback': 33.99, 'hardback': 11.99}))

    def test_kindle_discount_boundary_and_unset_print_prices(self):
        self.assertEqual(P.kindle_price_problems(8.00, {'paperback': 10.00}), [])
        self.assertTrue(P.kindle_price_problems(8.01, {'paperback': 10.00}))
        self.assertEqual(P.kindle_price_problems(8.99, {'paperback': None}), [])


if __name__ == '__main__':
    unittest.main()
