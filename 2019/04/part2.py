#!/usr/bin/env python3
import sys

from common import (
    new_two_adjacent_generator,
    never_decrease_generator,
    six_digit_generator,
)


def main():

    start, end = [int(v) for v in sys.stdin.readline().strip().split("-")]

    passwords = new_two_adjacent_generator(
        never_decrease_generator(six_digit_generator(range(start, end + 1)))
    )

    print(len(list(passwords)))


if __name__ == "__main__":
    main()
