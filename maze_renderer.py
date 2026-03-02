import mlx

class MazeApp:
    def __init__(self):
        self.mlx = mlx.Mlx()
        self.mlx = None
        self.win = None

        #images
        self.maze_img = None
        self.button_img = None
        self.mlx = self.mlx_init()
    
    def mlx_init(self):
        self.mlx = self.mlx.mlx_init()
        print("hillow")


def maze_draw(maze):
    mazeApp = MazeApp()
