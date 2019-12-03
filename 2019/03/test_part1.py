#!/usr/bin/env python3

import unittest
from collections import namedtuple

from main import execute


class TestMain(unittest.TestCase):
    def test_global(self):
        TestCase = namedtuple("TestCase", ["wire_1", "wire_2", "result"])
        test_cases = [
            TestCase(["R8", "U5", "L5", "D3"], ["U7", "R6", "D4", "L4"], 6,),
            TestCase(
                ["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"],
                ["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"],
                159,
            ),
            TestCase(
                [
                    "R98",
                    "U47",
                    "R26",
                    "D63",
                    "R33",
                    "U87",
                    "L62",
                    "D20",
                    "R33",
                    "U53",
                    "R51",
                ],
                ["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"],
                135,
            ),
        ]

        for test_case in test_cases:
            with self.subTest():
                result = execute(test_case.wire_1, test_case.wire_2)
                self.assertEqual(test_case.result, result)


if __name__ == "__main__":
    unittest.main()
