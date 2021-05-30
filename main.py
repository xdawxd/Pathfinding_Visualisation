import pygame
import os
from queue import PriorityQueue

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Pathfinding Visualisation')

icon = pygame.image.load(os.path.join('static/icons', 'route.png'))
pygame.display.set_icon(icon)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY_OUTLINE = (64, 64, 64)
GRAY = (200, 200, 200)
LIGHT_GRAY = (100, 100, 100)
TEAL = (0, 255, 255)


class Dijkstra:

    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid) - 1

    def draw_path(self, current, came_from):
        while current in came_from:
            current = came_from[current]
            current.set_color(TEAL)

    def get_neighbors(self, node):
        neighbors = []
        row = node.row
        col = node.col

        if row > 0 and not self.grid[row - 1][col].is_wall():
            neighbors.append(self.grid[row - 1][col])
        if row < self.size and not self.grid[row + 1][col].is_wall():
            neighbors.append(self.grid[row + 1][col])
        if col > 0 and not self.grid[row][col - 1].is_wall():
            neighbors.append(self.grid[row][col - 1])
        if col < self.size and not self.grid[row][col + 1].is_wall():
            neighbors.append(self.grid[row][col + 1])

        return neighbors

    def find_path(self, start, end):
        if not start or not end or start == end:
            return False

        queue = PriorityQueue()
        queue.put((0, start))
        costs = {spot: float('inf') for row in self.grid for spot in row}
        costs[start] = 0
        visited = {start}
        came_from = {}

        while not queue.empty():
            current = queue.get()[1]
            neighbors = self.get_neighbors(current)

            if current == end:
                # reconstruct the path

                self.draw_path(current, came_from)
                return True

            for neighbor in neighbors:
                temp_cost = costs[current] + 1

                if temp_cost < costs[neighbor]:
                    came_from[neighbor] = current
                    costs[neighbor] = temp_cost

                    if neighbor not in visited:
                        queue.put((temp_cost, neighbor))
                        visited.add(neighbor)
                        neighbor.set_color(GRAY)

            if current != start:
                current.set_color(LIGHT_GRAY)

        return False


class Spot:
    """A class representing a single spot in the grid"""
    def __init__(self, rect, row, col):
        self.rect = rect
        self.row = row
        self.col = col
        self.color = WHITE

    def is_wall(self):
        return self.color == BLACK

    def set_color(self, clr):
        self.color = clr

    def get_color(self):
        return self.color

    def draw(self, win):
        pygame.draw.rect(win, GRAY_OUTLINE, pygame.draw.rect(WIN, self.color, self.rect), 1)

    def __lt__(self, other):
        return False


class Area:
    BLOCK_SIZE = 16

    def __init__(self, win):
        self.win = win
        self.grid = []
        self.start = None
        self.end = None
        self.algorithm = None
        self.elements = WINDOW_WIDTH // self.BLOCK_SIZE
        self.pressed_list = [[False for _ in range(self.elements)] for _ in range(self.elements)]

    def set_algorithm(self, alg):
        self.algorithm = alg

    def grid_init(self):
        for x in range(0, WINDOW_WIDTH, self.BLOCK_SIZE):
            self.grid.append([])
            for y in range(0, WINDOW_HEIGHT, self.BLOCK_SIZE):
                row = len(self.grid) - 1
                col = len(self.grid[row])
                rect = pygame.Rect(x, y, self.BLOCK_SIZE, self.BLOCK_SIZE)
                spot = Spot(rect, row, col)
                self.grid[row].append(spot)

        return self.grid

    def handle_mouse(self, event):
        if pygame.mouse.get_pressed(3)[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row, col = mouse_x // 16, mouse_y // 16
            self.pressed_list[row][col] = True

            if not self.start:
                self.start = self.grid[row][col]

            elif not self.end:
                self.end = self.grid[row][col]

        if self.algorithm and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.start and self.end:
                self.algorithm.find_path(self.start, self.end)


    def draw_grid(self):
        grid_size = len(self.grid)
        for i in range(grid_size):
            for j in range(grid_size):
                spot = self.grid[i][j]

                if i == 0 or j == 0 or i == grid_size - 1 or j == grid_size - 1:
                    spot.set_color(BLACK)
                    spot.draw(WIN)
                if self.start and spot != self.end:
                    self.start.set_color(GREEN)
                    self.start.draw(WIN)
                if self.end and spot != self.start:
                    self.end.set_color(RED)
                    self.end.draw(WIN)
                if self.pressed_list[i][j]:
                    spot.set_color(BLACK)
                    spot.draw(WIN)
                else:
                    spot.draw(WIN)


def draw(area):
    WIN.fill(WHITE)

    area.draw_grid()

    pygame.display.update()


def main():
    run = True
    area = Area(WIN)
    grid = area.grid_init()
    dijkstra = Dijkstra(grid)
    area.set_algorithm(dijkstra)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            area.handle_mouse(event)

        draw(area)

    pygame.quit()


if __name__ == '__main__':
    main()
