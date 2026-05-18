import pygame
from Direction import Direction


class Renderer:
    def __init__(self, maze, solver=None, cell_size=40):
        self.maze = maze
        self.solver = solver

        self.cell_size = cell_size
        width = maze.cols * cell_size
        height = maze.rows * cell_size

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Maze Solver")

    def get_pos(self, cell):
        x = cell.col * self.cell_size
        y = cell.row * self.cell_size
        return x, y

    def draw_maze(self):
        for row in self.maze.grid:
            for cell in row:
                x, y = self.get_pos(cell)
                s = self.cell_size

                if cell.walls[Direction.TOP]:
                    pygame.draw.line(
                        self.screen,
                        (0, 0, 0),
                        (x, y),
                        (x + s, y)
                    )

                if cell.walls[Direction.LEFT]:
                    pygame.draw.line(
                        self.screen,
                        (0, 0, 0),
                        (x, y),
                        (x, y + s)
                    )

                if cell.walls[Direction.BOTTOM]:
                    pygame.draw.line(
                        self.screen,
                        (0, 0, 0),
                        (x, y + s),
                        (x + s, y + s)
                    )

                if cell.walls[Direction.RIGHT]:
                    pygame.draw.line(
                        self.screen,
                        (0, 0, 0),
                        (x + s, y),
                        (x + s, y + s)
                    )

    def render_generation(self):
        self.screen.fill((255,255,255))
        self.draw_maze()

        pygame.display.update()