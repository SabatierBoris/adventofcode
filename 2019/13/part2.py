#!/usr/bin/env python3

import sys
from program import Program
from game import Game
import threading
import os
from time import sleep


SLEEP_DURATION = 0.01


def play(game):
    while True:
        game.update_state()
        os.system("clear")
        game.display()
        if not game.is_running():
            break
        ball = game.get_ball_pos()
        cursor = game.get_cursor_pos()
        print(ball)
        print(cursor)
        if ball[0] > cursor[0]:
            print("Move right")
            game.move_right()
        elif ball[0] < cursor[0]:
            print("Move left")
            game.move_left()
        else:
            print("Dont move")
            game.dont_move()

        sleep(SLEEP_DURATION)


def main():
    data = sys.stdin.readline()
    g = Game(Program(data, 1))
    threads = [
        threading.Thread(target=g.execute),
        threading.Thread(target=lambda: play(g)),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
