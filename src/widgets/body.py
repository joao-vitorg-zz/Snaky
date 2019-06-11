#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from curses import color_pair

from src import SNAKE_Y, SNAKE_X

__all__ = ['Body']


class Body:
    def __init__(self, window):
        self.window = window
        self.body_list = []

        # Head
        self.last_head_coor = (SNAKE_Y, SNAKE_X)
        self.head_y = SNAKE_Y
        self.head_x = SNAKE_X

    def render(self):
        self.window.addstr(*self.head_coor, '█', color_pair(2))  # Head
        for body in self.body_list:
            self.window.addstr(*body, '█', color_pair(1))  # Body

    def add_body(self, y, x):
        self.body_list.append([y, x])

    @property
    def head_coor(self):
        return self.head_y, self.head_x
