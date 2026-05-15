from enum import Enum
class Direction(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

OPPOSITE = {
    Direction.TOP: Direction.BOTTOM,
    Direction.BOTTOM: Direction.TOP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT
}