import pygame


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

    def render_generation(self):
        self.screen.fill((255, 255, 255))
        pygame.display.update()