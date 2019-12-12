#!/usr/bin/env python3

import sys
from program import Program
import threading


class Robot:
    def __init__(self, program):
        self.__program = program
        self.__pos = (0, 0)
        self.__dir = (0, 1)
        self.__painted_zone = set()
        self.__white_zone = set([(0, 0)])

    def execute(self):
        self.__threads = [
            threading.Thread(target=self.__program.execute),
            threading.Thread(target=self.feed),
        ]

        for thread in self.__threads:
            thread.start()

        for thread in self.__threads:
            thread.join()

        print(len(self.__painted_zone))

    def print(self):
        x_range = (-10, 50)
        y_range = (-10, 5)

        for y in range(y_range[1], y_range[0] - 1, -1):
            for x in range(x_range[0], x_range[1] + 1):
                pos = (x, y)
                value = "."
                if pos == self.__pos:
                    if self.__dir == (1, 0):
                        value = ">"
                    elif self.__dir == (0, 1):
                        value = "^"
                    elif self.__dir == (-1, 0):
                        value = "<"
                    else:
                        value = "v"
                elif pos in self.__white_zone:
                    value = "#"
                print(value, end="")
            print("")
        print("====================")

    def action(self):
        self.print()
        color = 0
        if self.__pos in self.__white_zone:
            color = 1
        print("send", color)
        self.__program.send_input(color)
        action = next(self.__program)
        rotation = next(self.__program)

        if action == 1:
            self.__white_zone.add(self.__pos)
            print("paint it white")
        else:
            self.__white_zone.discard(self.__pos)
        self.__painted_zone.add(self.__pos)

        self.update_direction(rotation)
        self.move()

    def move(self):
        print("move from ", self.__pos, "with", self.__dir, end="")
        self.__pos = (self.__pos[0] + self.__dir[0], self.__pos[1] + self.__dir[1])
        print("to", self.__pos)

    def update_direction(self, rotation):
        if rotation == 0:  # Turn 90 left
            print("Turn left", self.__pos, self.__dir)
            if self.__dir == (1, 0):
                self.__dir = (0, 1)
            elif self.__dir == (0, 1):
                self.__dir = (-1, 0)
            elif self.__dir == (-1, 0):
                self.__dir = (0, -1)
            else:
                self.__dir = (1, 0)
        else:  # Turn 90 right
            print("Turn right", self.__pos, self.__dir)
            if self.__dir == (1, 0):
                self.__dir = (0, -1)
            elif self.__dir == (0, -1):
                self.__dir = (-1, 0)
            elif self.__dir == (-1, 0):
                self.__dir = (0, 1)
            else:
                self.__dir = (1, 0)

    def feed(self):
        while self.__program.is_running():
            self.action()


def main():
    data = sys.stdin.readline()
    r = Robot(Program(data, 1))
    r.execute()


if __name__ == "__main__":
    main()
