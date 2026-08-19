from dataclasses import dataclass
from enum import Enum
from .colors import Colors
import random


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
        """
        returns the  hexadecimal value representing the cell walls
        """
        cell_value = format(
                self.N * 1 + self.E * 2 + self.S * 4 + self.W * 8, "X"
                )
        return cell_value


class MazeGenerator:
    def __init__(self, width: int, height: int,
                 seed: int | None = None) -> None:
        """Initialize the maze generator

        args:
            width: number of cells in each row.
            height: number of rows in the maze.
            seed: used to make maze generation reproducible.
        """
        self.width: int = width
        self.height: int = height
        self.rng = random.Random(seed)
        self.grid: list[list[Cell]] = []
        self.coordinate: set[tuple[int, int]] = set()
        self.logo: list[tuple[int, int]] = []
        # row by row
        for row in range(height):
            row_list: list[Cell] = []
            for col in range(width):
                row_list.append(Cell(r=row, c=col))
            self.grid.append(row_list)

    def n_neighbors(self, cell: Cell) -> list[tuple[Cell, Directions]]:
        """Return all unvisited neighboring cells.
        args:
                cell: the cell whose neighbors shoulde be cheched
        returns:
                a list of tuples that conatains unvisited neighboring cell
                and the dirc from the current cell to that neighbor
        """
        n: list[tuple[Cell, Directions]] = []
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

    def generate(self, entry: tuple[int, int]) -> None:
        """
        generate a maze using depth first search
        the algo starts from the entry cell
        and visits unvisited neighboring cells while removing the walls
        between connected cells
        args:
            entry: The row and column coordinates of the starting cell.
        """
        start_row, start_col = entry
        cell = self.grid[start_row][start_col]
        cell.visited = True
        stack: list[Cell] = [cell]
        while stack:
            current = stack[-1]
            n = self.n_neighbors(current)
            n = [(c, d) for c, d in n if (c.r, c.c) not in self.logo]
            if n:
                next_cell, direction = self.rng.choice(n)
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
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def check_3X3(self, cell: Cell) -> bool:
        """
        The maze can’t have large open areas.
        Corridors can’t be wider than 2 cells.
        For example, you can have 2x3 or 3x2 open area
        but never a 3x3 open area.
        """
        if cell.r + 2 >= self.height or cell.c + 2 >= self.width:
            return False
        reachable_n3X3 = [cell]
        visited = {(cell.r, cell.c)}
        while reachable_n3X3:
            current = reachable_n3X3.pop(0)
            for n, d in self.reachable_neighbors(current):
                if not (cell.r <= n.r <= cell.r + 2 and
                        cell.c <= n.c <= cell.c + 2):
                    continue
                if (n.r, n.c) not in visited:
                    visited.add((n.r, n.c))
                    reachable_n3X3.append(n)
        return len(visited) == 9

    def break_deadends(self) -> None:
        for row in self.grid:
            for cell in row:
                counter = 0
                if (cell.r, cell.c) in self.logo:
                    continue
                if cell.N:
                    counter += 1
                if cell.E:
                    counter += 1
                if cell.W:
                    counter += 1
                if cell.S:
                    counter += 1
                if counter >= 3:
                    self.break_walls(cell)

    def break_walls(self, cell: Cell) -> None:
        n = self.n_neighbors(cell)
        n = [(c, d) for c, d in n if (c.r, c.c) not in self.logo]
        if n:
            next_cell, direction = self.rng.choice(n)
            if direction == Directions.NORTH:
                cell.N = False
                next_cell.S = False
            elif direction == Directions.EAST:
                cell.E = False
                next_cell.W = False
            elif direction == Directions.SOUTH:
                cell.S = False
                next_cell.N = False
            elif direction == Directions.WEST:
                cell.W = False
                next_cell.E = False

    def imperfect_Maze(self) -> None:
        """
        in case the maze is not perfect this function loops for it.
        it uses n_neighbors to access unreachable neighbors.
        """
        for row in self.grid:
            for cell in row:
                if self.check_3X3(cell):
                    continue
                if (cell.r, cell.c) in self.logo:
                    continue
                else:
                    self.break_walls(cell)
        self.break_deadends()

    def create_output_file(
        self, entry: tuple[int, int],
        exitpoint: tuple[int, int],
        file: str,
        path: str
    ) -> None:
        """
        create the hexadecimal representaion of the maze
        """
        Entry = f"{entry[0]}, {entry[1]}"
        Exitpoint = f"{exitpoint[0]}, {exitpoint[1]}"
        maze_str = ""
        for row in self.grid:
            for cell in row:
                maze_str += cell.calc_cell_value
            if row != self.grid[-1]:
                maze_str += "\n"
        with open(file, "w") as f:
            f.write(maze_str)
            f.write("\n\n")
            f.write(Entry)
            f.write("\n")
            f.write(Exitpoint)
            f.write("\n")
            f.write(path)
            f.write("\n")

    def reachable_neighbors(self, cell: Cell) -> list[tuple[Cell, Directions]]:
        """
        returns neghboring cells that can be reached without crossing walls
        args:
                cell: whose reachable neighbors should be checked
        returns:
                a list of tuples containing each reachable neighboring cell
                and the direction from the current cell to that neighbor
        """
        n: list[tuple[Cell, Directions]] = []
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

    def bfs_alg(self,
                entry: tuple[int, int],
                exitpoint: tuple[int, int]) -> str:
        """
        find the shortest path between the entry and exit using BFS
        args:
            entry: The row and column coordinates of the starting cell
            exitpoint: The row and column coordinates of the destination cell
        returns:
            a string containing the dir of the shortest path
        """
        xs, ys = entry
        xe, ye = exitpoint

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
                    parent[(n.r, n.c)] = ((current_cell.r, current_cell.c), d)

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
        return "".join(d.name[0] for d in path)

    def draw(
        self,
        entry: tuple[int, int],
        exitpoint: tuple[int, int],
        show_path: bool,
        color: Colors,
        color_reset: str,
    ) -> None:
        """
        display the maze in the terminal
        the entry is displayed as S, the exit as E, and the shortest path
        can optionally be displayed using dots
        args:
                entry: The row and column coordinates of the maze entrance
                exitpoint: The row and column coordinates of the maze exit
                show_path: Whether to display the calculated path
                color: The terminal color used to draw the maze
                color_reset: The terminal escape sequence
                used to reset the color
        """
        xs, ys = entry
        xe, ye = exitpoint
        top_line = "▄"

        for cell in self.grid[0]:
            if cell.N:
                top_line += "▄▄▄▄"
            else:
                top_line += "   ▄"
        print(f"{color.value}{top_line}{color_reset}")
        for row in self.grid:
            middle_line = ""
            for cell in row:
                if cell.W:
                    middle_line += "█"
                else:
                    middle_line += " "
                if (cell.r, cell.c) in self.logo:
                    middle_line += (
                            f"{Colors.LIGHT_WHITE.value}░░░{color.value}"
                            )
                    continue
                if (cell.r, cell.c) == (xs, ys):
                    middle_line += " 🐀"
                    continue
                if (cell.r, cell.c) == (xe, ye):
                    middle_line += " 🪤"
                    continue
                if show_path:
                    if (cell.r, cell.c) in self.coordinate:
                        middle_line += (
                                f"{Colors.LIGHT_WHITE.value} • {color.value}"
                                )
                        continue
                middle_line += "   "
            if row[-1].E:
                middle_line += "█"
            else:
                middle_line += " "
            print(f"{color.value}{middle_line}{color_reset}")
            if self.grid.index(row) == len(self.grid) - 1:
                bottom_line = "▀"
                for cell in row:
                    if cell.S:
                        bottom_line += "▀▀▀▀"
                    else:
                        bottom_line += "   ▀"
            else:
                bottom_line = "█"
                for cell in row:
                    if cell.S:
                        bottom_line += "████"
                    else:
                        bottom_line += "   █"
            print(f"{color.value}{bottom_line}{color_reset}")
        print()
        print()
        print("1. Re-generate a new maze and display it")
        print("2. Show/Hide a valid shortest path ", end="")
        print("from the entrance to the exit")
        print("3. Change maze wall colors")
        print("4. Exit")

    def logo_42(
        self,
        Entry: tuple[int, int],
        Exitpoint: tuple[int, int],
        width: int,
        height: int,
    ) -> None:
        if width % 2 == 0:
            x = (width // 2) - 1
        else:
            x = (width // 2) + 1
        if height % 2 == 0:
            y = (height // 2) - 1
        else:
            y = (height // 2) + 1

        self.logo = [
            (y - 2, x - 3),
            (y - 1, x - 3),
            (y, x - 3),
            (y, x - 2),
            (y, x - 1),
            (y + 1, x - 1),
            (y + 2, x - 1),
            (y - 2, x + 1),
            (y - 2, x + 2),
            (y - 2, x + 3),
            (y - 1, x + 3),
            (y, x + 3),
            (y, x + 2),
            (y, x + 1),
            (y + 1, x + 1),
            (y + 2, x + 1),
            (y + 2, x + 2),
            (y + 2, x + 3),
        ]

        if (Entry in self.logo) or (Exitpoint in self.logo):
            raise Exception("Coordinate Error")
