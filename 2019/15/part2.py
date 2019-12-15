#!/usr/bin/env python3

import sys
import os
import threading
from time import sleep

from program import Program
from droid import Droid

SLEEP_DURATION = 0.0001


def play(d):
    while d.is_running():
        os.system("clear")
        d.display()
        if not d.explore():
            break
        sleep(SLEEP_DURATION)
        d.read_sensor()

    d.init_oxygen()
    i = 0
    while d.expand_oxygen():
        i += 1
        os.system("clear")
        d.display()
        sleep(SLEEP_DURATION)
    print(i)


def main():
    data = sys.stdin.readline()
    d = Droid(Program(data))

    threads = [
        threading.Thread(target=d.execute),
        threading.Thread(target=lambda: play(d)),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
