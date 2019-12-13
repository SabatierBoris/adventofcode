#!/usr/bin/env python3

import sys
from program import Program
from game import Game


def main():
    data = sys.stdin.readline()
    g = Game(Program(data))
    g.execute()
    g.update_state()
    print(g.get_nb_of_block())


if __name__ == "__main__":
    main()
