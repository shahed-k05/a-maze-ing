import sys
import random
from mazegen.config_parser import read_config
from mazegen.generator import MazeGenerator
from mazegen.colors import Colors
try:
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
        output = maze_gen_obj.create_output_file()
        path = maze_gen_obj.bfs_alg(config['ENTRY'],config['EXIT'])
        with open("output_maze.txt", "w") as f:
            f.write(output)
            f.write("\n\n")
            f.write(config['ENTRY'])
            f.write("\n")
            f.write(config['EXIT'])
            f.write("\n")
            f.write(path)
        show_path = True
        color = Colors.DEFAULT
        color_reset = "\u001b[0m"
        while True:
            maze_gen_obj.draw(config['ENTRY'],config['EXIT'], show_path, color, color_reset)
            action = input()
            if action == "1":
                maze_gen_obj = MazeGenerator(int(config['WIDTH']), int(config['HEIGHT']), None)
                maze_gen_obj.generate(config['ENTRY'])
                output = maze_gen_obj.create_output_file()
                path = maze_gen_obj.bfs_alg(config['ENTRY'],config['EXIT'])
                with open("output_maze.txt", "w") as f:
                    f.write(output)
                    f.write("\n\n")
                    f.write(config['ENTRY'])
                    f.write("\n")
                    f.write(config['EXIT'])
                    f.write("\n")
                    f.write(path)
            if action == "2":
                show_path = not show_path
            if action == "3":
                color = random.choice(list(Colors))

            if action == "4":
                break

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
