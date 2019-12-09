#!/usr/bin/env python3

import sys
from common import Program


def main():
    data = sys.stdin.readline()
    p = Program(data)
    p.send_input(2)
    p.execute()
    print(list(p))


if __name__ == "__main__":
    main()
