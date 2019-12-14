#!/usr/bin/env python3
import sys
from system import System


def ppcm(*n):
    """Calcul du 'Plus Petit Commun Multiple' de n (>=2) valeurs entières (Euclide)"""

    def _pgcd(a, b):
        while b:
            a, b = b, a % b
        return a

    p = abs(n[0] * n[1]) // _pgcd(n[0], n[1])
    for x in n[2:]:
        p = abs(p * x) // _pgcd(p, x)
    return p


def main():
    datas = [i.strip() for i in sys.stdin.readlines()]
    s = System(datas)
    loop_infos = s.find_loop()
    print(loop_infos)
    print(ppcm(*loop_infos))


if __name__ == "__main__":
    main()
