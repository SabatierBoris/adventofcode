#!/usr/bin/env python3
import unittest

from common import Node, generate_tree


class TestNode(unittest.TestCase):
    def test_no_distance(self):
        n = Node("test")

        self.assertEqual(n.distance(), 0)

    def test_simple_distance(self):
        com = Node("COM")
        b = Node("B", com)
        c = Node("C", b)

        self.assertEqual(c.distance(), 2)

    def test_complexe_distance(self):
        com = Node("COM")
        b = Node("B", com)
        c = Node("C", b)
        g = Node("G", b)
        h = Node("H", g)

        self.assertEqual(h.distance(), 3)

    def test_distance_distance(self):
        com = Node("COM")
        b = Node("B", com)

        c = Node("C", b)
        d = Node("D", c)
        e = Node("E", d)
        f = Node("F", e)

        g = Node("G", b)
        h = Node("H", g)

        i = Node("I", d)
        san = Node("SAN", i)

        j = Node("J", e)
        k = Node("K", j)
        l = Node("L", k)
        you = Node("YOU", k)

        self.assertEqual(you.distance_with(san), 4)


class TestTree(unittest.TestCase):
    def test_generate(self):
        raw_data = """COM)B
                      B)C
                      C)D
                      D)E
                      E)F
                      B)G
                      G)H
                      D)I
                      E)J
                      J)K
                      K)L"""
        data = [l.strip().split(")") for l in raw_data.split("\n")]

        tree = generate_tree(data)

        result = 0
        for _, node in tree.items():
            result += node.distance()

        self.assertEqual(result, 42)

    def test_generate_with_com_in_middle(self):
        raw_data = """B)C
                      C)D
                      D)E
                      E)F
                      B)G
                      G)H
                      COM)B
                      D)I
                      E)J
                      J)K
                      K)L"""
        data = [l.strip().split(")") for l in raw_data.split("\n")]

        tree = generate_tree(data)

        result = 0
        for _, node in tree.items():
            result += node.distance()

        self.assertEqual(result, 42)


if __name__ == "__main__":
    unittest.main()
