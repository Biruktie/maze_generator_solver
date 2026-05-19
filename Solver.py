from Direction import Direction
import random
class Solver:
    def __init__(self, maze):
        self.maze = maze

        self.start_cell = maze.grid[maze.start[0]][maze.start[1]]

        self.current_cell = self.start_cell
        self.end_cell = maze.grid[maze.end[0]][maze.end[1]]

        self.stack = []

        self.visited = set()
        self.visited.add((self.start_cell.row, self.start_cell.col))

        self.solved = False
        self.finished = False

    def get_valid_neighbors(self, current_cell):
        valid_neighbors = []

        if not current_cell.walls[Direction.TOP]:
            if current_cell.row > 0:
                next_cell = self.maze.grid[current_cell.row-1][current_cell.col]
                if (next_cell.row, next_cell.col) not in self.visited:
                    valid_neighbors.append((next_cell, Direction.TOP))

        if not current_cell.walls[Direction.LEFT]:
            if current_cell.col > 0:
                next_cell = self.maze.grid[current_cell.row][current_cell.col - 1]
                if (next_cell.row, next_cell.col) not in self.visited:
                    valid_neighbors.append((next_cell, Direction.LEFT))

        if not current_cell.walls[Direction.BOTTOM]:
            if current_cell.row < self.maze.rows - 1:
                next_cell = self.maze.grid[current_cell.row + 1][current_cell.col]
                if (next_cell.row, next_cell.col) not in self.visited:
                    valid_neighbors.append((next_cell, Direction.BOTTOM))

        if not current_cell.walls[Direction.RIGHT]:
            if current_cell.col < self.maze.cols - 1:
                next_cell = self.maze.grid[current_cell.row][current_cell.col + 1]
                if (next_cell.row, next_cell.col) not in self.visited:
                    valid_neighbors.append((next_cell, Direction.RIGHT))

        return valid_neighbors
