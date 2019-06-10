#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from curses import color_pair
from random import randint


class Food:
    def __init__(self, max_y, max_x, window):
        self.max_y, self.max_x = max_y, max_x
        self.window = window
        self.coor = (randint(1, max_y), randint(1, max_x))

    def render(self):
        self.window.addstr(*self.coor, "█", color_pair(3))

    def renew(self):
        self.coor = (randint(1, self.max_y), randint(1, self.max_x))
