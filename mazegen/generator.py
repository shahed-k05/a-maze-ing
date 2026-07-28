# You must implement the maze generation as a unique class (e.g., ‘MazeGenerator‘) inside a
# standalone module that can be imported in a future project.
""" from dataclasses import dataclass


@dataclass
class Cell:
    r: int
    c: int

    N: bool = True
    E: bool = True
    S: bool = True
    W: bool = True

    visited: bool = False


    @property
    def calc_cell_value(self) -> str:
        cell_value = format(self.N * 1 + self.E * 2 + self.S * 4 + self.W * 8, 'X')
        return cell_value



class MazeGenerator():
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = []
        for row in range(height):
            lis: list[Cell] = []
            for col in range(width):
                cell = Cell(r=row, c=col)
                # print(cell.calc_cell_value)
                lis.append(cell)
            self.grid.append(lis)


    def generate(self, start: str):
        stack = []
        current = self.grid[start[0]][start[1]]
        current.visited = True
        stack.append(current)

        while stack:
            current = stack[-1]
            neighbors = self._get_neighbors(current)
            if neighbors:
                next_cell = random.choice(neighbors)
                self._remove_wall(current, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

 """
# m = MazeGenerator(4, 5)

import random
from dataclasses import dataclass


@dataclass
class Cell:
    r: int
    c: int
    N: bool = True
    E: bool = True
    S: bool = True
    W: bool = True
    visited: bool = False

    @property
    def calc_cell_value(self) -> str:
        cell_value = format(self.N * 1 + self.E * 2 + self.S * 4 + self.W * 8, 'X')
        return cell_value


class MazeGenerator:
    _DIRS = {
        "N": (-1, 0, "S"),
        "E": (0, 1, "W"),
        "S": (1, 0, "N"),
        "W": (0, -1, "E"),
    }


    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = []
        for row in range(height):
            lis: list[Cell] = []
            for col in range(width):
                cell = Cell(r=row, c=col)
                lis.append(cell)
            self.grid.append(lis)


    def _get_neighbors(self, cell: Cell) -> list[tuple[Cell, str]]:
        neighbors = []
        for direction, (dr, dc, _) in self._DIRS.items():
            nr, nc = cell.r + dr, cell.c + dc
            if 0 <= nr < self.height and 0 <= nc < self.width:
                neighbor = self.grid[nr][nc]
                if not neighbor.visited:
                    neighbors.append((neighbor, direction))
        return neighbors


    def _remove_wall(self, current: Cell, neighbor: Cell, direction: str) -> None:
        opposite = self._DIRS[direction][2]
        setattr(current, direction, False)
        setattr(neighbor, opposite, False)


    def generate(self, entry: tuple[int, int] = (0, 0)) -> None:
        start_row, start_col = entry
        stack: list[Cell] = []
        current = self.grid[start_row][start_col]
        current.visited = True
        stack.append(current)

        while stack:
            current = stack[-1]
            neighbors = self._get_neighbors(current)
            if neighbors:
                next_cell, direction = random.choice(neighbors)
                self._remove_wall(current, next_cell, direction)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()


    def to_ascii(self) -> str:
        lines = []
        top = "+" + "+".join("---" if True else "   " for _ in range(self.width)) + "+"
        lines.append("+" + "---+" * self.width)
        for row in self.grid:
            line_mid = "|"
            line_bottom = "+"
            for cell in row:
                line_mid += "   " + ("|" if cell.E else " ")
                line_bottom += ("---" if cell.S else "   ") + "+"
            lines.append(line_mid)
            lines.append(line_bottom)
        return "\n".join(lines)

    def export_hex(self) -> list[list[str]]:
        return [[cell.calc_cell_value for cell in row] for row in self.grid]
