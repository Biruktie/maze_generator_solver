from Cell import Cell
from Direction import Direction, OPPOSITE
import random

class Maze:
    def __init__(self, rows, cols, start=(0, 0), end=None, allow_cycles=False):
        self.rows = rows
        self.cols = cols

        self.start = start

        if end is None:
            end = (rows - 1, cols - 1)
        self.end = end

        self.grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.maze_generated = False  # Indicates if the maze generation is complete

        # Enterance direction 
        start_direction = self.create_opening(start)

        # Exit direction
        end_direction = self.create_opening(end)

        self.grid[self.start[0]][self.start[1]].walls[start_direction] = False  # Entrance
        self.grid[self.end[0]][self.end[1]].walls[end_direction] = False  # Exit

        self.visited_cells = [[False for _ in range(cols)] for _ in
                              range(rows)]  # Tracking the visited cells during generation

        self.visited_cells[self.start[0]][
            self.start[1]] = True  # The starting cell is considered visited from the beginning

        # Used for step-by-step generation
        self.stack = []
        self.current_cell = self.grid[start[0]][start[1]]

        # To support cycle generation 
        self.allow_cycles = allow_cycles

        # Log of the moves taken during generation, useful for visualization
        self.action_log = []  # Stores tuples of (current_cell, next_cell, action_type) where action_type can be "move" or "backtrack" or "cycle"

    def create_opening(self, position):
        row, col = position

        possible_walls = []

        # Check which maze boundary the cell touches

        if row == 0:
            possible_walls.append(Direction.TOP)

        if row == self.rows - 1:
            possible_walls.append(Direction.BOTTOM)

        if col == 0:
            possible_walls.append(Direction.LEFT)

        if col == self.cols - 1:
            possible_walls.append(Direction.RIGHT)

        # If cell is not on boundary we assign an opening on the top by default
        if not possible_walls:
            print(f"Cell {position} is not on the boundary, so we create an opening on the top by default")
            return Direction.TOP

        # Randomly choose one valid outer wall
        opening_direction = random.choice(possible_walls)

        # Remove that wall
        self.grid[row][col].walls[opening_direction] = False

        return opening_direction

    # Added for testing to generate and observe the final maze 
    def generate_maze(self):
        while not self.maze_generated:
            self.generate_step()

    def generate_step(self):
        neighbors = self.get_unvisited_neighbors(self.current_cell)

        if neighbors:
            next_cell, direction = random.choice(neighbors)
            self.remove_wall(self.current_cell, next_cell, direction)

            # LOG MOVE
            self.action_log.append(
                (self.current_cell, next_cell, "move")
            )

            self.stack.append(self.current_cell)

            self.visited_cells[next_cell.row][next_cell.col] = True
            self.current_cell = next_cell

        elif self.stack:
            self.current_cell = self.stack.pop()
            self.action_log.append(
                (self.current_cell, None, "backtrack")
            )


        else:
            self.maze_generated = True

