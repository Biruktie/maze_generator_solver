# Computer Graphics Assignment: Building and Running Mazes

This project implements an interactive maze generator and automatic maze solver visualized using Pygame. The generator constructs a proper maze where every cell is connected through a unique path. Maze generation is implemented using a randomized stack-based DFS approach, while solving is implemented using both randomized backtracking DFS and the wall follower (“shoulder-to-the-wall”) algorithm.

As an additional feature, the project also supports cycle generation to demonstrate cases where the wall follower algorithm fails when the destination is inside the maze and loops exist.

## Important Improvements to the Suggested Implementation

### Cell-Based Wall Representation

The assignment document suggested representing walls using two 2D arrays:

```c
char northWall[R][C], eastWall[R][C];
```

In this representation:

- `northWall[i][j]` represents the upper wall of a cell.
- `eastWall[i][j]` represents the right wall of a cell.

While functional, this approach requires coordinate offsets to query southern and western walls and introduces extra boundary-handling complexity. To simplify wall management, we instead designed a `Cell` class that explicitly stores all four walls:

```python
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = {
            Direction.TOP: True,
            Direction.RIGHT: True,
            Direction.BOTTOM: True,
            Direction.LEFT: True
        }
```

Wall removal is handled symmetrically using an `OPPOSITE` direction lookup:

```python
def remove_wall(self, current_cell, next_cell, direction):
    current_cell.walls[direction] = False
    next_cell.walls[OPPOSITE[direction]] = False
```

This approach improves readability, reduces boundary-related errors, and integrates naturally with our project’s object-oriented design.

### Stack-Based DFS for Maze Generation

The assignment document suggests storing alternative candidate cells on the stack during generation. Our implementation instead stores the traversal path itself and performs iterative DFS with explicit backtracking.

This approach is algorithmically equivalent because when the generator reaches a dead end, it backtracks through previously visited cells until it finds one with unexplored neighbors. Instead of storing all alternative branches immediately, unexplored paths are rediscovered dynamically during backtracking.

We chose this design because it closely mirrors the standard recursive DFS maze-generation algorithm while remaining iterative and simplifying stack management.

---

# Implementation Details

## Maze Generation

The maze is generated dynamically using randomized stack-based DFS:

1. The grid begins with all walls intact.
2. A starting cell is selected and marked as visited.
3. The generator checks neighboring cells that are within bounds and unvisited.
4. If valid neighbors exist:
   - One is chosen randomly.
   - The separating wall is removed.
   - The current cell is pushed onto a stack.
   - The generator moves to the selected neighbor.

5. If a dead end is reached, the generator backtracks using the stack.
6. Generation terminates when the stack becomes empty, ensuring all cells are connected.

## Bonus Feature: Cycle Injection

A proper maze forms a tree structure with no cycles. To introduce additional complexity, the project optionally supports cycle generation (`allow_cycles=True`).

During generation, there is a 5% probability (1 in 20 chance) that the generator removes an additional wall between two already visited neighboring cells. This introduces loops into the maze and creates more challenging solving scenarios.

---

# Maze Solving

## Backtracking Algorithm

Once the maze is generated, a solver mouse is placed at the starting cell to search for the exit:

1. **Exploration**: The solver checks all open neighboring paths while ignoring previously visited cells.
2. **Path Choice**: If valid neighbors exist, one is selected randomly, the current cell is pushed onto the stack, and the solver moves forward.
3. **Backtracking & Dead Ends**: When no valid moves remain, the current cell is marked as a dead end (blue in the visualization), and the solver backtracks using the stack.
4. **Success**: The algorithm terminates once the exit cell is reached, and the final solution path is highlighted.

## Wall Follower Algorithm

The wall follower (“shoulder-to-the-wall”) algorithm solves the maze by continuously maintaining contact with the right wall while tracking the solver’s current orientation.

1. **Initial Orientation**: The solver begins facing an initial direction stored using a directional index (`dir_index`).

2. **Movement Priority**: At each step, the solver checks possible movements in the following priority order:
   - Attempt to turn right and move forward.
   - Otherwise continue moving forward.
   - Otherwise turn left and move forward.
   - Otherwise turn around and move backward.

3. **Directional Movement**: Direction helper functions (`right_dir`, `left_dir`, `cur_dir`) determine the next orientation, while `move_nums()` converts directions into coordinate offsets for movement.

4. **Wall Checking**: Before moving, the solver verifies that:
   - The target position remains inside maze boundaries.
   - No wall blocks movement in the chosen direction.

5. **Loop Handling**: Since wall-following algorithms may become trapped in cycles, the implementation includes a step limit (`steps > 2000`) to safely terminate infinite loops. Cells where the solver is forced to turn back are also tracked for visualization purposes.

6. **Success Condition**: The algorithm terminates successfully once the solver reaches the destination cell.

7. **Limitations with Cycles**: The wall follower method works reliably for proper mazes where the entrance and exit lie on the outer boundary. However, when cycles are introduced and the destination lies inside the maze interior, the solver may repeatedly traverse the same loop without reaching the target.

---

# Theoretical Analysis

## Stack vs Queue (DFS vs BFS)

A queue is not necessarily “better” than a stack, but it significantly changes the maze structure.

- **Stack-based exploration (DFS)** produces long corridors and deep winding paths because the generator explores deeply before backtracking.
- **Queue-based exploration (BFS)** expands uniformly outward from the starting point, producing shorter and denser branches.

Using a stack creates the classic maze appearance with deep paths and fewer local branches.

## Wall Follower Method and Cycles

The wall follower method works reliably when the maze forms a proper connected structure and the start/end lie on the outer boundary.

Even when cycles exist, continuously following the outer wall eventually reaches the exit if both the entrance and exit are connected to the maze boundary.

However, when the start or end lies inside the maze interior and cycles surround the destination, the solver may become trapped indefinitely following an internal loop. This project demonstrates this limitation using interior start/end points combined with random cycle injection.

---

# Getting Started

## Prerequisites

Install dependencies using:

```bash
pip install -r requirements.txt
```

## Running the Application

Run the visualizer using:

```bash
python main.py
```
