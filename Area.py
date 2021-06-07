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

    def __init__(self, win, font):
        self.win = win
        self.font = font
        self.grid = []
        self.start = None
        self.end = None
        self.algorithm = None
        self.window_size = pygame.display.get_surface().get_size()[0]
        self.elements = self.window_size // self.BLOCK_SIZE

    def set_algorithm(self, alg):
        self.algorithm = alg

    def get_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        row, col = mouse_y // self.BLOCK_SIZE, mouse_x // self.BLOCK_SIZE
        return row, col

    def draw_rect(self, rect, color):
        pygame.draw.rect(self.win, Colors.LIGHT_GRAY, pygame.draw.rect(self.win, color, rect), 1)

    def inside_grid(self, row, col):
        if 5 < row < len(self.grid) - 1 and 0 < col < len(self.grid) - 1:
            return True
        return False

    def handle_mouse(self, event):
        if pygame.mouse.get_pressed(3)[0]:
            row, col = self.get_position()

            if self.inside_grid(row, col):
                self.grid[row][col].set_color(Colors.BLACK)

                if not self.start:
                    self.start = self.grid[row][col]

                elif not self.end:
                    self.end = self.grid[row][col]

        if pygame.mouse.get_pressed(3)[2]:
            row, col = self.get_position()

            if self.inside_grid(row, col):
                self.grid[row][col].set_color(Colors.WHITE)

        if self.algorithm and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.start and self.end:
                self.algorithm.find_path(self.start, self.end)

    def options_init(self):
        width = (self.window_size - self.BLOCK_SIZE * 2) / 4
        height = 65

        algorithms = ['Dijkstra', 'A*', 'BFS', 'DFS']

        for i in range(len(algorithms)):
            rect = pygame.Rect(self.BLOCK_SIZE + width * i, self.BLOCK_SIZE, width, height)

            if rect.collidepoint(pygame.mouse.get_pos()):
                text = self.font.render(algorithms[i], True, Colors.WHITE)
                self.draw_rect(rect, Colors.BLACK)
            else:
                text = self.font.render(algorithms[i], True, Colors.BLACK)
                self.draw_rect(rect, Colors.WHITE)

            text_pos = text.get_rect(center=(rect.x + width / 2, rect.y + height / 2))
            self.win.blit(text, text_pos)

    def grid_init(self):
        for x in range(0, self.window_size, self.BLOCK_SIZE):
            self.grid.append([])
            for y in range(0, self.window_size, self.BLOCK_SIZE):
                row = len(self.grid) - 1
                col = len(self.grid[row])

                if x == 0 or x > 64 or y == 0 or y == 784:
                    rect = pygame.Rect(y, x, self.BLOCK_SIZE, self.BLOCK_SIZE)
                    spot = Spot(self.win, rect, row, col)
                    self.grid[row].append(spot)

        return self.grid

    def draw(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                spot = self.grid[i][j]

                if self.start and spot != self.end:
                    self.start.set_color(Colors.GREEN)
                    self.start.draw(self.win)

                if self.end and spot != self.start:
                    self.end.set_color(Colors.RED)
                    self.end.draw(self.win)

                if i == 0 or j == 0 or i == len(self.grid) - 1 or \
                        j == len(self.grid[i]) - 1 or i == 5:
                    spot.set_color(Colors.BLACK)
                    spot.draw(self.win)

                else:
                    spot.draw(self.win)

        self.options_init()
