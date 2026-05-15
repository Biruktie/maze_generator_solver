from Direction import Direction


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = {Direction.TOP: True, Direction.RIGHT: True, Direction.BOTTOM: True, Direction.LEFT: True}
