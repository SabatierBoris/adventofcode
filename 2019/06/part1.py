#!/usr/bin/env python3
import sys

from common import generate_tree


def main():
    data = [l.strip().split(")") for l in sys.stdin.readlines()]

    tree = generate_tree(data)

    result = 0
    for _, node in tree.items():
        result += node.distance()

    print(result)


if __name__ == "__main__":
    main()
