#!/usr/bin/env python3
import unittest

from common import get_layers, parse_infos, merge_layers


class TestGetLayers(unittest.TestCase):
    def test_simple(self):
        wide = 3
        tall = 2
        data = "123456789012"

        layers = list(get_layers(data, wide, tall))

        self.assertEqual(len(layers), 2)
        self.assertEqual(layers[0], "123456")
        self.assertEqual(layers[1], "789012")


class TestGetLayers(unittest.TestCase):
    def test_simple(self):
        layer = "123456"
        infos = parse_infos(layer)

        self.assertEqual(infos, {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1})


class TestMergeLayers(unittest.TestCase):
    def test_simple(self):
        layers = ["0222", "1122", "2212", "0000"]
        layer = merge_layers(layers)

        self.assertEqual(layer, "0110")


parse_infos
pass


if __name__ == "__main__":
    unittest.main()
