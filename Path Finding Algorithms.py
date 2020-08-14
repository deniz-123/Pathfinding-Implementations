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
import Algorithms

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

    grid = Algorithms.make_grid(round(N_WIDTH))
    while run:
        Algorithms.draw(screen, grid, N_WIDTH)
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
                    Algorithms.a_star(start, end, lambda: Algorithms.draw(screen, grid, N_WIDTH), path_1, grid)
                    boolean_d = False
                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    Algorithms.dijsktra(start, end, lambda: Algorithms.draw(screen, grid, N_WIDTH), path_1, grid)
                    boolean_d = False
                if event.key == pygame.K_m and boolean_m:
                    Algorithms.maze_recursive(grid, lambda: Algorithms.draw(screen, grid, N_WIDTH))
                    boolean_m = False
                if event.key == pygame.K_p and boolean_p:
                    Algorithms.maze_prims(grid, lambda: Algorithms.draw(screen, grid, N_WIDTH))
                    boolean_p = False
                if event.key == pygame.K_r and boolean_r:
                    Algorithms.rand_obstacle(grid, lambda: Algorithms.draw(screen, grid, N_WIDTH))
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
                        Algorithms.draw(screen, grid, N_WIDTH)
                    grid = Algorithms.make_grid(round(N_WIDTH))
                    boolean_a = True
                    boolean_d = True
                    boolean_m = True
                    boolean_r = True
                    boolean_p = True
                    path_1 = []
        pygame.display.update()


main()
