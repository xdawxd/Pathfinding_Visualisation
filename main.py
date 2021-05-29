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
GRAY = (64, 64, 64)


def get_position(node):
    x, y = node.x, node.y
    pos_x, pos_y = x // 16, y // 16
    return pos_x, pos_y


class Dijkstra:

    def __init__(self, grid):  # pressed_list
        self.grid = grid
        self.size = len(grid)
        # self.pressed_list = pressed_list
        self.processed = []

    def get_neighbors(self, node):
        neighbors = []
        row, col = get_position(node)

        if row > 0:
            neighbors.append(self.grid[row - 1][col])
        if row < self.size:
            neighbors.append(self.grid[row + 1][col])
        if col > 0:
            neighbors.append(self.grid[row][col - 1])
        if col < self.size:
            neighbors.append(self.grid[row][col + 1])

        return neighbors

    def dijkstra(self, start, end):
        if not start or not end or start == end:
            return False

        queue = PriorityQueue()
        queue.put((0, start))
        distance = 0
        visited = {}

        while not queue.empty():
            current = queue.get()[1]
            visited[current] = distance
            distance += 1
            neighbors = self.get_neighbors(current)

            if current == end:
                # reconstruct the path
                return True

            for neighbor in neighbors:
                queue.put((distance, neighbor))


class Spot:
    """A class representing a single spot in the grid"""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE


class Area:
    BLOCK_SIZE = 16

    def __init__(self, win):
        self.win = win
        self.grid = []
        self.start = None
        self.end = None
        self.elements = WINDOW_WIDTH // self.BLOCK_SIZE
        self.pressed_list = [[False for _ in range(self.elements)] for _ in range(self.elements)]

    def grid_init(self):
        for x in range(0, WINDOW_WIDTH, self.BLOCK_SIZE):
            self.grid.append([])
            for y in range(0, WINDOW_HEIGHT, self.BLOCK_SIZE):
                rect = pygame.Rect(x, y, self.BLOCK_SIZE, self.BLOCK_SIZE)
                self.grid[len(self.grid) - 1].append(rect)

        return self.grid

    def handle_mouse(self):
        if pygame.mouse.get_pressed(3)[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row, col = mouse_x // 16, mouse_y // 16
            self.pressed_list[row][col] = True

            if not self.start:
                self.start = self.grid[row][col]

            elif not self.end:
                self.end = self.grid[row][col]

    def draw_grid(self):
        grid_size = len(self.grid)
        for i in range(grid_size):
            for j in range(grid_size):
                if i == 0 or j == 0 or i == grid_size - 1 or j == grid_size - 1:
                    pygame.draw.rect(WIN, BLACK, self.grid[i][j])
                if self.start:
                    pygame.draw.rect(WIN, BLACK, pygame.draw.rect(WIN, GREEN, self.start), 1)
                if self.end:
                    pygame.draw.rect(WIN, BLACK, pygame.draw.rect(WIN, RED, self.end), 1)
                if self.pressed_list[i][j]:
                    pygame.draw.rect(WIN, GRAY, pygame.draw.rect(WIN, BLACK, self.grid[i][j]), 1)
                else:
                    pygame.draw.rect(WIN, GRAY, self.grid[i][j], 1)


def draw(area):
    WIN.fill(WHITE)

    area.draw_grid()

    pygame.display.update()


def main():
    run = True
    area = Area(WIN)
    grid = area.grid_init()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            area.handle_mouse()

        draw(area)

    pygame.quit()


if __name__ == '__main__':
    main()
