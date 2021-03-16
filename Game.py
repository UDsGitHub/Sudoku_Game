import pygame, sys, time
from Solver import*
from Generator import make_grid
from pygame.locals import *

pygame.init()

FPS = 60
clock = pygame.time.Clock()
win_size = (600, 600)
win_col = pygame.Color("white")
screen = pygame.display.set_mode(win_size)


class Grid:
    board = make_grid(20)

    def __init__(self, rows, cols, width, height):
        self.rows = rows  # depending on the num of rows or cols, draw rows or cols from 0, num not including num
        self.cols = cols
        self.width = width
        self.height = height
        self.cubes = [[Cube(self.board[i][j], i, j, self.width, self.height) for j in range(len(self.board[0]))] for i
                      in range(len(self.board))]
        self.selected = None
        self.model = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i
                      in range(self.rows)]

    def draw_grid(self, win):
        pygame.draw.rect(win, pygame.Color("black"), (pygame.Rect(30, 30, self.width, self.height)), 3)

        # drawing columns

        for i in range(0, self.cols):
            if i != 0 and i % 3 != 0:
                pygame.draw.line(win, pygame.Color("black"), (i * (self.width // self.cols) + 30, 30),
                                 (i * (self.width // self.cols) + 30, 570))
            else:
                pygame.draw.line(win, pygame.Color("black"), (i * (self.width // self.cols) + 30, 30),
                                 (i * (self.width // self.cols) + 30, 570), 3)

        # drawing rows

        for i in range(0, self.rows):
            if i != 0 and i % 3 != 0:
                pygame.draw.line(win, pygame.Color("black"), (30, i * (self.width // self.rows) + 30),
                                 (570, i * (self.width // self.rows) + 30))
            else:
                pygame.draw.line(win, pygame.Color("black"), (30, i * (self.width // self.rows) + 30),
                                 (570, i * (self.width // self.rows) + 30), 3)

        # drawing cubes

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.cubes[i][j].draw(win)

    def click(self, pos):

        if (30 < pos[0] < self.width + 30) and (30 < pos[1] < self.height + 30):
            gap = self.width // grid_res
            x = (pos[0] - 30) // gap
            y = (pos[1] - 30) // gap
            return (y, x)  # row, col
        else:
            return None

    def select(self, row, col):

        # deselect all others
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == self.cubes[row][col].value and self.cubes[row][col].value != 0 and self.cubes[i][j] != self.cubes[row][col]:
                    self.cubes[i][j].highlighted = True
                else:
                    self.cubes[i][j].highlighted = False
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def place(self, val):
        row, col = self.selected

        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.board, val, (row, col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False

        return True


class Cube:

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.temp = 0
        self.selected = False
        self.highlighted = False

    def draw(self, win):
        font = pygame.font.Font('freesansbold.ttf', 32)

        gap = self.width // grid_res
        x = gap * self.col + 50
        y = gap * self.row + 50

        if self.temp != 0 and self.value == 0:
            font = pygame.font.Font('freesansbold.ttf', 14)
            text = font.render(str(self.temp), True, pygame.Color("light gray"))
            win.blit(text, (x + 24, y - 12))
        elif not(self.value == 0):
            text = font.render(str(self.value), True, pygame.Color("black"))
            win.blit(text, (x, y))

        if self.selected:
            pygame.draw.rect(win, pygame.Color("red"), (pygame.Rect(x - 20, y - 20, gap, gap)), 3)
        if self.highlighted:
            pygame.draw.rect(win, pygame.Color("blue"), (pygame.Rect(x - 20, y - 20, gap, gap)), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    form_time = " " + str(minute) + ":" + str(sec)
    return form_time


def game_update(time):
    screen.fill(win_col)
    grid.draw_grid(screen)
    fnt = pygame.font.Font("freesansbold.ttf", 22)
    text = fnt.render(format_time(time), True, pygame.Color("black"))
    screen.blit(text, (win_size[0]-80, win_size[0]-28))
    clock.tick(FPS)
    pygame.display.update()


run = True
grid_res = 9
grid = Grid(grid_res, grid_res, 540, 540)
key = None
start = time.time()


while run:

    play_time = round(time.time()-start)

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_1:
                key = 1
            if event.key == K_2:
                key = 2
            if event.key == K_3:
                key = 3
            if event.key == K_4:
                key = 4
            if event.key == K_5:
                key = 5
            if event.key == K_6:
                key = 6
            if event.key == K_7:
                key = 7
            if event.key == K_8:
                key = 8
            if event.key == K_9:
                key = 9
            if event.key == K_RETURN:
                i, j = grid.selected
                if grid.cubes[i][j].temp != 0:
                    if grid.place(grid.cubes[i][j].temp):
                        print("Success")
                    else:
                        print("Wrong")
                    key = None

                    if grid.is_finished():
                        print("Game Over")
                        run = False

        if grid.selected and key != None:
            grid.sketch(key)

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = grid.click(mouse_pos)
                if clicked:
                    grid.select(clicked[0], clicked[1])
                    key = None
    game_update(play_time)
