#!/usr/bin/env python3

import sys


from common import get_layers, parse_infos


def main():
    wide = int(sys.stdin.readline().strip())
    tall = int(sys.stdin.readline().strip())
    data = sys.stdin.readline().strip()

    layers = get_layers(data, wide, tall)

    layers_infos = [parse_infos(layer) for layer in layers]

    for info in layers_infos:
        print(info)

    def get_zero(info):
        return info.get("0", 0)

    min_layer = min(layers_infos, key=get_zero)
    print(min_layer)

    print(min_layer["1"] * min_layer["2"])


if __name__ == "__main__":
    main()
