#!/usr/bin/env python3
import sys


def computeFuelNeeded(mass):
    return (mass // 3) - 2


def main():
    sumOfFuel = 0
    for line in sys.stdin:
        mass = int(line)
        sumOfFuel += computeFuelNeeded(mass)
    print(sumOfFuel)


if __name__ == "__main__":
    main()
