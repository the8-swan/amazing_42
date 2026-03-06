This project has been created as part of the 42 curriculum by obakri, ikabboud.*

# A-Maze-ing

## Description

a_maze_ing is a project that aims to create an interactive maze and pathfinding visualization tool built from scratch using the Python programming language and the MiniLibX library. The project demonstrates advanced algorithm implementation, low-level graphics programming, and real-time animation rendering.

The program takes a configuration file as input, generates a maze according to the given parameters, displays it graphically with interactive controls, and writes the result to an output file using a hexadecimal wall encoding.

## Instructions

### Requirements

- Python 3.10 or later
- MiniLibX library
- pip or any compatible package manager

### Installation
```bash
make install
```

### Run
```bash
make run
```

or directly:
```bash
python3 a_maze_ing.py config.txt
```

### Debug
```bash
make debug
```

### Lint
```bash
make lint
```

### Clean
```bash
make clean
```

### Configuration file format

The configuration file must contain one `KEY=VALUE` pair per line. Lines starting with `#` are treated as comments and ignored.

| Key | Description | Example |
|---|---|---|
| WIDTH | Maze width in number of cells | WIDTH=20 |
| HEIGHT | Maze height in number of cells | HEIGHT=15 |
| ENTRY | Entry coordinates (x,y) | ENTRY=0,0 |
| EXIT | Exit coordinates (x,y) | EXIT=19,14 |
| OUTPUT_FILE | Name of the output file | OUTPUT_FILE=maze.txt |
| PERFECT | Whether the maze is perfect | PERFECT=True |
| SEED | Optional seed for reproducibility | SEED=42 |

A default configuration file `config.txt` is available at the root of the repository.

## Maze Generation Algorithms

### DFS (Depth-First Search)

Depth-First Search generates mazes by exploring paths as deeply as possible before backtracking. It picks random unvisited neighbors, removes walls between cells, and uses a stack to backtrack when stuck, creating a perfect maze with long winding corridors. It is fast (O(n)), simple to implement, and widely used in maze-based games.

By default the DFS algorithm is used to generate the maze. The user can switch to Wilson's algorithm at runtime by clicking the "change algorithm" button.

We chose DFS as the default because it is fast, memory-efficient, and produces visually interesting mazes with long corridors that are satisfying to navigate.

### Wilson's Algorithm

Wilson's algorithm generates mazes through loop-erased random walks. Starting from an unvisited cell, a random walk is performed until it reaches the existing maze structure. Any loops the path crosses are erased before the path is carved into the maze. This produces completely unbiased mazes where all possible configurations are equally likely, unlike DFS which tends to favor long corridors. It is slower but guarantees perfect uniformity in maze generation.

## Reusable Module

The maze generation logic is packaged as a standalone installable Python module. The package is called `mazegen` and the built file (`.whl`) is located at the root of the repository.

### What is reusable

The `Maze` class inside `mazegen.py` is fully self-contained and independent of the graphical interface. It handles maze generation, pathfinding, and output. It can be imported and used in any Python project.

### Installation
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage
```python
from mazegen import Maze

data = {
    "WIDTH": 20,
    "HEIGHT": 15,
    "ENTRY": (0, 0),
    "EXIT": (19, 14),
    "OUTPUT_FILE": "maze.txt",
    "PERFECT": True,
    "SEED": 42
}

maze = Maze(data)
maze.dsf_algorith()
maze.bfs_algo()

# Access the cell grid
print(maze.cells[0][0].walls)

# Access the solution path
print(maze.path)

# Write to output file
maze.output_maze()
```

### Custom parameters

- Change `WIDTH` and `HEIGHT` to control maze dimensions.
- Set `SEED` to any integer for reproducible results.
- Set `PERFECT` to `True` for a maze with exactly one path between entry and exit, or `False` to introduce random wall removals creating loops.

### Building the package from source
```bash
python -m venv venv
source venv/bin/activate
pip install build
python -m build
```

The output will be in the `dist/` folder.

## Team and Project Management

### Roles

**ikabboud** was responsible for implementing the generation algorithms (DFS and Wilson's), the BFS pathfinding, the perfect/imperfect maze logic, and the output file generation.

**obakri** was responsible for the graphical interface using MiniLibX, the configuration file parsing, the Makefile, and this README.

### Planning

We started by splitting the project into two independent parts: the generation/logic side and the graphical/interface side. This allowed us to work in parallel. The initial plan was to finish the core generation first and integrate the renderer after, which worked well in practice. Toward the end we focused on integration, type hints, packaging, and linting, which took more time than expected.

### What worked well and what could be improved

The separation of responsibilities between generation and rendering worked well and kept the code clean. Communication was consistent throughout the project. If we had more time, we would improve the animation smoothness, add more algorithm options, and write unit tests to cover edge cases more thoroughly.

### Tools used

- Python 3.10
- MiniLibX (graphical rendering)
- mypy (static type checking)
- flake8 (code style)

## Resources

- [Maze generation algorithms - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Wilson's algorithm explained](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Wilson's_algorithm)
- [Depth-first search - Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Breadth-first search - Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [MiniLibX documentation](https://harm-smits.github.io/42docs/libs/minilibx)
- [Python typing module - docs.python.org](https://docs.python.org/3/library/typing.html)
- [PEP 257 - Docstring conventions](https://peps.python.org/pep-0257/)
- [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

### AI usage

Claude AI was used to assist with the following tasks:
- Understanding some complex concepts . 
- Correcting docstrings for some functions and classes
- Structuring this README
- Advising on the Python packaging setup (pyproject.toml structure)


Made by ❤️