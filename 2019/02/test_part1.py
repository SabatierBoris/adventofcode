#!/usr/bin/env python3
import unittest

from part1 import execute_add, execute_mult


class TestExecuteAdd(unittest.TestCase):
    def test_simple(self):
        memory = [1, 4, 5, 6, 1, 1, 0]
        pos = 0
        memory, pos, cont = execute_add(memory, pos)
        self.assertEqual(pos, 4)
        self.assertEqual(cont, True)
        self.assertEqual(memory, [1, 4, 5, 6, 1, 1, 2])

    def test_inplace(self):
        memory = [1, 0, 0, 0, 99]
        pos = 0
        memory, pos, cont = execute_add(memory, pos)
        self.assertEqual(pos, 4)
        self.assertEqual(cont, True)
        self.assertEqual(memory, [2, 0, 0, 0, 99])

    def test_out_of_range(self):
        memory = [1, 0, 0, 100, 99]
        pos = 0
        with self.assertRaises(IndexError):
            execute_add(memory, pos)

    def test_wrong_operator(self):
        memory = [2, 0, 0, 0, 99]
        pos = 0
        with self.assertRaises(AssertionError):
            execute_add(memory, pos)


class TestExecuteMult(unittest.TestCase):
    def test_simple(self):
        memory = [2, 4, 5, 6, 1, 1, 0]
        pos = 0
        memory, pos, cont = execute_mult(memory, pos)
        self.assertEqual(pos, 4)
        self.assertEqual(cont, True)
        self.assertEqual(memory, [2, 4, 5, 6, 1, 1, 1])

    def test_inplace(self):
        memory = [2, 0, 0, 0, 99]
        pos = 0
        memory, pos, cont = execute_mult(memory, pos)
        self.assertEqual(pos, 4)
        self.assertEqual(cont, True)
        self.assertEqual(memory, [4, 0, 0, 0, 99])

    def test_out_of_range(self):
        memory = [2, 0, 0, 100, 99]
        pos = 0
        with self.assertRaises(IndexError):
            execute_mult(memory, pos)

    def test_wrong_operator(self):
        memory = [1, 0, 0, 0, 99]
        pos = 0
        with self.assertRaises(AssertionError):
            execute_mult(memory, pos)


if __name__ == "__main__":
    unittest.main()
