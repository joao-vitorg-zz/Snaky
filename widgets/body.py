#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from curses import color_pair


class Body:
    def __init__(self, y, x, window):
        self.window = window
        self.body_list = []

        # Head
        self.last_head_coor = (y, x)
        self.head_y = y
        self.head_x = x

    def render(self):
        self.window.addstr(*self.head_coor, '█', color_pair(2))  # Head
        for body in self.body_list:
            self.window.addstr(*body, '█', color_pair(1))  # Body

    def add_body(self, y, x):
        self.body_list.append([y, x])

    @property
    def head_coor(self):
        return self.head_y, self.head_x
