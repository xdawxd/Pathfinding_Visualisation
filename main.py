import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Visualiser')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Algorithms:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end

    def a_star(self):
        pass


class Area:
    GRID_SIZE = 50
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
                    pygame.draw.rect(WIN, BLACK, self.grid[i][j])
                else:
                    pygame.draw.rect(WIN, BLACK, self.grid[i][j], 1)


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
