from Algorithms import Dijkstra, BFS, DFS, AStar
from Utils import Colors, Static
import pygame


class Spot:
    """A class representing a single spot in the grid"""

    def __init__(self, rect):
        self.rect = rect
        self.color = Colors.WHITE

    def is_wall(self):
        return self.color is Colors.BLACK

    def set_color(self, clr):
        self.color = clr

    def get_color(self):
        return self.color

    def get_position_in_grid(self):
        block_size = Static.BLOCK_SIZE
        row = self.rect.top // block_size
        col = self.rect.left // block_size
        return [row, col]

    def get_pos(self):
        return list(map(lambda pos: pos * Static.BLOCK_SIZE, self.get_position_in_grid()))

    def draw(self, win):
        pygame.draw.rect(win, Colors.LIGHT_GRAY, pygame.draw.rect(win, self.color, self.rect), 1)

    def __lt__(self, other):
        return False


class Area:
    def __init__(self):
        self.grid = []
        self.start = None
        self.end = None
        self.algorithm = None

    @staticmethod
    def get_mouse_position():
        mouse_x, mouse_y = pygame.mouse.get_pos()
        block_size = Static.BLOCK_SIZE
        row, col = mouse_y // block_size, mouse_x // block_size
        return row, col

    def is_inside_grid(self, row, col):
        if 5 < row < len(self.grid) - 1 and 0 < col < len(self.grid) - 1:
            return True
        return False

    def options_init(self):
        pass

    def grid_init(self):
        window_size = pygame.display.get_surface().get_size()[0]
        block_size = Static.BLOCK_SIZE

        for x in range(0, window_size, block_size):
            self.grid.append([])
            for y in range(0, window_size, block_size):
                spot = Spot(pygame.Rect(y, x, block_size, block_size))

                row = len(self.grid) - 1
                self.grid[row].append(spot)

        return self.grid


class Controller:
    def __init__(self, window, font, area):
        self.window = window
        self.font = font
        self.area = area

    def run_algorithm(self, algorithm):
        if not (self.area.start and self.area.end):
            return

        if self.lmb_pressed() and not self.area.algorithm:
            self.area.algorithm = algorithm(self.window, self)
            self.area.algorithm.find_path(self.area.start, self.area.end)

    def check_collision(self, rect, algorithm):
        if rect.collidepoint(pygame.mouse.get_pos()):
            text = self.font.render(algorithm.__name__, True, Colors.WHITE)
            self.draw_rect(rect, Colors.BLACK)
            self.run_algorithm(algorithm)
        else:
            text = self.font.render(algorithm.__name__, True, Colors.BLACK)
            self.draw_rect(rect, Colors.WHITE)

        return text

    def handle_options(self):
        block_size = Static.BLOCK_SIZE
        width, height = Static.OPTIONS_SIZE
        algorithms = (Dijkstra, AStar, BFS, DFS)

        for idx in range(len(algorithms)):
            rect = pygame.Rect(block_size + width * idx, block_size, width, height)
            algorithm = algorithms[idx]

            text = self.check_collision(rect, algorithm)
            text_pos = text.get_rect(center=(rect.x + width / 2, rect.y + height / 2))
            self.window.blit(text, text_pos)

    def lmb_pressed(self):
        return True if pygame.mouse.get_pressed(3)[0] else False

    def color_field(self, row, col):
        if not self.area.is_inside_grid(row, col):
            return

        self.area.grid[row][col].set_color(Colors.BLACK)

        if not self.area.start:
            self.area.start = self.area.grid[row][col]

        elif not self.area.end:
            self.area.end = self.area.grid[row][col]

    def rmb_pressed(self):
        return True if pygame.mouse.get_pressed(3)[2] else False

    def clear_field(self, row, col):
        if self.area.is_inside_grid(row, col):
            self.area.grid[row][col].set_color(Colors.WHITE)

    def handle_mouse(self):
        if self.lmb_pressed():
            row, col = self.area.get_mouse_position()
            self.color_field(row, col)

        if self.rmb_pressed():
            row, col = self.area.get_mouse_position()
            self.clear_field(row, col)

    def start_set(self, current):
        return True if self.area.start and current != self.area.end else False

    def end_set(self, current):
        return True if self.area.end and current != self.area.start else False

    def draw_spot(self, current, color):
        current.set_color(color)
        current.draw(self.window)

    def draw_rect(self, rect, color):
        pygame.draw.rect(self.window, Colors.LIGHT_GRAY, pygame.draw.rect(self.window, color, rect), 1)

    def draw(self):
        self.window.fill(Colors.WHITE)
        for row in range(len(self.area.grid)):
            for col in range(len(self.area.grid[row])):
                spot = self.area.grid[row][col]

                if self.start_set(spot):
                    self.draw_spot(self.area.start, Colors.GREEN)

                elif self.end_set(spot):
                    self.draw_spot(self.area.end, Colors.RED)

                if not self.area.is_inside_grid(row, col):
                    self.draw_spot(spot, Colors.BLACK)

                else:
                    spot.draw(self.window)

        self.handle_options()
        pygame.display.update()
