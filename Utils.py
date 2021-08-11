from dataclasses import dataclass
import pygame
import os


@dataclass
class Colors:
    """A class representing colors."""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    LIGHT_GRAY = (64, 64, 64)
    GRAY = (200, 200, 200)
    DARK_GRAY = (100, 100, 100)
    TEAL = (0, 255, 255)


@dataclass
class Static:
    """A class containing all static variables used for the visualization."""
    BLOCK_SIZE: int = 16
    WINDOW_SIZE: int = 800
    OPTIONS_SIZE: tuple[int, int] = (WINDOW_SIZE - BLOCK_SIZE * 2) / 4, 65

    WIN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption('Pathfinding Visualisation')

    ICON = pygame.image.load(os.path.join('static/icons', 'route.png'))
    pygame.display.set_icon(ICON)

    pygame.font.init()
    FONT = pygame.font.Font('static/fonts/Fipps-Regular.otf', 24)
