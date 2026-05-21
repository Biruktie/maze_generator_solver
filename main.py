import random

import pygame
from Maze import Maze
from Renderer import Renderer
from Solver import Solver

newCells = False  # for checking if the user wants the start and edge cells to be in the middle of the maze or not
cycles = False  # for checking if the user wants cycles in the maze or not

edge = input("Do you want the start and end cells to be in the middle of the maze? y/n: ")
if edge == "y":
    newCells = True

cycled = input("Do you want to create cycles in the maze? y/n: ")
if cycled == "y":
    cycles = True

print("Choose solving algorithm: ")
print("1 -> DFS backtracking")
print("2 -> Shoulder-to-wall algorithm")

choice = input("Enter choice: ")

if choice == "1":
    algorithm = "dfs"
elif choice == "2":
    algorithm = "shoulder"
else:
    print("Invalid choice, defaulted to dfs")
    algorithm = "dfs"


pygame.init()
rows = 15
cols = 15

if newCells:
    start_row = random.randint(1, rows - 2)
    start_col = random.randint(1, cols - 2)

    end_row = random.randint(1, rows - 2)
    end_col = random.randint(1, cols - 2)

    while (start_row, start_col) == (end_row, end_col):
        end_row = random.randint(1, rows - 2)
        end_col = random.randint(1, cols - 2)

    if cycled:
        maze = Maze(rows, cols, start=(start_row, start_col), end=(end_row, end_col), allow_cycles=True)
    else:
        maze = Maze(rows, cols, start=(start_row, start_col), end=(end_row, end_col))
else:
    if cycled:
        maze = Maze(rows, cols, allow_cycles=True)
    else:
        maze = Maze(rows, cols)

renderer = Renderer(maze)

clock = pygame.time.Clock()

mode = "generate"
solver = None

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if mode == "generate":
        if not maze.maze_generated:
            maze.generate_step()
            pygame.time.delay(10)

        else:
            solver = Solver(maze, algorithm=algorithm)
            renderer.solver = solver
            mode = "solve"

        renderer.render_generation()

    elif mode == "solve":
        if solver and not solver.finished:
            solver.step()
            pygame.time.delay(40)

        renderer.render_solver()

pygame.quit()
