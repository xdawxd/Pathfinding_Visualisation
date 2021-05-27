import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 16


class Block:
    def __init__(self, row, col, size):
        pass


def draw(row, col):
    WIN.fill(BLACK)
    for i in range(81):
        for j in range(81):
            rect = pygame.Rect(0, 0, BLOCK_SIZE * i, BLOCK_SIZE * j)
            pygame.draw.rect(WIN, WHITE, rect, 1)

            if row == i and col == j:
                x = BLOCK_SIZE * row
                y = BLOCK_SIZE * col
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(WIN, WHITE, rect)

    pygame.display.update()


def main():
    global WIN
    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Visualiser')

    run = True
    while run:
        row, col = None, None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row, col = mouse_x // 16, mouse_y // 16

        draw(row, col)
    pygame.quit()


if __name__ == '__main__':
    main()
