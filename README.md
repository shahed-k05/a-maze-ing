*This activity has been created as part of the 42 curriculum by sshakhat, syasin*
# A-Maze-ing
## Description
This is the "A-MAZE-ING" project from 42 School. It was written in python 3
The goal was to create a reusable maze generator module using mazegen package 
The program:
  - Generate maze using **Depth-first-search(DFS)** with iterative backtracking.
  - Solves them using **Breadth-first-search(BFS) to find the shortest path.
  - Renders them in the **terminal** with full ANSI colors.
  - Exports them to a file in **hexadecimal format**.
  - Embeds a visible **"42" pattern**.
## Project Structure
**A_Maze_ing** is the root directory of the project. It contains:
```text
.
├── a_maze_ing.py
├── config.txt
├── LICENSE.md
├── Makefile
├── mazegen
│   ├── colors.py
│   ├── config_parser.py
│   ├── generator.py
│   └── __init__.py
├── mazegen-1.0.0-py3-none-any.whl
├── maze.txt
├── pyproject.toml
└── README.md
```
## Instructions

### Runnig the project 
```bash
make run
```
### Debug the project
```bash
make debug
```
### Run flake8 and mypy
```bash
make lint
```
### Run flake8 and mypy in strict mode
```bash
make lint-strict
```
### Remove all temporary files
```bash
make clean
```
## Configuration File

The maze is configured through config.txt.

The configuration follows the following format:

- WIDTH=10
- HEIGHT=10
- ENTRY=0,0
- EXIT=9,9
- OUTPUT_FILE=maze.txt
- PERFECT=True
- SEED=42
### Configuration Parameters
- **WIDTH**: Width of the maze.
- **HEIGHT**: Height of the maze.
- **ENTRY**: Starting cell of the maze.
- **EXIT**: Destination cell of the maze.
- **OUTPUT_FILE**: File where the generated maze is exported.
- **PERFECT**: Determines whether a perfect maze should be generated.
- **SEED**: Seed used to make maze generation reproducible.

The configuration parser validates the values before the maze is generated.

## Algorithm — DFS

The purpose of Depth-First Search (DFS) in a maze is to systematically explore routes by diving as deep as possible down a single path until hitting a dead end, then backtracking to try alternative branches.

## Path Algorithm — BFS

To solve the shortest-path task, we implemented the BFS (breadth-first
search) algorithm. In each round, it takes one step in every possible
direction from the entry cell, storing each visited cell in a dictionary
that maps the cell to the cell it came from. This makes it straightforward
to reconstruct the shortest path as soon as the algorithm reaches the exit
cell.

## Reusability

The `mazegen` module is designed to be reusable in other projects. See the
[Instructions](#instructions) section above for details on installing and
using it.



## Team and Project Management
We are a team of two members, Shaden Shakhatreh and Shahed Yassin, we split the algorithms shahed worked solving in DFS and shaden did the  BFS and we worked together on all other parts of the project.

Our plan was to first understand the requirements, then develop, test, debug, and package the project. The plan evolved as we faced challenges during development.

Our teamwork and communication worked well. We could improve by planning testing and debugging time earlier.

We used Git/GitHub, VS Code, Python, Mypy, Flake8, Pytest, and Makefile.

## Resources
- https://aryanab.medium.com/maze-generation-recursive-backtracking-5981bc5cc766
- https://en.wikipedia.org/wiki/Box-drawing_characters
- https://www.geeksforgeeks.org/python/python-program-for-rat-in-a-maze-backtracking-2/

## AI Usage

We used AI tools, as a learning and development aid.