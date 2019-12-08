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
                assert modes[nb_inputs] == 0

            args = []
            for i in range(nb_inputs):
                memory_pos = pos + 1 + i
                args.append(
                    memory[memory[memory_pos]] if modes[i] == 0 else memory[memory_pos]
                )

            logging.debug(
                "%s - %s(%s) => ",
                memory[pos : pos + 1 + nb_inputs + as_output],
                f.__name__,
                ", ".join([str(i) for i in args]),
            )
            result = f(self, *args)

            logging.debug(result)
            if as_output:
                memory[memory[pos + nb_inputs + as_output]] = result

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
    def __init__(self, name, data):
        self.__name = name
        self.__initial_memory = [int(v) for v in data.split(",")]
        self.__memory = list(self.__initial_memory)
        self.__pos = 0
        self.__running = True
        self.__input = Queue(1)
        self.__output = Queue(1)

    def reset(self):
        self.__running = True
        self.__memory = list(self.__initial_memory)

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
        value = self.__input.get()
        # print("%s input %s" % (self.__name, value))
        self.__input.task_done()
        return value

    @instruction(4, 1, False)
    def output(self, value):
        # print("%s output %s" % (self.__name, value))
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

    @instruction(99, 0, False)
    def halt(self):
        # print("%s is halted" % (self.__name))
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
        while self.__running:
            try:
                value = self.__output.get(timeout=1)
                self.__output.task_done()
                return value
            except Empty:
                # print("no output data")
                continue
        if self.__output.empty():
            raise StopIteration
        value = self.__output.get()
        self.__output.task_done()
        return value


def process_amps(data, config):
    amps = [Program(data) for _ in range(len(config))]

    prev_value = 0
    for i in range(len(config)):
        amps[i].send_input(config[i])
        amps[i].send_input(prev_value)
        amps[i].execute()
        prev_value = next(amps[i])

    return prev_value


def process_part1(data):
    results = []

    for config in itertools.permutations(range(5), 5):
        result = process_amps(data, config)
        # print(config, result)
        results.append(result)

    return max(results)


def process_looped_amps(data, config):
    amps = [Program(str(i), data) for i in range(len(config))]

    for i in range(len(config)):
        amps[i].send_input(config[i])

    threads = [threading.Thread(target=amp.execute) for amp in amps]
    threads.append(threading.Thread(target=amps[0].send_input, args=(0,)))

    result = 0

    def connect_amps(src, dst):
        nonlocal result
        for data in src:
            # print(src._Program__name, data, " to ", dst._Program__name)
            try:
                dst.send_input(data)
            except StopIteration:
                result = data

    src = amps[-1]
    for dst in amps:
        threads.append(threading.Thread(target=connect_amps, args=(src, dst)))
        src = dst

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return result


def process_part2(data):
    results = []

    for config in itertools.permutations(range(5, 10), 5):
        # print(config)
        result = process_looped_amps(data, config)
        results.append(result)

    return max(results)
