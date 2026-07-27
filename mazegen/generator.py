# You must implement the maze generation as a unique class (e.g., ‘MazeGenerator‘) inside a
# standalone module that can be imported in a future project.
from dataclasses import dataclass
@dataclass
class Cell:
    row: int
    col: int

    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True

    visited: bool = False


class MazeGenerator():
    def __init__(self, width: int, height: int):
        self.width = width # 4
        self.height = height # 3
        self.grid = []
        for col in range(width):# 0 .. 3
            lis: list = []
            for row in range(height):# 0 .. 2
                cell = Cell(row, col)
                lis.append(cell)
            self.grid.append(lis)


m = MazeGenerator(4, 3)
print(m.grid[0][1].row)
