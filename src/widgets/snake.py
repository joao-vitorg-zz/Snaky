#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP

from src.conf import TIMEOUT, SNAKE_Y, SNAKE_X, SNAKE_LENGTH, MAX_X, MAX_Y
from src.widgets import Body

__all__ = ['Snake']

REV_DIR_MAP = {KEY_RIGHT: KEY_LEFT,
               KEY_LEFT: KEY_RIGHT,
               KEY_DOWN: KEY_UP,
               KEY_UP: KEY_DOWN}


class Snake(Body):
    def __init__(self, window):
        super().__init__(window)
        self.direction = KEY_RIGHT
        self.timeout = TIMEOUT
        self.hit_score = 0
        self.direction_map = {KEY_RIGHT: self.move_right,
                              KEY_LEFT: self.move_left,
                              KEY_DOWN: self.move_down,
                              KEY_UP: self.move_up}

        for i in range(1, SNAKE_LENGTH):
            self.add_body(SNAKE_Y, SNAKE_X - i)

    def update(self):
        self.body_list.pop(-1)
        self.body_list.insert(0, self.head_coor)
        self.last_head_coor = self.head_coor
        self.direction_map[self.direction]()

        return any([tuple(body) == self.head_coor for body in self.body_list])

    def eat_food(self):
        self.add_body(*self.last_head_coor)
        self.hit_score += 1
        if self.hit_score % 3 == 0:
            self.timeout -= 5
            self.window.timeout(self.timeout)

    def change_direction(self, direction):
        if direction != REV_DIR_MAP[self.direction]:
            self.direction = direction

    def move_up(self):
        self.head_y -= 1
        if self.head_y < 1:
            self.head_y = MAX_Y

    def move_down(self):
        self.head_y += 1
        if self.head_y > MAX_Y:
            self.head_y = 1

    def move_left(self):
        self.head_x -= 1
        if self.head_x < 1:
            self.head_x = MAX_X

    def move_right(self):
        self.head_x += 1
        if self.head_x > MAX_X:
            self.head_x = 1

    @property
    def score(self):
        return 'Score: {}'.format(self.hit_score)
