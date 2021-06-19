from Area import Area
import pygame
import os


class Visualize:
    WINDOW_SIZE = 800

    WIN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption('Pathfinding Visualisation')

    ICON = pygame.image.load(os.path.join('static/icons', 'route.png'))
    pygame.display.set_icon(ICON)

    pygame.font.init()
    FONT = pygame.font.Font('static/fonts/Fipps-Regular.otf', 24)

    @classmethod
    def visualize(cls):
        run = True

        area = Area(cls.WIN, cls.FONT)
        area.grid_init()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        cls.visualize()

                area.handle_mouse(event)

            area.draw()

        pygame.quit()
