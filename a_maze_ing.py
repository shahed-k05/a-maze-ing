import sys
import random
from mazegen.config_parser import read_config
from mazegen.generator import MazeGenerator
from mazegen.colors import Colors


def main() -> None:
    if len(sys.argv) <= 1:
        raise Exception("The configuratoin file does not exist")
    try:
        config = read_config(sys.argv[1])
        if config is None:
            return
        if not isinstance(config["WIDTH"], str) or not isinstance(
            config["HEIGHT"], str
        ):
            return
        if not isinstance(config["SEED"], str):
            return
        if not isinstance(config["PERFECT"], str):
            return
        if not isinstance(config["OUTPUT_FILE"], str):
            return
        if not isinstance(config["ENTRY"], tuple) or not isinstance(
            config["EXIT"], tuple
        ):
            return
        maze_gen_obj = MazeGenerator(
            int(config["WIDTH"]), int(config["HEIGHT"]), int(config["SEED"])
        )
        if int(config["WIDTH"]) < 8 or int(config["HEIGHT"]) < 6:
            print("Warning: maze too small")
        else:
            try:
                maze_gen_obj.logo_42(
                    config["ENTRY"],
                    config["EXIT"],
                    int(config["WIDTH"]),
                    int(config["HEIGHT"]),
                )
            except Exception as e:
                with open(config["OUTPUT_FILE"], "w"):
                    pass
                print(e)
                return

        maze_gen_obj.generate(config["ENTRY"])
        if config["PERFECT"] == "False":
            maze_gen_obj.imperfect_Maze()

        path = maze_gen_obj.bfs_alg(config["ENTRY"], config["EXIT"])
        maze_gen_obj.create_output_file(
            (config["ENTRY"]), (config["EXIT"]), config["OUTPUT_FILE"], path
        )
        show_path = True
        color: Colors = Colors.DEFAULT
        color_reset = "\u001b[0m"
        while True:
            maze_gen_obj.draw(
                config["ENTRY"], config["EXIT"], show_path, color, color_reset
            )
            action = input()
            if action == "1":
                maze_gen_obj = MazeGenerator(
                    int(config["WIDTH"]), int(config["HEIGHT"]), None
                )
                if int(config["WIDTH"]) < 8 or int(config["HEIGHT"]) < 6:
                    print("Warning: maze too small")
                else:
                    maze_gen_obj.logo_42(
                        config["ENTRY"],
                        config["EXIT"],
                        int(config["WIDTH"]),
                        int(config["HEIGHT"]),
                    )

                maze_gen_obj.generate(config["ENTRY"])
                if config["PERFECT"] == "False":
                    maze_gen_obj.imperfect_Maze()

                path = maze_gen_obj.bfs_alg(config["ENTRY"], config["EXIT"])
                maze_gen_obj.create_output_file(
                    config["ENTRY"], config["EXIT"],
                    config["OUTPUT_FILE"], path
                )
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
