#!/usr/bin/env python3
import sys
from cookbook import CookBook


def main():
    book = CookBook([l.strip() for l in sys.stdin.readlines()])

    qty = 1_000_000_000_000
    print(book.get_from(qty, "ORE", "FUEL"))

    print("KO", 2521843)


if __name__ == "__main__":
    main()
