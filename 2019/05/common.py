#!/usr/bin/env python3
import sys


def get_mode(value, nb_params):
    mode = []
    value //= 100
    for i in range(nb_params):
        mode.append(value % 10)
        value //= 10
    return mode


def execute_add(memory, pos):
    assert memory[pos] % 10 == 1
    mode = get_mode(memory[pos], 3)
    assert mode[2] == 0

    val_a = memory[memory[pos + 1]] if mode[0] == 0 else memory[pos + 1]
    val_b = memory[memory[pos + 2]] if mode[1] == 0 else memory[pos + 2]

    memory[memory[pos + 3]] = val_a + val_b
    return memory, pos + 4, True


def execute_mult(memory, pos):
    assert memory[pos] % 10 == 2
    mode = get_mode(memory[pos], 3)
    assert mode[2] == 0

    val_a = memory[memory[pos + 1]] if mode[0] == 0 else memory[pos + 1]
    val_b = memory[memory[pos + 2]] if mode[1] == 0 else memory[pos + 2]

    memory[memory[pos + 3]] = val_a * val_b
    return memory, pos + 4, True


def execute_input(memory, pos):
    assert memory[pos] % 10 == 3
    mode = get_mode(memory[pos], 1)
    assert mode[0] == 0

    memory[memory[pos + 1]] = int(input())

    return memory, pos + 2, True


def execute_output(memory, pos):
    assert memory[pos] % 10 == 4
    mode = get_mode(memory[pos], 1)

    val = memory[memory[pos + 1]] if mode[0] == 0 else memory[pos + 1]
    print(val)

    return memory, pos + 2, True


def execute_jump_if_true(memory, pos):
    assert memory[pos] % 10 == 5
    mode = get_mode(memory[pos], 2)

    val = memory[memory[pos + 1]] if mode[0] == 0 else memory[pos + 1]
    target = memory[memory[pos + 2]] if mode[1] == 0 else memory[pos + 2]
    new_pos = target if val else pos + 3

    return memory, new_pos, True


def execute_jump_if_false(memory, pos):
    assert memory[pos] % 10 == 6
    mode = get_mode(memory[pos], 2)

    val = memory[memory[pos + 1]] if mode[0] == 0 else memory[pos + 1]
    target = memory[memory[pos + 2]] if mode[1] == 0 else memory[pos + 2]
    new_pos = target if not val else pos + 3

    return memory, new_pos, True


def execute_less_than(memory, pos):
    assert memory[pos] % 10 == 7
    mode = get_mode(memory[pos], 3)
    assert mode[2] == 0

    val_a = memory[memory[pos + 1]] if mode[0] == 0 else memory[pos + 1]
    val_b = memory[memory[pos + 2]] if mode[1] == 0 else memory[pos + 2]

    memory[memory[pos + 3]] = 1 if val_a < val_b else 0
    return memory, pos + 4, True


def execute_equals(memory, pos):
    assert memory[pos] % 10 == 8
    mode = get_mode(memory[pos], 3)
    assert mode[2] == 0

    val_a = memory[memory[pos + 1]] if mode[0] == 0 else memory[pos + 1]
    val_b = memory[memory[pos + 2]] if mode[1] == 0 else memory[pos + 2]

    memory[memory[pos + 3]] = 1 if val_a == val_b else 0
    return memory, pos + 4, True


def execute_end(memory, pos):
    return memory, pos, False


functions = {
    1: execute_add,
    2: execute_mult,
    3: execute_input,
    4: execute_output,
    5: execute_jump_if_true,
    6: execute_jump_if_false,
    7: execute_less_than,
    8: execute_equals,
    99: execute_end,
}


def execute(memory):
    memory, pos, cont = functions[memory[0]](memory, 0)
    while cont:
        memory, pos, cont = functions[memory[pos] % 100](memory, pos)
    return memory[0]


def main():
    memory = [int(v) for v in sys.stdin.readline().split(",")]
    print(execute(memory))


if __name__ == "__main__":
    main()
