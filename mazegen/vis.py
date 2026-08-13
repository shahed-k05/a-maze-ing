from .generator import Directions
class ascii_visualizer:
    @staticmethod
    def Convert_to_Binary(hex_cells :str) -> list:
        b_list =[]
        for cell in hex_cells:
            if cell == "\n":
                b_list.append("\n")
            else:
                b_list.append(format (int(cell, 16), '04b'))
        return b_list
    @staticmethod
    def draw(b_cells) -> None:
        for bit in b_cells:
            if bit == "\n":
                print()
            for bit in bit:
                if bit == "1":
                    print("#", end="")
                else:
                    print(" ", end="")


