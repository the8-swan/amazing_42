import sys
import config_validation
from maze import Maze

def main():
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
                print(data)
                maze = Maze(data)
                maze.my_42()
                maze.dsf_algorith(0, 0)
                maze_renderer.maze_draw(maze)
        except (FileNotFoundError, config_validation.ErrorInConfigFile) as e:
            print(e)


if __name__ == "__main__":
    main()
