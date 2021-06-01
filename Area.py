from Colors import Colors
import pygame


class Spot:
    """A class representing a single spot in the grid"""
    def __init__(self, win, rect, row, col):
        self.win = win
        self.rect = rect
        self.row = row
        self.col = col
        self.color = Colors.WHITE

    def is_wall(self):
        return self.color == Colors.BLACK

    def set_color(self, clr):
        self.color = clr

    def get_color(self):
        return self.color

    def draw(self, win):
        pygame.draw.rect(win, Colors.LIGHT_GRAY, pygame.draw.rect(win, self.color, self.rect), 1)

    def __lt__(self, other):
        return False


class Area:
    BLOCK_SIZE = 16

    def __init__(self, win, window_size):
        self.win = win
        self.window_size = window_size
        self.grid = []
        self.start = None
        self.end = None
        self.algorithm = None
        self.elements = self.window_size // self.BLOCK_SIZE
        self.pressed_list = [[False for _ in range(self.elements)] for _ in range(self.elements)]

    def set_algorithm(self, alg):
        self.algorithm = alg

    def handle_mouse(self, event):
        if pygame.mouse.get_pressed(3)[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row, col = mouse_x // self.BLOCK_SIZE, mouse_y // self.BLOCK_SIZE
            self.pressed_list[row][col] = True

            if not self.start:
                self.start = self.grid[row][col]
            elif not self.end:
                self.end = self.grid[row][col]

        if self.algorithm and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.start and self.end:
                self.algorithm.find_path(self.start, self.end)

    def grid_init(self):
        for x in range(0, self.window_size, self.BLOCK_SIZE):
            self.grid.append([])
            for y in range(0, self.window_size, self.BLOCK_SIZE):
                row = len(self.grid) - 1
                col = len(self.grid[row])
                rect = pygame.Rect(x, y, self.BLOCK_SIZE, self.BLOCK_SIZE)
                spot = Spot(self.win, rect, row, col)
                self.grid[row].append(spot)

        return self.grid

    def draw_grid(self):
        grid_size = len(self.grid)
        for i in range(grid_size):
            for j in range(grid_size):
                spot = self.grid[i][j]

                if i == 0 or j == 0 or i == grid_size - 1 or j == grid_size - 1:
                    spot.set_color(Colors.BLACK)
                    spot.draw(self.win)
                if self.start and spot != self.end:
                    self.start.set_color(Colors.GREEN)
                    self.start.draw(self.win)
                if self.end and spot != self.start:
                    self.end.set_color(Colors.RED)
                    self.end.draw(self.win)
                if self.pressed_list[i][j]:
                    spot.set_color(Colors.BLACK)
                    spot.draw(self.win)
                else:
                    spot.draw(self.win)
