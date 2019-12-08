#!/usr/bin/env python3
import unittest

from common import Program, process_part1, process_part2


class TestGetMode(unittest.TestCase):
    def test_default(self):
        mode = Program.get_mode(1, 3)

        self.assertEqual(mode, [0, 0, 0])

    def test_setted(self):
        mode = Program.get_mode(1001, 3)

        self.assertEqual(mode, [0, 1, 0])

    def test_full_setted(self):
        mode = Program.get_mode(11101, 3)

        self.assertEqual(mode, [1, 1, 1])


class TestErrors(unittest.TestCase):
    def test_out_of_range(self):
        p = Program("1, 0, 0, 100, 99")
        with self.assertRaises(IndexError):
            p.step()

    def test_immediate_result_error(self):
        p = Program("10001, 0, 0, 0, 99")
        with self.assertRaises(AssertionError):
            p.step()

    def test_out_of_range(self):
        p = Program("98, 0, 0, 100, 99")
        with self.assertRaises(AssertionError):
            p.step()


class TestExecuteAdd(unittest.TestCase):
    def test_simple(self):
        p = Program("1,4,5,6,1,1,0")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [1, 4, 5, 6, 1, 1, 2])

    def test_inplace(self):
        p = Program("1, 0, 0, 0, 99")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [2, 0, 0, 0, 99])

    def test_immediate_one(self):
        p = Program("1001, 0, 4, 0, 99")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [1005, 0, 4, 0, 99])

    def test_immediate_two(self):
        p = Program("1101, 5, 4, 0, 99")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [9, 5, 4, 0, 99])


class TestExecuteMult(unittest.TestCase):
    def test_simple(self):
        p = Program("2, 4, 5, 6, 1, 1, 0")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [2, 4, 5, 6, 1, 1, 1])

    def test_inplace(self):
        p = Program("2, 0, 0, 0, 99")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [4, 0, 0, 0, 99])

    def test_immediate_one(self):
        p = Program("1002, 0, 4, 0, 99")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [4008, 0, 4, 0, 99])

    def test_immediate_two(self):
        p = Program("1102, 5, 4, 0, 99")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [20, 5, 4, 0, 99])


class TestInput(unittest.TestCase):
    def test_simple(self):
        p = Program("3, 1")
        p.send_input(42)
        p.step()
        self.assertEqual(p._Program__pos, 2)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [3, 42])


class TestOuput(unittest.TestCase):
    def test_simple(self):
        p = Program("4, 0")
        p.step()
        self.assertEqual(p._Program__pos, 2)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [4, 0])
        self.assertEqual(next(p), 4)

    def test_direct(self):
        p = Program("104, 0")
        p.step()
        self.assertEqual(p._Program__pos, 2)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [104, 0])
        self.assertEqual(next(p), 0)


class TestJumpIfTrue(unittest.TestCase):
    def test_simple_true(self):
        p = Program("5, 0, 0")
        p.step()
        self.assertEqual(p._Program__pos, 5)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [5, 0, 0])

    def test_direct_true(self):
        p = Program("1105, 1, 0")
        p.step()
        self.assertEqual(p._Program__pos, 0)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [1105, 1, 0])

    def test_simple_false(self):
        p = Program("5, 2, 0")
        p.step()
        self.assertEqual(p._Program__pos, 3)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [5, 2, 0])


class TestJumpIfFalse(unittest.TestCase):
    def test_simple_false(self):
        p = Program("6, 2, 0")
        p.step()
        self.assertEqual(p._Program__pos, 6)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [6, 2, 0])

    def test_direct_false(self):
        p = Program("1106, 0, 0")
        p.step()
        self.assertEqual(p._Program__pos, 0)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [1106, 0, 0])

    def test_simple_true(self):
        p = Program("6, 1, 0")
        p.step()
        self.assertEqual(p._Program__pos, 3)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [6, 1, 0])


class TestLessThan(unittest.TestCase):
    def test_true(self):
        p = Program("7, 1, 0, 3")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [7, 1, 0, 1])

    def test_false(self):
        p = Program("7, 0, 1, 3")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [7, 0, 1, 0])

    def test_direct_true(self):
        p = Program("1107, 0, 1, 3")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [1107, 0, 1, 1])

    def test_direct_false(self):
        p = Program("1107, 1, 0, 3")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [1107, 1, 0, 0])


class TestEquals(unittest.TestCase):
    def test_true(self):
        p = Program("8, 0, 0, 3")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [8, 0, 0, 1])

    def test_false(self):
        p = Program("8, 0, 1, 3")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [8, 0, 1, 0])

    def test_direct_true(self):
        p = Program("1108, 1, 1, 3")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [1108, 1, 1, 1])

    def test_direct_false(self):
        p = Program("1108, 1, 0, 3")
        p.step()
        self.assertEqual(p._Program__pos, 4)
        self.assertEqual(p._Program__running, True)
        self.assertEqual(p._Program__memory, [1108, 1, 0, 0])


class TestHalt(unittest.TestCase):
    def test_simple(self):
        p = Program("99")
        p.step()
        self.assertEqual(p._Program__pos, 1)
        self.assertEqual(p._Program__running, False)
        self.assertEqual(p._Program__memory, [99])


class TestFonctionnal(unittest.TestCase):
    def test_day2_part1(self):
        datas = [
            ("1,9,10,3,2,3,11,0,99,30,40,50", 3500),
        ]
        for data, result in datas:
            with self.subTest(data=data):
                p = Program(data)
                p.execute()
                self.assertEqual(p._Program__memory[0], result)

    def test_day5_part2(self):
        datas = [
            (
                "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99",
                7,
                999,
            ),
            (
                "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99",
                8,
                1000,
            ),
            (
                "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99",
                9,
                1001,
            ),
        ]
        for data, data_input, result in datas:
            with self.subTest(data=data):
                p = Program(data)
                p.send_input(data_input)
                p.execute()
                self.assertEqual(next(p), result)

    def test_day7_part1(self):
        datas = [
            ("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", 43210),
            (
                "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
                54321,
            ),
            (
                "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
                65210,
            ),
        ]
        for data, result in datas:
            with self.subTest(data=data):
                self.assertEqual(process_part1(data), result)

    def test_day7_part2(self):
        datas = [
            (
                "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
                139629729,
            ),
            (
                "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10",
                18216,
            ),
        ]
        for data, result in datas:
            with self.subTest(data=data):
                self.assertEqual(process_part2(data), result)


if __name__ == "__main__":
    unittest.main()
