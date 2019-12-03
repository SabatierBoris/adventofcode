#!/usr/bin/env python3
import itertools
import sys

from part1 import execute


def mutate(memory, noun, verb):
    memory[1] = noun
    memory[2] = verb

    return memory


def main():
    initial_memory = [int(v) for v in sys.stdin.readline().split(",")]
    for noun, verb in itertools.product(range(100), repeat=2):
        tested_memory = mutate(list(initial_memory), noun, verb)
        result = execute(tested_memory)
        if result == 19690720:
            print(noun, verb, 100 * noun + verb)
            return


if __name__ == "__main__":
    main()
