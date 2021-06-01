from queue import PriorityQueue
from Colors import Colors
import pygame


class Algorithm:
    def __init__(self, win, area):
        self.win = win
        self.area = area
        self.grid = area.grid
        self.size = len(area.grid) - 1

    def draw(self):
        self.win.fill(Colors.WHITE)

        self.area.draw_grid()

        pygame.display.update()

    def draw_path(self, current, came_from):
        while current in came_from:
            current = came_from[current]
            current.set_color(Colors.TEAL)
            self.draw()

    def get_neighbors(self, node):
        neighbors = []
        row = node.row
        col = node.col

        if row > 0 and not self.grid[row - 1][col].is_wall():
            neighbors.append(self.grid[row - 1][col])
        if row < self.size and not self.grid[row + 1][col].is_wall():
            neighbors.append(self.grid[row + 1][col])
        if col > 0 and not self.grid[row][col - 1].is_wall():
            neighbors.append(self.grid[row][col - 1])
        if col < self.size and not self.grid[row][col + 1].is_wall():
            neighbors.append(self.grid[row][col + 1])

        return neighbors


class Dijkstra(Algorithm):
    def __init__(self, win, area):
        super().__init__(win, area)

    def find_path(self, start, end):
        if not start or not end or start == end:
            return False

        queue = PriorityQueue()
        queue.put((0, start))
        costs = {spot: float('inf') for row in self.grid for spot in row}
        costs[start] = 0
        visited = {start}
        came_from = {}

        while not queue.empty():
            current = queue.get()[1]
            neighbors = self.get_neighbors(current)

            if current == end:
                self.draw_path(current, came_from)
                return True

            for neighbor in neighbors:
                cost = costs[current] + 1

                if cost < costs[neighbor]:
                    came_from[neighbor] = current
                    costs[neighbor] = cost

                    if neighbor not in visited:
                        queue.put((cost, neighbor))
                        visited.add(neighbor)
                        neighbor.set_color(Colors.DARK_GRAY)

            self.draw()

            if current != start:
                current.set_color(Colors.GRAY)

        return False


class DFS(Algorithm):
    def __init__(self, win, area):
        super().__init__(win, area)

    def find_path(self):
        pass
