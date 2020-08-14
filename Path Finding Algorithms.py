"""
@Author Deniz Berkant Demirörs
@Date 08/08/2020
@Version 1.0.4
Using A* and Dijkstra's algorithm to find the shortest path between two or more spots and barriers
Creating a random maze using Recursive Backtracker and Prim's algorithms and solving them with A* and Dijkstra
@Keys
Clear = c
Maze Recursive = m
Maze Prim's = p
Random Obstacles = r
A* Algorithm = a
Dijkstra's Algorithm = d
Start = Mouse Left Click
End Spots = Mouse Right Click(can be multiple)
Obstacles = Middle button of mouse
Weighted Spots = After putting start node use Mouse Left Click to put
"""

import pygame
import math
import random
import time
from copy import *
from queue import *

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
WIDTH = 1180
HEIGHT = 900
N_WIDTH = 20
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


def make_grid(gap):
    grid = []
    rows = WIDTH // N_WIDTH
    column = HEIGHT // N_WIDTH
    for i in range(int(rows)):
        grid.append([])
        for j in range(int(column)):
            node = Node(i, j, gap)
            grid[i].append(node)
    return grid


def draw_grid(win, gap):
    rows = WIDTH // gap
    column = HEIGHT // gap
    for i in range(int(rows)):
        pygame.draw.line(win, Grey, (i * gap, 0), (i * gap, HEIGHT))
        for j in range(int(column)):
            pygame.draw.line(win, Grey, (0, j * gap), (WIDTH, j * gap))


def draw(win, grid, gap):
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, gap)
    pygame.display.update()


def heuristic(n1, n2):
    x1, y1 = n1.get_pos()
    x2, y2 = n2.get_pos()
    return abs(x1 - x2) + abs(y1 - y2)


def rand_obstacle(grid, draw):
    for row in grid:
        for node in row:
            node.update_neighbors(grid)
            neighbors_a = node.get_neighbors()
            if node.col % 2 == 0 and node.maze_visited == False:
                j = random.randrange(len(neighbors_a))
                if not neighbors_a[j].maze_visited:
                    neighbors_a[j].set_color(Black)
                neighbors_a[j].maze_visited = True
    draw()


def maze_prims(grid, draw):
    # variables
    cell = []
    maze = []

    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    for i in range(round(T_ROWS)):
        for j in range(round(T_COLS)):
            if i == 0 or i == T_ROWS - 1:
                grid[i][j].set_color(Black)
            elif j == 0 or j == T_COLS - 1:
                grid[i][j].set_color(Black)
            elif i % 2 == 0:
                grid[i][j].set_color(Black)
            elif j % 2 == 0:
                grid[i][j].set_color(Black)
            else:
                grid[i][j].set_color(Black)
                grid[i][j].visited_cell = False
                cell.append(grid[i][j])
        draw()

    for row in grid:
        for node in row:
            node.update_maze_neighbors(grid)

    i = random.randint(0, len(cell) - 1)

    c_tmp = Node(1, 1, 1)
    back = None
    maze.append(cell[i])

    while maze:
        clock.tick(10000000)
        for row in grid:
            for node in row:
                node.update_maze_neighbors(grid)
        back = back

        if len(maze) > 0:
            j = random.randint(0, len(maze) - 1)
            current = maze[j]
            current.set_color(White)
            tmp_color = current.previous
            if tmp_color:
                for neighbor in current.get_neighbors():
                    if neighbor in tmp_color.get_neighbors():
                        neighbor.set_color(White)
                if tmp_color in maze:
                    maze.remove(tmp_color)
            draw()
        elif len(maze) == 1:
            j = 0
            current = maze[j]

        if current in maze:
            maze.remove(current)
        current.visited_cell = True
        random.shuffle(current.get_maze_neighbors())

        if current.get_maze_neighbors():
            for item in current.get_maze_neighbors():
                if not item.visited_cell:
                    for neighbor in current.get_neighbors():
                        if neighbor in item.get_neighbors():
                            item.set_color(White)
                            neighbor.set_color(White)
                            item.visited_cell = True
                            item.previous = current
                            c_tmp = item
                            back = True
                            break
                if back:
                    break

            for element in current.get_maze_neighbors():
                if not element.visited_cell:
                    element.previous = current
                    maze.append(element)
                    element.set_color(Blue)

        if c_tmp.get_maze_neighbors():
            for element in c_tmp.get_maze_neighbors():
                if not element.visited_cell:
                    element.previous = c_tmp
                    if element.color != Blue:
                        maze.append(element)
                        element.set_color(Blue)

        back = False
        draw()
    for row in grid:
        for node in row:
            node.previous = None


def maze_recursive(grid, draw):
    # variables
    cell = []
    stack = []

    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    for i in range(round(T_ROWS)):
        for j in range(round(T_COLS)):
            if i == 0 or i == T_ROWS - 1:
                grid[i][j].set_color(Black)
            elif j == 0 or j == T_COLS - 1:
                grid[i][j].set_color(Black)
            elif i % 2 == 0:
                grid[i][j].set_color(Black)
            elif j % 2 == 0:
                grid[i][j].set_color(Black)
            else:
                grid[i][j].set_color(Black)
                grid[i][j].visited_cell = False
                cell.append(grid[i][j])
        draw()
    for row in grid:
        for node in row:
            node.update_maze_neighbors(grid)

    current = cell[0]
    current.visited_cell = True

    while cell:
        clock.tick(20000000)
        for row in grid:
            for node in row:
                node.update_maze_neighbors(grid)

        current = current
        current.visited_cell = True
        maze_neighbors_tmp = current.get_maze_neighbors()

        if maze_neighbors_tmp:
            if len(maze_neighbors_tmp) > 1:
                i = random.randint(0, len(current.get_maze_neighbors()) - 1)
                chosen = current.get_maze_neighbors()[i]
                chosen.set_color(Pink)
                current.set_color(Yellow)
                stack.append(current)
            elif len(maze_neighbors_tmp) == 1:
                chosen = current.get_maze_neighbors()[0]
                chosen.set_color(Pink)
                current.set_color(Yellow)
                stack.append(current)

            for neighbor in current.get_neighbors():
                if neighbor in chosen.get_neighbors():
                    if current in stack:
                        neighbor.set_color(Yellow)
                        neighbor.maze_visited = True
                    break

            if chosen in cell:
                cell.remove(chosen)
            current = chosen

        elif stack:
            current.set_color(White)
            for neighbor in current.get_neighbors():
                if neighbor.maze_visited:
                    neighbor.set_color(White)
            current = stack[len(stack) - 1]
            current.set_color(Pink)
            stack.remove(current)

        if not stack:
            current.set_color(White)
            cell.remove(current)
        draw()


def dijsktra(start, end, draw, path_1, grid):
    open_set = [start]
    path = path_1
    start.g = 0
    start.h = heuristic(start, end[0])
    algorithm = True

    while algorithm:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if not open_set:
            break
        if len(open_set) < 2:
            current = open_set[0]
            open_set.remove(current)
        else:
            current = open_set[0]
            open_set.remove(current)
            tmp = open_set[0]
            if current.g > tmp.g:
                open_set.append(current)
                current = open_set[0]
                open_set.remove(current)

        for neighbor in current.get_neighbors():
            temp_g = current.g + 1

            if temp_g < neighbor.g:
                neighbor.previous = current
                if neighbor.color == Yellow or neighbor.color == Pink:
                    neighbor.g = temp_g + 10
                else:
                    neighbor.g = temp_g
                if neighbor not in open_set:
                    open_set.append(neighbor)
                    if neighbor.color != Orange and neighbor.color != Yellow and neighbor.color != Turquoise and neighbor.color != Pink:
                        neighbor.set_color(Green)
                    elif neighbor.color == Yellow:
                        neighbor.set_color(Pink)

        if current.color != Orange and current.color != Turquoise and current.color != Pink:
            current.set_color(Red)

        if current == end[0] and len(end) > 1:
            start = end[0]
            end.pop(0)
            temp = current
            path.append(current)
            while temp.previous:
                path.append(temp)
                temp = temp.previous
            for row in grid:
                for node in row:
                    node.g = math.inf
                    node.previous = None
            dijsktra(start, end, draw, path, grid)
            break
        elif current == end[0] and len(end) == 1:
            end.pop(0)
            temp = current
            temp_path = [current]
            while temp.previous:
                temp_path.append(temp)
                temp = temp.previous
            path.extend(temp_path)
            for i in range(2, len(path)):
                if path[i].color != Orange and path[i].color != Turquoise:
                    path[i].set_color(Purple)
                elif path[i].color == Turquoise:
                    path[i].set_color(Grown)
                draw()
            algorithm = False
        draw()


def a_star(start, end, draw, path_1, grid):
    open_set = [start]
    count = 0
    open_set_prio = PriorityQueue()
    open_set_prio.put((0, count, start))
    path = path_1
    start.g = 0
    start.h = heuristic(start, end[0])
    algorithm = True

    while algorithm:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if open_set_prio.empty():
            break
        current = open_set_prio.get()[2]
        open_set.remove(current)

        for neighbor in current.get_neighbors():
            temp_g = current.g + 1

            if temp_g < neighbor.g:
                neighbor.previous = current
                neighbor.g = temp_g
                neighbor.h = heuristic(neighbor, end[0])
                if neighbor.color == Yellow or neighbor.color == Pink:
                    neighbor.f = neighbor.g + neighbor.h + 10
                else:
                    neighbor.f = neighbor.g + neighbor.h
                if neighbor not in open_set:
                    count += 1
                    open_set_prio.put((neighbor.f, count, neighbor))
                    open_set.append(neighbor)
                    if neighbor.color != Orange and neighbor.color != Yellow and neighbor.color != Turquoise and neighbor.color != Pink:
                        neighbor.set_color(Green)
                    elif neighbor.color == Yellow:
                        neighbor.set_color(Pink)

        if current.color != Orange and current.color != Turquoise and current.color != Pink:
            current.set_color(Red)

        if current == end[0] and len(end) > 1:
            start = end[0]
            end.pop(0)
            temp = current
            path.append(current)
            while temp.previous:
                path.append(temp)
                temp = temp.previous
            for row in grid:
                for node in row:
                    node.g = math.inf
                    node.h = math.inf
                    node.previous = None
            a_star(start, end, draw, path, grid)
            break
        elif current == end[0] and len(end) == 1:
            end.pop(0)
            temp = current
            temp_path = [current]
            while temp.previous:
                temp_path.append(temp)
                temp = temp.previous
            path.extend(temp_path)
            for i in range(2, len(path)):
                if path[i].color != Orange and path[i].color != Turquoise:
                    path[i].set_color(Purple)
                elif path[i].color == Turquoise:
                    path[i].set_color(Grown)
                draw()
            algorithm = False
        draw()


def main():
    # variables
    boolean_a = True
    boolean_d = True
    boolean_m = True
    boolean_r = True
    boolean_p = True
    start = None
    end = []
    run = True
    path_1 = []
    rows = WIDTH // N_WIDTH
    column = HEIGHT // N_WIDTH

    grid = make_grid(round(N_WIDTH))
    while run:
        draw(screen, grid, N_WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            mx, my = pygame.mouse.get_pos()
            m_x_i = mx // N_WIDTH
            m_x_j = my // N_WIDTH

            if boolean_a and pygame.mouse.get_pressed()[0]:
                if grid[int(m_x_i)][int(m_x_j)].color == White:
                    grid[int(m_x_i)][int(m_x_j)].set_color(Turquoise)
                    start = grid[int(m_x_i)][int(m_x_j)]
                    boolean_a = False
            elif not boolean_a and pygame.mouse.get_pressed()[0]:
                if grid[int(m_x_i)][int(m_x_j)].color == White:
                    grid[int(m_x_i)][int(m_x_j)].set_color(Yellow)
            if pygame.mouse.get_pressed()[1]:
                if grid[int(m_x_i)][int(m_x_j)].color == White:
                    grid[int(m_x_i)][int(m_x_j)].set_color(Black)
            if boolean_d and pygame.mouse.get_pressed()[2]:
                if grid[int(m_x_i)][int(m_x_j)].color == White:
                    grid[int(m_x_i)][int(m_x_j)].set_color(Orange)
                    end.append(grid[int(m_x_i)][int(m_x_j)])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star(start, end, lambda: draw(screen, grid, N_WIDTH), path_1, grid)
                    boolean_d = False
                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    dijsktra(start, end, lambda: draw(screen, grid, N_WIDTH), path_1, grid)
                    boolean_d = False
                if event.key == pygame.K_m and boolean_m:
                    maze_recursive(grid, lambda: draw(screen, grid, N_WIDTH))
                    boolean_m = False
                if event.key == pygame.K_p and boolean_p:
                    maze_prims(grid, lambda: draw(screen, grid, N_WIDTH))
                    boolean_p = False
                if event.key == pygame.K_r and boolean_r:
                    rand_obstacle(grid, lambda: draw(screen, grid, N_WIDTH))
                    boolean_r = False
                if event.key == pygame.K_c:
                    start = None
                    end = []
                    for i in range(int(rows)):
                        for j in range(int(column)):
                            if 0 < i < int(rows) - 1:
                                grid[i][j].set_color(Black)
                                grid[i + 1][j].set_color(Black)
                                grid[i - 1][j].set_color(White)
                            elif i == 0:
                                grid[i][j].set_color(Black)
                            elif i == int(rows):
                                grid[i][j].set_color(White)
                        # clock.tick(15)
                        draw(screen, grid, N_WIDTH)
                    grid = make_grid(round(N_WIDTH))
                    boolean_a = True
                    boolean_d = True
                    boolean_m = True
                    boolean_r = True
                    boolean_p = True
                    path_1 = []
        pygame.display.update()


main()
