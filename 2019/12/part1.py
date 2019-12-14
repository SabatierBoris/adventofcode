#!/usr/bin/env python3
import sys
from system import System

NB_STEP = 1000


def main():
    datas = [i.strip() for i in sys.stdin.readlines()]
    s = System(datas)
    print(s)
    for i in range(NB_STEP):
        s.update()
        # print("")
        # print("After %s step:" % (i + 1))
        # print(s)
    print(s.get_energy())


if __name__ == "__main__":
    main()
