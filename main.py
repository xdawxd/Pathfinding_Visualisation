from Area import Area
from Algorithms import Dijkstra, DFS, BFS
import pygame
import os

WINDOW_SIZE = 800

WIN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Pathfinding Visualisation')

ICON = pygame.image.load(os.path.join('static/icons', 'route.png'))
pygame.display.set_icon(ICON)

pygame.font.init()
FONT = pygame.font.Font('static/fonts/Fipps-Regular.otf', 24)


#  TODO:
#   -> fix the grid loading under the menu buttons
#   -> A*
def main():
    run = True

    area = Area(WIN, FONT)
    area.grid_init()

    dijkstra = Dijkstra(WIN, area)
    dfs = DFS(WIN, area)
    bfs = BFS(WIN, area)

    area.set_algorithm(dijkstra)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()

            area.handle_mouse(event)

        dijkstra.draw()

    pygame.quit()


if __name__ == '__main__':
    main()