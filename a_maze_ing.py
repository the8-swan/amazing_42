import sys
import config_validation
from mazegen import Maze
from maze_renderer import maze_draw


def main() -> None:
    """Read the config file path from the command line, validate it,
    generate the maze, and launch the renderer."""
    args = sys.argv[1:]
    if args.__len__() > 1:
        print("Too many files , make sure to enter one file !!")
    elif args.__len__() < 1:
        print("You forgot to mention the config file !!")
    else:
        try:
            with open(sys.argv[1], "r") as file:
                content = file.read()
                data = config_validation.validation(content)
                maze = Maze(data)
                if maze_draw(maze):
                    maze.output_maze()
        except (FileNotFoundError, config_validation.ErrorInConfigFile) as e:
            print(e)


if __name__ == "__main__":
    main()
