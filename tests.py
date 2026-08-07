# m = MazeGenerator(20,20, 42)
# # print("Cell values: before maze generation:")

# # for row in m.grid:
# #     print([c.calc_cell_value for c in row])
# m.generate("0,0")
# # for row in m.grid:
# #     print([f"({c.r}, {c.c})" for c in row])

# # print("Cell values: after maze generation:")
# # for row in m.grid:
# #     print([c for c in row])
# # print("\n\n\n\n\n")
# print(m.bfs_alg(("0,0"), ("10,10")))
# # n = []
# # for cell in m.grid:
# #     for i in cell:
# #         print(m.reachable_neighbors(i))
