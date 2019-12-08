#!/usr/bin/env python3
import sys

from common import generate_tree


def main():
    data = [l.strip().split(")") for l in sys.stdin.readlines()]

    tree = generate_tree(data)

    you = tree["YOU"]
    san = tree["SAN"]

    print(you.distance_with(san))


if __name__ == "__main__":
    main()
