#!/usr/bin/env python3

import sys


from common import get_layers, merge_layers


def main():
    wide = int(sys.stdin.readline().strip())
    tall = int(sys.stdin.readline().strip())
    data = sys.stdin.readline().strip()

    layers = get_layers(data, wide, tall)

    print(merge_layers(layers))


if __name__ == "__main__":
    main()
