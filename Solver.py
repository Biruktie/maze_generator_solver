from Direction import Direction
import random
class Solver:
    def __init__(self, maze,algorithm="dfs"):
        self.algorithm = algorithm
        self.maze = maze

        self.start_cell = maze.grid[maze.start[0]][maze.start[1]]
        self.end_cell = maze.grid[maze.end[0]][maze.end[1]]

        self.x = self.start_cell.row
        self.y = self.start_cell.col

        self.current_cell = self.start_cell

        self.stack = []

        self.visited = set()
        self.visited.add((self.start_cell.row, self.start_cell.col))

        self.dead_ends = set()
        self.turn_ends = set()

        self.solution_path = []

        self.solved = False
        self.finished = False

        self.directions = [
            Direction.TOP,
            Direction.RIGHT,
            Direction.BOTTOM,
            Direction.LEFT
        ]
        self.dir_index = 1

        self.steps = 0

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

    def solve_step(self):
        if self.current_cell == self.end_cell:
            self.solved = True
            self.finished = True
            self.solution_path = self.stack.copy()
            self.solution_path.append(self.current_cell)

            return

        neighbors = self.get_valid_neighbors(self.current_cell)
        if neighbors:
            next_cell, direction = random.choice(neighbors)
            self.stack.append(self.current_cell)

            self.current_cell = next_cell
            self.visited.add((next_cell.row, next_cell.col))
        else:
            dead_end = self.current_cell
            self.dead_ends.add((dead_end.row, dead_end.col))

            if self.stack:
                prev_cell = self.stack.pop()

                self.current_cell = prev_cell
            else:
                self.finished = True
                return

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.current_cell = self.maze.grid[self.x][self.y]
        self.visited.add((self.x, self.y))
    
    def is_open(self, x, y, direction):

        if x < 0 or y < 0 or x >= self.maze.rows or y >= self.maze.cols:
            return False

        cell = self.maze.grid[x][y]
        return not cell.walls[direction]

    def move_nums(self, direction):
        if direction == Direction.TOP:
            return -1, 0
        if direction == Direction.BOTTOM:
            return 1, 0
        if direction == Direction.LEFT:
            return 0, -1
        if direction == Direction.RIGHT:
            return 0, 1
    
    def can_move(self, x, y, dx, dy, direction):
        nx, ny = x + dx, y + dy

        if not (0 <= nx < self.maze.rows and 0 <= ny < self.maze.cols):
            return False

        return self.is_open(x, y, direction)