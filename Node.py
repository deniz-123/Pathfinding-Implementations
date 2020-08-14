"""
The Node object for Path Finding Algorithms
"""

import pygame
import math

# colors
Black = 0, 0, 0
Blue = 0, 0, 255
Grown = 105, 105, 10
Green = 0, 255, 0
Grey = 128, 128, 128
Purple = 128, 0, 128
Pink = 250, 100, 250
Red = 255, 0, 0
Turquoise = 64, 224, 208
Orange = 255, 165, 0
White = 255, 255, 255
Yellow = 255, 255, 0

# init pygame
WIDTH = 1185
HEIGHT = 885
N_WIDTH = 15
T_ROWS = WIDTH / N_WIDTH
T_COLS = HEIGHT / N_WIDTH
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(Black)
clock = pygame.time.Clock()

# var
grid = None

class Node():
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.g = math.inf
        self.h = math.inf
        self.f = self.g + self.h
        self.color = White
        self.neighbors = []
        self.maze_neighbors = []
        self.width = width
        self.t_rows = WIDTH / width
        self.t_cols = HEIGHT / width
        self.previous = None
        self.maze_visited = False
        self.visited_cell = True

    def __str__(self):
        return "I am {} - {}".format(self.col, self.row)

    def get_neighbors(self):
        return self.neighbors

    def get_maze_neighbors(self):
        return self.maze_neighbors

    def set_color(self, color):
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == Black

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.col < self.t_cols - 1 and not grid[self.row][self.col + 1].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # UP
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.row < self.t_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row - 1][self.col])

    def update_maze_neighbors(self, grid):
        self.maze_neighbors = []
        if self.col < self.t_cols - 2 and not grid[self.row][self.col + 2].visited_cell:  # DOWN
            self.maze_neighbors.append(grid[self.row][self.col + 2])

        if self.col > 1 and not grid[self.row][self.col - 2].visited_cell:  # UP
            self.maze_neighbors.append(grid[self.row][self.col - 2])

        if self.row < self.t_rows - 2 and not grid[self.row + 2][self.col].visited_cell:  # RIGHT
            self.maze_neighbors.append(grid[self.row + 2][self.col])

        if self.row > 1 and not grid[self.row - 2][self.col].visited_cell:  # LEFT
            self.maze_neighbors.append(grid[self.row - 2][self.col])
