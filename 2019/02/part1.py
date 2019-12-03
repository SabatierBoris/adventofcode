#!/usr/bin/env python3
import sys


def execute_add(memory, pos):
    assert memory[pos] == 1
    memory[memory[pos + 3]] = memory[memory[pos + 1]] + memory[memory[pos + 2]]
    return memory, pos + 4, True


def execute_mult(memory, pos):
    assert memory[pos] == 2
    memory[memory[pos + 3]] = memory[memory[pos + 1]] * memory[memory[pos + 2]]
    return memory, pos + 4, True


def execute_end(memory, pos):
    return memory, pos, False


functions = {
    1: execute_add,
    2: execute_mult,
    99: execute_end,
}


def execute(memory):
    memory, pos, cont = functions[memory[0]](memory, 0)
    while cont:
        memory, pos, cont = functions[memory[pos]](memory, pos)
    return memory[0]


def main():
    memory = [int(v) for v in sys.stdin.readline().split(",")]
    print(execute(memory))


if __name__ == "__main__":
    main()
