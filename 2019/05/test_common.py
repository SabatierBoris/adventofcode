#!/usr/bin/env python3
import unittest

from common import execute_add, execute_mult, get_mode


class TestGetMode(unittest.TestCase):
    def test_default(self):
        mode = get_mode(1, 3)

        self.assertEqual(mode, [0, 0, 0])

    def test_setted(self):
        mode = get_mode(1001, 3)

        self.assertEqual(mode, [0, 1, 0])

    def test_full_setted(self):
        mode = get_mode(11101, 3)

        self.assertEqual(mode, [1, 1, 1])


class TestExecuteAdd(unittest.TestCase):
    def test_simple(self):
        memory = [1, 4, 5, 6, 1, 1, 0]
        pos = 0
        memory, pos, cont = execute_add(memory, pos)
        self.assertEqual(pos, 4)
        self.assertEqual(cont, True)
        self.assertEqual(memory, [1, 4, 5, 6, 1, 1, 2])

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

    def test_immediate_one(self):
        memory = [1001, 0, 4, 0, 99]
        pos = 0
        memory, pos, cont = execute_add(memory, pos)
        self.assertEqual(pos, 4)
        self.assertEqual(cont, True)
        self.assertEqual(memory, [1005, 0, 4, 0, 99])

    def test_immediate_two(self):
        memory = [1101, 5, 4, 0, 99]
        pos = 0
        memory, pos, cont = execute_add(memory, pos)
        self.assertEqual(pos, 4)
        self.assertEqual(cont, True)
        self.assertEqual(memory, [9, 5, 4, 0, 99])

    def test_immediate_result_error(self):
        memory = [10001, 0, 0, 0, 99]
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

    def test_immediate_one(self):
        memory = [1002, 0, 4, 0, 99]
        pos = 0
        memory, pos, cont = execute_mult(memory, pos)
        self.assertEqual(pos, 4)
        self.assertEqual(cont, True)
        self.assertEqual(memory, [4008, 0, 4, 0, 99])

    def test_immediate_two(self):
        memory = [1102, 5, 4, 0, 99]
        pos = 0
        memory, pos, cont = execute_mult(memory, pos)
        self.assertEqual(pos, 4)
        self.assertEqual(cont, True)
        self.assertEqual(memory, [20, 5, 4, 0, 99])

    def test_immediate_result_error(self):
        memory = [10002, 0, 0, 0, 99]
        pos = 0
        with self.assertRaises(AssertionError):
            execute_mult(memory, pos)


if __name__ == "__main__":
    unittest.main()
