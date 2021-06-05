from Area import Area
from Algorithms import Dijkstra, DFS, BFS
import pygame
import os

WINDOW_SIZE = 800

WIN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Pathfinding Visualisation')

icon = pygame.image.load(os.path.join('static/icons', 'route.png'))
pygame.display.set_icon(icon)


#  TODO -> right click for erasing, A*
#   some kind of menu to choose algorithms
def main():
    run = True

    area = Area(WIN, WINDOW_SIZE)
    area.grid_init()
    dijkstra = Dijkstra(WIN, area)
    dfs = DFS(WIN, area)
    bfs = BFS(WIN, area)

    area.set_algorithm(dijkstra)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            area.handle_mouse(event)

        dijkstra.draw()

    pygame.quit()


if __name__ == '__main__':
    main()