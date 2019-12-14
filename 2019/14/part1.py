#!/usr/bin/env python3
import sys
from cookbook import CookBook


def main():
    book = CookBook([l.strip() for l in sys.stdin.readlines()])
    print(book.get("FUEL", "ORE"))


if __name__ == "__main__":
    main()
