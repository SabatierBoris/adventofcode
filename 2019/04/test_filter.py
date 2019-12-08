#!/usr/bin/env python3

import unittest
from collections import namedtuple

from common import (
    new_two_adjacent_filter,
    two_adjacent_filter,
    never_decrease_filter,
    six_digit_filter,
)


class TestFilter(unittest.TestCase):
    def test_six_digit(self):
        self.assertTrue(six_digit_filter(1))
        self.assertTrue(six_digit_filter(999999))
        self.assertFalse(six_digit_filter(1000000))

    def test_never_decrease(self):
        self.assertTrue(never_decrease_filter(123456))
        self.assertTrue(never_decrease_filter(1111123))
        self.assertFalse(never_decrease_filter(654321))
        self.assertFalse(never_decrease_filter(1111121))

    def test_two_adjacent(self):
        self.assertTrue(two_adjacent_filter(122345))
        self.assertTrue(two_adjacent_filter(111123))
        self.assertTrue(two_adjacent_filter(111111))
        self.assertFalse(two_adjacent_filter(123789))

    def test_new_two_adjacent(self):
        self.assertTrue(new_two_adjacent_filter(112233))
        self.assertTrue(new_two_adjacent_filter(111122))
        self.assertTrue(new_two_adjacent_filter(112222))
        self.assertFalse(new_two_adjacent_filter(123444))


if __name__ == "__main__":
    unittest.main()
