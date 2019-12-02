#!/usr/bin/env python3
import sys


def computeFuelNeeded(mass):
    return (mass // 3) - 2


def computeFuelNeededForModule(mass):
    sumOfFuel = computeFuelNeeded(mass)
    moreFuelNeeded = computeFuelNeeded(sumOfFuel)
    while moreFuelNeeded > 0:
        sumOfFuel += moreFuelNeeded
        moreFuelNeeded = computeFuelNeeded(moreFuelNeeded)
    return sumOfFuel


def main():
    sumOfFuel = 0
    for line in sys.stdin:
        mass = int(line)
        sumOfFuel += computeFuelNeededForModule(mass)
    print(sumOfFuel)


if __name__ == "__main__":
    main()
