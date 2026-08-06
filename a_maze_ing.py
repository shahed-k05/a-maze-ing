import sys
import random
from mazegen.config_parser import read_config
from mazegen.generator import MazeGenerator
#from mazegen.solver import dfs_alg
try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as  e:
    print(e)
    sys.exit(1)


def main() -> None:
    if len(sys.argv) <= 1:
        raise Exception("The configuratoin file does not exist")
    try:
        config = read_config(sys.argv[1])
        maze_gen_obj = MazeGenerator(int(config['WIDTH']), int(config['HEIGHT']), int(config['SEED']))
        maze_gen_obj.generate(config['ENTRY'])
        for row in maze_gen_obj.grid:
            print([c.calc_cell_value for c in row])
        output = maze_gen_obj.create_output_file(config['ENTRY'],config['EXIT'])
        with open("output_maze.txt", "w") as f:
            f.write(output)
        # dfs_alg(output, config['ENTRY'], config['EXIT'])
        # n = []
        # for cell in maze_gen_obj.grid:
        #     n = maze_gen_obj.visited_neighbors(cell)
        # print(n)


    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
