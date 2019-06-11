#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from curses import color_pair
from random import randint

from src.conf import MAX_Y, MAX_X

__all__ = ['Food']


class Food:
    def __init__(self, window):
        self.coor = (randint(1, MAX_Y), randint(1, MAX_X))
        self.window = window

    def render(self):
        self.window.addstr(*self.coor, "█", color_pair(3))

    def renew(self):
        self.coor = (randint(1, MAX_Y), randint(1, MAX_X))
