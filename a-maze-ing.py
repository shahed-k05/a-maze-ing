""" import sys
import random
from mazegen.config_parser import read_config

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as  e:
    print(e)
    sys.exit(1)


def main() -> None:
    if len(sys.argv) <= 1:
        raise Exception("The configuratoin file does not exist")
        sys.exit(1)
    try:
        config = read_config(sys.argv[1])
        maze_gen_obj = MazeGenerator(config['WIDTH'], config['HEIGHT'])
        maze_gen_obj.generate(config['ENTRY'])
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()
 """
import sys

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    print(e)
    sys.exit(1)

from mazegen.config_parser import read_config, ConfigError
from mazegen.generator import MazeGenerator


def draw_maze(maze: MazeGenerator, entry: tuple[int, int], exit_: tuple[int, int]) -> None:
    fig, ax = plt.subplots(figsize=(maze.width, maze.height))
    for row in maze.grid:
        for cell in row:
            x, y = cell.c, maze.height - cell.r  # نعكس y عشان الرسم يطلع من فوق لتحت
            if cell.N:
                ax.plot([x, x + 1], [y, y], color="black")
            if cell.S:
                ax.plot([x, x + 1], [y - 1, y - 1], color="black")
            if cell.E:
                ax.plot([x + 1, x + 1], [y - 1, y], color="black")
            if cell.W:
                ax.plot([x, x], [y - 1, y], color="black")

    er, ec = entry
    xr, xc = exit_
    ax.plot(ec + 0.5, maze.height - er - 0.5, "go", markersize=12, label="Entry")
    ax.plot(xc + 0.5, maze.height - xr - 0.5, "ro", markersize=12, label="Exit")

    ax.set_xlim(0, maze.width)
    ax.set_ylim(0, maze.height)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.legend()
    plt.tight_layout()
    plt.savefig("maze.png", dpi=150)
    print("Maze saved to maze.png")


def main() -> None:
    if len(sys.argv) <= 1:
        print("Usage: python main.py <config_file>")
        sys.exit(1)

    try:
        config = read_config(sys.argv[1])

        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        er, ec = (int(v) for v in config["ENTRY"].split(",", 1))
        xr, xc = (int(v) for v in config["EXIT"].split(",", 1))

        maze_gen_obj = MazeGenerator(width, height)
        maze_gen_obj.generate((er, ec))

        print(maze_gen_obj.to_ascii())
        draw_maze(maze_gen_obj, (er, ec), (xr, xc))

    except ConfigError as e:
        print(f"Config error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
