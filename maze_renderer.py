import mlx
import dimentions


class img_data:
    def __init__(self, addr, bits_per_pixel, size_line, endian):
        self.addr = addr
        self.bits_per_pixel = bits_per_pixel
        self.size_line = size_line
        self.endian = endian

    def set_color_to_image(self, height, width, color: int):
        """Fill entire image with a solid color."""
        for y in range(height):
            for x in range(width):
                self.put_pixel_fast(x, y, color)

    def put_pixel_fast(self, x: int, y: int, color: int):
        """Set a single pixel color."""
        bytes_per_pixel = self.bits_per_pixel // 8

        # Calculate byte offset in flat array
        # size_line is bytes per row (may include padding)
        row_offset = y * self.size_line
        pixel_offset = x * bytes_per_pixel
        index = row_offset + pixel_offset

        # Assign color components (BGRA format)
        self.addr[index + 0] = color & 0xFF  # Blue
        self.addr[index + 1] = (color >> 8) & 0xFF  # Green
        self.addr[index + 2] = (color >> 16) & 0xFF  # Red
        if bytes_per_pixel == 4:
            self.addr[index + 3] = (
                (color >> 24) & 0xFF if (color >> 24) else 0xFF
            )  # Alpha

class MazeApp:
    def __init__(self, maze):
        self.mlx_ptr = mlx.Mlx()
        self.mlx = None
        self.win = None
        self.maze = maze
        self.currentx = 0
        self.currenty = 0
        self.is_animating = True
        self.color = dimentions.colors[2]["base_wall_color"]

        #the actual MLX image object Required by (mlx_put_image_to_window,redraw it later,to destroy it)
        self.maze_obj = None
        self.button_obj = None

        #memory 
        self.maze_addr = None
        self.button_addr = None

        self.mlx_init()
        self.create_maze_img()
        self.create_button_img()

    def mlx_init(self):
        self.mlx = self.mlx_ptr.mlx_init()
        self.win = self.mlx_ptr. mlx_new_window(self.mlx, dimentions.window_x, dimentions.window_y, "A_MAZE_ING")
    
    def create_maze_img(self):
        self.maze_obj = self.mlx_ptr.mlx_new_image(self.mlx, dimentions.image_maze_x, dimentions.image_maze_y)
        addr, bpp, size_line, endian = self.mlx_ptr.mlx_get_data_addr(self.maze_obj)
        img = img_data(addr, bpp, size_line, endian)
        self.maze_addr = img
        self.maze_addr.set_color_to_image(dimentions.image_maze_y, dimentions.image_maze_x, dimentions.colors[0]["background"])
        self.mlx_ptr.mlx_put_image_to_window(self.mlx, self.win, self.maze_obj, 0, 0)

    def create_button_img(self):
        self.button_obj = self.mlx_ptr.mlx_new_image(self.mlx, dimentions.image_button_x, dimentions.image_button_y)
        addr, bpp, size_line, endian = self.mlx_ptr.mlx_get_data_addr(self.button_obj)
        img = img_data(addr, bpp, size_line, endian)
        self.button_addr = img
        self.button_addr.set_color_to_image(dimentions.image_button_y, dimentions.image_button_x, dimentions.colors[0]["background"])
        self.mlx_ptr.mlx_put_image_to_window(self.mlx, self.win, self.button_obj, dimentions.image_maze_x, 0)

    def destroy_win(self, param):
        self.mlx_ptr.mlx_destroy_window(self.mlx, self.win)
        self.mlx_ptr.mlx_loop_exit(self.mlx)
    
    def upade_image_maze(self, param):
        if self.is_animating is False:
            return 0
        startx = int((dimentions.image_maze_x - (self.maze.width * self.maze.cell_size)) / 2)
        starty = int((dimentions.image_maze_y - (self.maze.height * self.maze.cell_size)) / 2)
    
        entryx, entryy = self.maze.entry
        exitx, exity = self.maze.exit     

        if self.currenty <= self.maze.height:
            for y in range(
                starty,
                (self.maze.height * self.maze.cell_size) + starty,
                self.maze.cell_size,
            ):
                yn = int((y - starty) / self.maze.cell_size)
                for x in range(0, self.currentx):
                    if self.maze.cells[yn][x].walls["N"] is True:
                        for i in range(
                            startx + (x * self.maze.cell_size),
                            startx + (x * self.maze.cell_size) + self.maze.cell_size,
                        ):
                            for j in range(self.maze.wall_size):
                                self.maze_addr.put_pixel_fast(i, y + j, self.color)
        
        if self.currentx <= self.maze.width:
            for x in range(
                startx,
                (self.maze.width * self.maze.cell_size) + startx,
                self.maze.cell_size,
            ):
                xn = int((x - startx) / self.maze.cell_size)
                for y in range(0, self.currenty):
                    if self.maze.cells[y][xn].walls["W"] is True:
                        for i in range(
                            starty + (y * self.maze.cell_size),
                            (y * self.maze.cell_size) + starty + self.maze.cell_size,
                        ):
                            for j in range(self.maze.wall_size):
                                self.maze_addr.put_pixel_fast(x + j, i, self.color)

        if self.currentx >= self.maze.width and self.currenty >= self.maze.height:
            for y in range(0, self.maze.height):
                if self.maze.cells[y][self.maze.width - 1].walls["E"] is True:
                    for i in range(
                        starty + (y * self.maze.cell_size),
                        (y * self.maze.cell_size) + starty + self.maze.cell_size,
                    ):
                        for j in range(self.maze.wall_size):
                            self.maze_addr.put_pixel_fast(
                                startx + (self.maze.width * self.maze.cell_size) + j,
                                i,
                                self.color,
                            )
            for x in range(0, self.maze.width):
                for i in range(
                    startx + (x * self.maze.cell_size),
                    startx + (x * self.maze.cell_size) + self.maze.cell_size,
                ):
                    for j in range(self.maze.wall_size):
                        self.maze_addr.put_pixel_fast(
                            i,
                            starty + (self.maze.height * self.maze.cell_size) + j,
                            self.color,
                        )
            #draw entry and exit point
            for eny in range(
                starty + (entryy * self.maze.cell_size),
                starty + ((entryy + 1) * self.maze.cell_size),
            ):
                for enx in range(
                    startx + (entryx * self.maze.cell_size),
                    startx + ((entryx + 1) * self.maze.cell_size),
                ):
                    self.maze_addr.put_pixel_fast(enx, eny, dimentions.colors[4]["entry"])
            for eny in range(
                starty + (exity * self.maze.cell_size),
                starty + ((exity + 1) * self.maze.cell_size),
            ):
                for enx in range(
                    startx + (exitx * self.maze.cell_size),
                    startx + ((exitx + 1) * self.maze.cell_size),
                ):
                    self.maze_addr.put_pixel_fast(enx, eny, dimentions.colors[5]["exit"])
            self.maze.bfs_algo()
            self.path_draw()
            self.is_animating = False
        self.mlx_ptr.mlx_put_image_to_window(
        self.mlx, self.win, self.maze_obj, 0, 0)

        if self.currentx < self.maze.width:
            self.currentx += 1
        if self.currenty < self.maze.height:
            self.currenty += 1

    def path_draw(self):
        print(self.maze.path)
        self.maze.is_path_draw = True
        startx = int((dimentions.image_maze_x - (self.maze.width * self.maze.cell_size)) / 2)
        starty = int((dimentions.image_maze_y - (self.maze.height * self.maze.cell_size)) / 2)
        border = self.maze.wall_size * 2
        color = dimentions.colors[6]["path_color"]
        for data in self.maze.path:
            x, y = data

            cell_left = startx + (x * self.maze.cell_size) + border
            cell_top = starty + (y * self.maze.cell_size) + border
            cell_right = startx + ((x + 1) * self.maze.cell_size) - border
            cell_bottom = starty + ((y + 1) * self.maze.cell_size) - border

            for py in range(cell_top, cell_bottom):
                for px in range(cell_left, cell_right):
                    self.maze_addr.put_pixel_fast(px, py, color)
        self.mlx_ptr.mlx_put_image_to_window(
            self.mlx, self.win, self.maze_obj, 0, 0
        )





def maze_draw(maze):
    mazeApp = MazeApp(maze)

    mazeApp.mlx_ptr.mlx_hook(mazeApp.win, 33, 0, mazeApp.destroy_win, None)
    mazeApp.mlx_ptr.mlx_loop_hook(mazeApp.mlx, mazeApp.upade_image_maze, None)
    mazeApp.mlx_ptr.mlx_loop(mazeApp.mlx)