#!/usr/bin/env python3
import sys

from common import Point, process_wire


def execute(wire_1, wire_2):
    start_point = Point(0, 0)
    path_1 = process_wire(wire_1)
    path_2 = process_wire(wire_2)

    common_points = (set(path_1) & set(path_2)) - set([start_point])

    return min([path_1.index(p) + path_2.index(p) for p in common_points])


def main():
    wire_1 = sys.stdin.readline().strip().split(",")
    wire_2 = sys.stdin.readline().strip().split(",")
    print(execute(wire_1, wire_2))


if __name__ == "__main__":
    main()
