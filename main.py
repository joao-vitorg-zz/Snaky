#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, endwin, newwin, start_color, initscr, noecho, curs_set, \
    init_pair

from src.conf import HEIGHT, WIDTH, TIMEOUT
from src.widgets import *


class SnakyGame:
    def __init__(self):
        self.init_courses()

        self.window = newwin(HEIGHT, WIDTH, 0, 0)
        self.window.timeout(TIMEOUT)
        self.window.keypad(1)

        self.snake = Snake(self.window)
        self.food = Food(self.window)
        self.main_loop()

    @staticmethod
    def init_courses():
        initscr()
        start_color()
        curs_set(0)
        noecho()

        init_pair(1, 2, 0)  # Green
        init_pair(2, 3, 0)  # yellow
        init_pair(3, 1, 0)  # Red

    def render(self):
        self.window.clear()
        self.window.border(0)
        self.snake.render()
        self.food.render()

        # window.addstr(0, 0, str([snake.head_coor]+[body for body in snake.body_list]))
        self.window.addstr(0, 13, self.snake.score)

    def main_loop(self):
        try:
            while not self.snake.collided:
                self.render()

                event = self.window.getch()

                if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
                    self.snake.change_direction(event)
                if event == 32:
                    self.pause()
                if self.snake.head_coor == self.food.coor:
                    self.eat()

                self.snake.update()

            endwin()
            print(self.snake.score)

        except (KeyboardInterrupt, Exception) as e:
            endwin()
            print('\033[93m', e, '\033[0m \n\n')
            print(self.snake.score)

    def pause(self):
        key = -1
        while key != 32:
            key = self.window.getch()

    def eat(self):
        self.snake.eat_food()
        self.food.renew()


if __name__ == '__main__':
    SnakyGame()
