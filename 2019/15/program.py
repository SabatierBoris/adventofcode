import itertools
from time import sleep
import threading
from queue import Queue, Empty
import logging


def instruction(code, nb_inputs, as_output, can_jump=False):
    def __instruction(f):
        def wrapper(self, memory, pos):
            assert memory[pos] % 100 == code

            modes = self.get_mode(memory[pos], nb_inputs + as_output)
            if as_output:
                assert modes[nb_inputs] != 1, "Error pos : %s value : %s" % (
                    pos,
                    memory[pos],
                )

            args = []
            for i in range(nb_inputs):
                args.append(self.get_value(pos + 1 + i, modes[i]))

            result = f(self, *args)

            if as_output:
                target_pos = self.get_target_position(
                    pos + nb_inputs + as_output, modes[nb_inputs]
                )
                while len(memory) <= target_pos:
                    memory.append(0)
                memory[target_pos] = result

            new_pos = pos + 1 + nb_inputs + as_output

            if can_jump and result is not None:
                new_pos = result

            return memory, new_pos

        wrapper._instruction_code = code

        return wrapper

    return __instruction


def class_register(cls):
    cls._instructions = {}
    for methodname in dir(cls):
        method = getattr(cls, methodname)
        if hasattr(method, "_instruction_code"):
            cls._instructions[method._instruction_code] = method
    return cls


@class_register
class Program:
    def __init__(self, data, queue_size=0):
        self.__initial_memory = [int(v) for v in data.split(",")]
        self.__memory = list(self.__initial_memory)
        self.__pos = 0
        self.__running = True
        self.__input = Queue(queue_size)
        self.__output = Queue(queue_size)
        self.__base = 0
        self.__input_needed = False

    def reset(self):
        self.__running = True
        self.__memory = list(self.__initial_memory)

    def get_value(self, position, mode):
        pos = self.get_target_position(position, mode)
        while len(self.__memory) <= pos:
            self.__memory.append(0)
        return self.__memory[pos]

    def get_target_position(self, position, mode):
        if mode == 0:
            return self.__memory[position]
        elif mode == 1:
            return position
        elif mode == 2:
            return self.__base + self.__memory[position]
        else:
            raise AssertionError("Unhandled mode %s" % mode)

    @staticmethod
    def get_mode(value, nb_params):
        mode = []
        value //= 100
        for _ in range(nb_params):
            mode.append(value % 10)
            value //= 10
        return mode

    @instruction(1, 2, True)
    def add(self, a, b):
        return a + b

    @instruction(2, 2, True)
    def mult(self, a, b):
        return a * b

    @instruction(3, 0, True)
    def input(self):
        self.__input_needed = True
        value = self.__input.get()
        self.__input_needed = False
        self.__input.task_done()
        return value

    @instruction(4, 1, False)
    def output(self, value):
        self.__output.put(value)

    @instruction(5, 2, False, True)
    def jump_if_true(self, val, target):
        return target if val else None

    @instruction(6, 2, False, True)
    def jump_if_false(self, val, target):
        return target if not val else None

    @instruction(7, 2, True)
    def less_than(self, a, b):
        return 1 if a < b else 0

    @instruction(8, 2, True)
    def equals(self, a, b):
        return 1 if a == b else 0

    @instruction(9, 1, False)
    def update_base(self, offset):
        self.__base += offset

    @instruction(99, 0, False)
    def halt(self):
        self.__running = False

    def send_input(self, value):
        if not self.__running:
            raise StopIteration
        self.__input.put(value)

    def step(self):
        current_action = self.__memory[self.__pos] % 100

        assert current_action in self._instructions, (
            "%s isn't valide instruction" % current_action
        )

        self.__memory, self.__pos = self._instructions[current_action](
            self, self.__memory, self.__pos
        )

    def execute(self):
        while self.__running:
            self.step()

    def __iter__(self):
        return self

    def __next__(self):
        while self.__running and not self.__input_needed:
            try:
                value = self.__output.get(timeout=1)
                self.__output.task_done()
                return value
            except Empty:
                continue
        if self.__output.empty():
            raise StopIteration
        value = self.__output.get()
        self.__output.task_done()
        return value

    def is_running(self):
        return self.__running
