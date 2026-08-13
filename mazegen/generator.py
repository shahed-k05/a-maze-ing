# You must implement the maze generation as a unique class (e.g., ‘MazeGenerator‘) inside a
# standalone module that can be imported in a future project.
from dataclasses import dataclass
from enum import Enum
#import random
import numpy as np
class Directions(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

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
    def __init__(self, width: int, height: int, seed: int | None = None) -> None:
        self.width: int = width
        self.height: int = height
        self.rng = np.random.default_rng(seed)
        self.grid: list[list[Cell]] = []
        self.coordinate = set()
        # row by row
        for row in range(height):
            row_list: list[Cell] = []
            for col in range(width):
                row_list.append(Cell(r=row, c=col))
            self.grid.append(row_list)


    def n_neighbors(self, cell: Cell) -> list[tuple[Cell, Directions]]:
        n: list = []
        r = cell.r
        c = cell.c

        if r > 0 and not self.grid[r - 1][c].visited:
            n.append((self.grid[r - 1][c], Directions.NORTH))
        if c < self.width - 1 and not self.grid[r][c + 1].visited:
            n.append((self.grid[r][c + 1], Directions.EAST))
        if r < self.height - 1 and not self.grid[r + 1][c].visited:
            n.append((self.grid[r + 1][c], Directions.SOUTH))
        if c > 0 and not self.grid[r][c - 1].visited:
            n.append((self.grid[r][c - 1], Directions.WEST))
        return n


    def generate(self, entry: str):
        start_row, start_col = entry.split(',', 1)
        start_row = int(start_row)
        start_col = int(start_col)
        cell = self.grid[start_row][start_col]
        cell.visited = True
        stack: list[Cell] = [cell]
        while stack:
            current = stack[-1]
            n = self.n_neighbors(current)
            if n:
                next_cell, direction = n[self.rng.integers(len(n))]
                if direction == Directions.NORTH:
                    current.N = False
                    next_cell.S = False
                elif direction == Directions.EAST:
                    current.E = False
                    next_cell.W = False
                elif direction == Directions.SOUTH:
                    current.S = False
                    next_cell.N = False
                elif direction == Directions.WEST:
                    current.W = False
                    next_cell.E = False
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()


    def create_output_file(self) -> str:
        maze_str = ""
        for row in self.grid:
            for cell in row:
                maze_str += cell.calc_cell_value
            if row != self.grid[-1]:
                maze_str += "\n"
        return maze_str

    def reachable_neighbors(self, cell: Cell) -> list[tuple[Cell, Directions]]:
        n: list = []
        r = cell.r
        c = cell.c

        if r > 0 and not cell.N:
            n.append((self.grid[r - 1][c], Directions.NORTH))
        if c < self.width - 1 and not cell.E:
            n.append((self.grid[r][c + 1], Directions.EAST))
        if r < self.height - 1 and not cell.S:
            n.append((self.grid[r + 1][c], Directions.SOUTH))
        if c > 0 and not cell.W:
            n.append((self.grid[r][c - 1], Directions.WEST))
        return n

    def bfs_alg(self, entry: str, exitpoint: str) -> str:
        xs, ys = entry.split(',', 1)
        xe, ye = exitpoint.split(',', 1)
        xs = int(xs)
        ys = int(ys)
        xe = int(xe)
        ye = int(ye)
        front = [self.grid[xs][ys]]
        explored = [self.grid[xs][ys]]
        parent = {}
        path = []
        while len(front) > 0:
            current_cell = front.pop(0)
            if current_cell == self.grid[xe][ye]:
                break
            for n, d in self.reachable_neighbors(current_cell):
                if n not in explored:
                    front.append(n)
                    explored.append(n)
                    parent[(n.r,n.c)] = ((current_cell.r ,current_cell.c), d)

        current = (xe, ye)
        start = (xs, ys)
        if current not in parent and current != start:
            return "there is no path leading to the end point"
        self.coordinate.clear()
        while current != start:
            parent_cell, d = parent[current]
            self.coordinate.add(parent_cell)
            path.append(d)
            current = parent_cell
        path.reverse()
        return ("".join(d.name[0] for d in path))

    def draw(self, entry: str, exitpoint: str, show_path: bool, color, color_reset) -> None:
        xs, ys = entry.split(',', 1)
        xe, ye = exitpoint.split(',', 1)
        top_line = "+"
        for cell in self.grid[0]:
            if cell.N:
                top_line += "---+"
            else:
                top_line += "   +"
        print(f"{color.value}{top_line}{color_reset}")
        for row in self.grid:
            middle_line = ""
            for cell in row:
                if cell.W:
                    middle_line += "|"
                else:
                    middle_line += " "
                if (str(cell.r), str(cell.c)) == (xs, ys):
                        middle_line += " S "
                        continue
                if (str(cell.r), str(cell.c)) == (xe, ye):
                        middle_line += " E "
                        continue
                if show_path:
                    if (cell.r, cell.c) in self.coordinate:
                        middle_line += " . "
                        continue
                middle_line += "   "
            if row[-1].E:
                middle_line += "|"
            else:
                middle_line += " "
            print(f"{color.value}{middle_line}{color_reset}")
            bottom_line = "+"
            for cell in row:
                if cell.S:
                    bottom_line += "---+"
                else:
                    bottom_line += "   +"
            print(f"{color.value}{bottom_line}{color_reset}")
        print()
        print()
        print("1. Re-generate a new maze and display it")
        print("2. Show/Hide a valid shortest path from the entrance to the exit")
        print("3. Change maze wall colors")
        print("4. Exit")
