from Area import Area, Controller
from Utils import Static
import pygame


class Visualize:
    WIN = Static.WIN
    FONT = Static.FONT

    @classmethod
    def visualize(cls):
        area = Area()
        area.grid_init()
        controller = Controller(cls.WIN, cls.FONT, area)

        run = True
        while run:
            for event in pygame.event.get():
                run = False if event.type == pygame.QUIT else True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        cls.visualize()

                controller.handle_mouse()

            controller.draw()

        pygame.quit()
