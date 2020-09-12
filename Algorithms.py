"""
Using Node class visualizing bunch of algorithms
"""

import pygame
import math
import random
from Pygame_version import Node
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


def make_grid(gap):
    grid = []
    rows = WIDTH // N_WIDTH
    column = HEIGHT // N_WIDTH
    for i in range(int(rows)):
        grid.append([])
        for j in range(int(column)):
            node = Node.Node(i, j, gap)
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


def maze_kruskals(grid, draw):
    # variables
    cell = []
    stack = []
    kruskal_no = 1

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
                grid[i][j].kruskal = kruskal_no
                cell.append(grid[i][j])
                kruskal_no += 1
        draw()
    for row in grid:
        for node in row:
            node.update_maze_neighbors(grid)
            node.kruskal_neighbors = node.maze_neighbors
    random.shuffle(cell)
    current = cell[0]
    number = current.kruskal
    algorithm = True
    count = 0
    while algorithm:

        loop2 = True
        algorithm = False
        for item in cell:
            item.update_kruskal_neighbors
            if len(item.kruskal_neighbors) == 0:
                cell.remove(item)
            if item.kruskal != number:
                algorithm = True
        if not algorithm:
            break

        maze_neighbors_tmp = current.get_maze_neighbors()
        random.shuffle(maze_neighbors_tmp)
        chosen = maze_neighbors_tmp[0]

        if current.kruskal != chosen.kruskal:
            for neighbor in current.get_neighbors():
                if neighbor in chosen.get_neighbors():
                    current.set_color(White)
                    chosen.set_color(White)
                    tmp_kruskal = chosen.kruskal
                    chosen.kruskal = current.kruskal
                    neighbor.set_color(White)

        for node in cell:
            if node.kruskal == tmp_kruskal:
                node.kruskal = chosen.kruskal

        random.shuffle(cell)
        number = current.kruskal
        if cell:
            current = cell[0]
        else:
            algorithm = False
        draw()


def hunt_kill(grid, draw):
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

    random.shuffle(cell)
    current = cell[0]
    stack.append(current)

    while stack:
        clock.tick(222222)
        for row in grid:
            for node in row:
                node.update_maze_neighbors(grid)

        current = current
        stack.remove(current)
        current.visited_cell = True
        current.set_color(White)
        random.shuffle(current.get_maze_neighbors())
        maze_neighbors_tmp = current.get_maze_neighbors()

        if maze_neighbors_tmp:
            if len(maze_neighbors_tmp) > 1:
                i = random.randint(0, len(current.get_maze_neighbors()) - 1)
                chosen = current.get_maze_neighbors()[i]
                stack.append(chosen)
            elif len(maze_neighbors_tmp) == 1:
                chosen = maze_neighbors_tmp[0]
                stack.append(chosen)

            for neighbor in current.get_neighbors():
                if neighbor in chosen.get_neighbors():
                    neighbor.set_color(White)
                    break
            current = chosen
        else:
            i = 1
            j = 1
            while True:
                if grid[i][j].visited_cell and grid[i][j].get_maze_neighbors():
                    current = grid[i][j]
                    if current.color != White:
                        current.set_color(Green)
                    stack.append(current)
                    break
                if i == T_ROWS - 2:
                    """if grid[i - 2][j].color != White:
                        grid[int(T_ROWS -2)][j].set_color(Black)"""
                    j += 2
                    i = 1
                    """if grid[i][j].color == Black and grid[i][j].color != White:
                        grid[i][j].set_color(Green)
                    if grid[i - 2][j - 2].color != White:
                        grid[i][j].set_color(Black)"""
                elif i != T_ROWS - 2 and j != T_COLS - 2:
                    i += 2
                    """if grid[i][j].color == Black and grid[i][j].color != White:
                        grid[i][j].set_color(Green)
                    if grid[i - 2][j].color != White:
                        grid[i - 2][j].set_color(Black)"""
                else:
                    break
                #draw()
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
        clock.tick(15)
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


def dfs(start, end, draw, path_1, grid):
    # update neighbors
    for row in grid:
        for node in row:
            node.update_neighbors(grid)
    # variables
    stack = [start]
    current = stack[0]
    path = path_1

    while stack:
        current = current
        stack.remove(current)
        current.maze_visited = True
        for neighbor in current.get_neighbors():
            if not neighbor.maze_visited:
                neighbor.previous = current
                stack.append(neighbor)
                if neighbor.color != Orange and neighbor.color != Turquoise:
                    neighbor.set_color(Green)
        if current.color != Orange and current.color != Turquoise:
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
                    node.previous = None
                    node.maze_visited = False
            dfs(start, end, draw, path_1, grid)
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
            break
        if stack:
            current = stack[len(stack) - 1]
        draw()
    draw()


def bfs(start, end, draw, path_1, grid):
    # update neighbors
    for row in grid:
        for node in row:
            node.update_neighbors(grid)
            node.maze_visited = False
    # variables
    open_set = [start]
    path = path_1
    algorithm = True

    while algorithm:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if not open_set:
            break
        current = open_set[0]
        current.maze_visited = True
        open_set.remove(current)

        for neighbor in current.get_neighbors():
            if not neighbor.maze_visited:
                neighbor.previous = current
                if neighbor not in open_set:
                    open_set.append(neighbor)
                    if neighbor.color != Orange and neighbor.color != Turquoise:
                        neighbor.set_color(Green)

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
            bfs(start, end, draw, path, grid)
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


def gbfs(start, end, draw, path_1, grid):
    # update heuristic and neighbors
    for row in grid:
        for node in row:
            node.update_neighbors(grid)
            node.h = heuristic(node, end[0])

    # variables
    open_set = [start]
    count = 0
    open_set_prio = PriorityQueue()
    open_set_prio.put((0, count, start))
    path = path_1
    algorithm = True

    while algorithm:
        clock.tick(1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if open_set_prio.empty():
            break
        current = open_set_prio.get()[2]
        open_set.remove(current)

        for neighbor in current.get_neighbors():
            if neighbor.color == Yellow or neighbor.color == Pink:
                neighbor.f = neighbor.h + 10
            else:
                neighbor.f = neighbor.h
            if neighbor not in open_set and neighbor.color != Red and neighbor != start: # and neighbor.color != Green and neighbor != start:
                neighbor.previous = current
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
                    node.h = math.inf
                    node.previous = None
            gbfs(start, end, draw, path, grid)
            break
        elif current == end[0] and len(end) == 1:
            end.pop(0)
            temp = current
            temp_path = [current]
            while temp.previous:
                temp_path.append(temp)
                temp = temp.previous
            path.extend(temp_path)
            for i in range(len(path)):
                if path[i].color != Orange and path[i].color != Turquoise:
                    path[i].set_color(Purple)
                elif path[i].color == Turquoise:
                    path[i].set_color(Grown)
                draw()
            algorithm = False
        draw()
