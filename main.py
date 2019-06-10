from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, color_pair, endwin, newwin, start_color, initscr, noecho, \
    curs_set, init_pair
from random import randint

# Configuration
HEIGHT = 20
WIDTH = 35
MAX_Y = HEIGHT - 2
MAX_X = WIDTH - 2
TIMEOUT = 100
SNAKE_LENGTH = 6
SNAKE_X = SNAKE_LENGTH + 1
SNAKE_Y = 3
REV_DIR_MAP = {KEY_RIGHT: KEY_LEFT,
               KEY_LEFT: KEY_RIGHT,
               KEY_DOWN: KEY_UP,
               KEY_UP: KEY_DOWN}


class Food:
    def __init__(self, window):
        self.coor = (randint(1, MAX_Y), randint(1, MAX_X))
        self.window = window

    def render(self):
        self.window.addstr(*self.coor, "█", color_pair(3))

    def renew(self):
        self.coor = (randint(1, MAX_Y), randint(1, MAX_X))


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


class Snake(Body):
    def __init__(self, y, x, window):
        super().__init__(y, x, window)
        self.direction = KEY_RIGHT
        self.timeout = TIMEOUT
        self.hit_score = 0
        self.direction_map = {KEY_RIGHT: self.move_right,
                              KEY_LEFT: self.move_left,
                              KEY_DOWN: self.move_down,
                              KEY_UP: self.move_up}

        for i in range(SNAKE_LENGTH, 0, -1):
            self.add_body(y, x-i)

    def update(self):
        self.body_list.pop(0)
        self.add_body(*self.head_coor)
        self.last_head_coor = self.head_coor
        self.direction_map[self.direction]()

        return any([body == self.head_coor for body in self.body_list[:-1]])  # collided

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
        return 'Score : {}'.format(self.hit_score)


if __name__ == '__main__':
    try:
        initscr()
        start_color()
        curs_set(0)
        noecho()

        init_pair(1, 2, 0)  # Green
        init_pair(2, 3, 0)  # yellow
        init_pair(3, 1, 0)  # Red

        window = newwin(HEIGHT, WIDTH, 0, 0)
        window.timeout(TIMEOUT)
        window.keypad(1)
        window.border(0)

        snake = Snake(SNAKE_Y, SNAKE_X, window)
        food = Food(window)

        while True:
            window.clear()
            window.border(0)
            snake.render()
            food.render()

            window.addstr(0, 5, snake.score)
            event = window.getch()

            if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
                snake.change_direction(event)

            if snake.head_coor == food.coor:
                food.renew()
                snake.eat_food()

            if event == 32:
                key = -1
                while key != 32:
                    key = window.getch()

            if snake.update():
                break

        endwin()
        print(snake.score)

    except (KeyboardInterrupt, Exception) as e:
        endwin()
        print('\033[93m', e, '\033[0m \n')
