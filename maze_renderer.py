import mlx
import dimentions
import random
from typing import Any, cast
from mazegen.mazegen import Maze
import time


class img_data:
    def __init__(self, addr: bytearray, bits_per_pixel: int, size_line: int,
                 endian: int) -> None:
        """Initialize the image buffer with its memory
        address and pixel format properties."""
        self.addr = addr
        self.bits_per_pixel = bits_per_pixel
        self.size_line = size_line
        self.endian = endian

    def set_color_to_image(self, height: int, width: int, color: int) -> None:
        """Fill entire image with a single solid color."""
        for y in range(height):
            for x in range(width):
                self.put_pixel_fast(x, y, color)

    def put_pixel_fast(self, x: int, y: int, color: int) -> None:
        """Set the color of a single pixel at the given coordinates."""
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

    mlx: Any
    win: Any
    maze_obj: Any
    button_obj: Any
    maze_addr: img_data
    button_addr: img_data
    color: int
    currentx: int
    currenty: int
    maze: Maze
    mlx_ptr: Any
    is_animating: bool

    def __init__(self, maze: Maze) -> None:
        """Initialize the application window, images,
        and maze rendering components."""
        self.mlx_ptr = mlx.Mlx()
        self.mlx = None
        self.win = None
        self.maze = maze
        self.currentx = 0
        self.currenty = 0
        self.is_animating = True
        self.color = dimentions.colors[2]["base_wall_color"]

        # the actual MLX image object Required by (mlx_put_image_to_window,
        # redraw it later,to destroy it)
        self.maze_obj = cast(img_data, None)
        self.button_obj = cast(img_data, None)

        # memory
        self.maze_addr = cast(img_data, None)
        self.button_addr = cast(img_data, None)

        self.mlx_init()
        self.create_maze_img()
        self.create_button_img()

    def mlx_init(self) -> None:
        """Create the MLX instance and open the display window."""
        self.mlx = self.mlx_ptr.mlx_init()
        self.win = self.mlx_ptr.mlx_new_window(
            self.mlx, dimentions.window_x, dimentions.window_y, "A_MAZE_ING"
        )

    def create_maze_img(self) -> None:
        """Allocate the maze image buffer and fill it
        with the background color."""
        self.maze_obj = self.mlx_ptr.mlx_new_image(
            self.mlx, dimentions.image_maze_x, dimentions.image_maze_y
        )
        addr, bpp, size_line, endian = self.mlx_ptr.mlx_get_data_addr(
                    self.maze_obj)
        img = img_data(addr, bpp, size_line, endian)
        self.maze_addr = img
        self.maze_addr.set_color_to_image(
            dimentions.image_maze_y,
            dimentions.image_maze_x,
            dimentions.colors[0]["background"],
        )
        self.mlx_ptr.mlx_put_image_to_window(
            self.mlx, self.win, self.maze_obj, 0, 0)

    def create_button_img(self) -> None:
        """Allocate the button panel image
        buffer and draw the buttons onto it."""
        self.button_obj = self.mlx_ptr.mlx_new_image(
            self.mlx, dimentions.image_button_x, dimentions.image_button_y
        )
        addr, bpp, size_line, endian = self.mlx_ptr.mlx_get_data_addr(
            self.button_obj)
        img = img_data(addr, bpp, size_line, endian)
        self.button_addr = img
        self.button_addr.set_color_to_image(
            dimentions.image_button_y,
            dimentions.image_button_x,
            dimentions.colors[0]["background"],
        )
        self.button_draw()
        self.mlx_ptr.mlx_put_image_to_window(
            self.mlx, self.win, self.button_obj, dimentions.image_maze_x, 0
        )

    def button_draw(self) -> None:
        """Draw all buttons with their background
        color and centered label text."""
        start: int = dimentions.sep_top_button
        i: int = 0

        def draw_text(text: str, button_top: int) -> None:
            text = text.upper()

            scale = 2
            thickness = 2
            letter_spacing = scale * 6

            text_width = len(text) * letter_spacing
            button_width = 260
            button_left = 70

            startx = button_left + (button_width - text_width) // 2
            starty = button_top + (70 - (5 * scale)) // 2

            for char in text:
                if char not in dimentions.font:
                    startx += letter_spacing
                    continue

                l_font = dimentions.font[char]

                for y in range(5):
                    for x in range(5):
                        if l_font[y][x] == "X":
                            for dy in range(scale):
                                for dx in range(scale):
                                    for t in range(thickness):
                                        self.button_addr.put_pixel_fast(
                                            startx + x * scale + dx + t,
                                            starty + y * scale + dy,
                                            0xFFFFFF,
                                        )
                startx += letter_spacing

        for button in dimentions.buttons:
            dimentions.buttons[i]["start_y"] = start
            dimentions.buttons[i]["end_y"] = start + dimentions.button_hight
            for y in range(start, start + dimentions.button_hight):
                for x in range(
                    dimentions.buttons[i]["start_x"],
                    dimentions.buttons[i]["end_x"]
                ):
                    self.button_addr.put_pixel_fast(
                        x, y, dimentions.colors[1]["button_bg"]
                    )
            draw_text(dimentions.buttons[i]["text"], start)
            start += dimentions.sep_button
            i += 1

    def destroy_win(self, param: Any) -> None:
        """Close the window and exit the MLX event loop."""
        self.mlx_ptr.mlx_destroy_window(self.mlx, self.win)
        self.mlx_ptr.mlx_loop_exit(self.mlx)

    def upade_image_maze(self, param: Any) -> int:
        """Animate the maze drawing column by column,
        then render the path once complete."""
        if self.is_animating is False:
            return 0
        if self.maze.width <= 40 and self.maze.height <= 40:
            time.sleep(0.02)
        startx = int(
            (dimentions.image_maze_x -
             (self.maze.width * self.maze.cell_size)) / 2
        )
        starty = int(
            (dimentions.image_maze_y -
             (self.maze.height * self.maze.cell_size)) / 2
        )

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
                            startx + (x * self.maze.cell_size) +
                            self.maze.cell_size
                        ):
                            for j in range(self.maze.wall_size):
                                self.maze_addr.put_pixel_fast(
                                    i, y + j, self.color)

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
                            (y * self.maze.cell_size) + starty +
                            self.maze.cell_size
                        ):
                            for j in range(self.maze.wall_size):
                                self.maze_addr.put_pixel_fast(
                                    x + j, i, self.color)

        if (self.currentx >= self.maze.width and
                self.currenty >= self.maze.height):
            for y in range(0, self.maze.height):
                if self.maze.cells[y][self.maze.width - 1].walls["E"] is True:
                    for i in range(
                        starty + (y * self.maze.cell_size),
                        (y * self.maze.cell_size) + starty +
                        self.maze.cell_size
                    ):
                        for j in range(self.maze.wall_size):
                            self.maze_addr.put_pixel_fast(
                                startx +
                                (self.maze.width * self.maze.cell_size) + j,
                                i,
                                self.color
                            )
            for x in range(0, self.maze.width):
                for i in range(
                    startx + (x * self.maze.cell_size),
                    startx + (x * self.maze.cell_size) + self.maze.cell_size,
                ):
                    for j in range(self.maze.wall_size):
                        self.maze_addr.put_pixel_fast(
                            i,
                            starty + (self.maze.height * self.maze.cell_size)
                            + j,
                            self.color,
                        )
            # draw entry and exit point
            for eny in range(
                starty + (entryy * self.maze.cell_size),
                starty + ((entryy + 1) * self.maze.cell_size),
            ):
                for enx in range(
                    startx + (entryx * self.maze.cell_size),
                    startx + ((entryx + 1) * self.maze.cell_size),
                ):
                    self.maze_addr.put_pixel_fast(
                        enx, eny, dimentions.colors[4]["entry"]
                    )
            for eny in range(
                starty + (exity * self.maze.cell_size),
                starty + ((exity + 1) * self.maze.cell_size),
            ):
                for enx in range(
                    startx + (exitx * self.maze.cell_size),
                    startx + ((exitx + 1) * self.maze.cell_size),
                ):
                    self.maze_addr.put_pixel_fast(
                        enx, eny, dimentions.colors[5]["exit"]
                    )
            self.maze.bfs_algo()
            self.path_draw()
            self.is_animating = False
        self.mlx_ptr.mlx_put_image_to_window(
            self.mlx, self.win, self.maze_obj, 0, 0)

        if self.currentx < self.maze.width:
            self.currentx += 1
        if self.currenty < self.maze.height:
            self.currenty += 1
        return 1

    def path_draw(self) -> None:
        """Highlight the solution path through the maze."""
        self.maze.is_path_draw = True
        startx = int(
            (dimentions.image_maze_x -
             (self.maze.width * self.maze.cell_size)) / 2
        )
        starty = int(
            (dimentions.image_maze_y -
             (self.maze.height * self.maze.cell_size)) / 2
        )
        border = self.maze.wall_size * 2 if self.maze.cell_size > 6 else 1
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
            self.mlx, self.win, self.maze_obj, 0, 0)

    def clear_image(self) -> None:
        """Erase the maze area by filling it with the background color."""
        width = int((800 - (self.maze.width * self.maze.cell_size)) / 2)
        height = int((800 - (self.maze.height * self.maze.cell_size)) / 2)
        for i in range(height + (self.maze.cell_size * self.maze.height)):
            for j in range(width + (self.maze.cell_size * self.maze.width)):
                self.maze_addr.put_pixel_fast(
                    j, i, dimentions.colors[0]["background"])

    def draw_maze_without_animation(self) -> None:
        """Redraw the full maze instantly without any animation."""
        self.clear_image()
        startx = int(
            (dimentions.image_maze_x -
             (self.maze.width * self.maze.cell_size)) / 2
        )
        starty = int(
            (dimentions.image_maze_y -
             (self.maze.height * self.maze.cell_size)) / 2
        )

        entryx, entryy = self.maze.entry
        exitx, exity = self.maze.exit

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
                        startx + (x * self.maze.cell_size) +
                        self.maze.cell_size
                    ):
                        for j in range(self.maze.wall_size):
                            self.maze_addr.put_pixel_fast(i, y + j, self.color)

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
                        (y * self.maze.cell_size) + starty +
                        self.maze.cell_size
                    ):
                        for j in range(self.maze.wall_size):
                            self.maze_addr.put_pixel_fast(x + j, i, self.color)

        for y in range(0, self.maze.height):
            if self.maze.cells[y][self.maze.width - 1].walls["E"] is True:
                for i in range(
                    starty + (y * self.maze.cell_size),
                    (y * self.maze.cell_size) + starty + self.maze.cell_size,
                ):
                    for j in range(self.maze.wall_size):
                        self.maze_addr.put_pixel_fast(
                            startx +
                            (self.maze.width * self.maze.cell_size) + j,
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
            # draw entry and exit point
        for eny in range(
            starty + (entryy * self.maze.cell_size),
            starty + ((entryy + 1) * self.maze.cell_size),
        ):
            for enx in range(
                startx + (entryx * self.maze.cell_size),
                startx + ((entryx + 1) * self.maze.cell_size),
            ):
                self.maze_addr.put_pixel_fast(enx, eny,
                                              dimentions.colors[4]["entry"])
        for eny in range(
            starty + (exity * self.maze.cell_size),
            starty + ((exity + 1) * self.maze.cell_size),
        ):
            for enx in range(
                startx + (exitx * self.maze.cell_size),
                startx + ((exitx + 1) * self.maze.cell_size),
            ):
                self.maze_addr.put_pixel_fast(enx, eny,
                                              dimentions.colors[5]["exit"])
        self.mlx_ptr.mlx_put_image_to_window(self.mlx,
                                             self.win, self.maze_obj, 0, 0)

    def clicked_button(self, button: int, x: int, y: int, data: Any) -> None:
        """Handle mouse click events and trigger the
        corresponding button action."""
        i = 0
        while i < 4:
            if (
                x >= dimentions.buttons[i]["start_x"]
                and x <= dimentions.buttons[i]["end_x"]
            ):
                if (
                    y >= dimentions.buttons[i]["start_y"]
                    and y <= dimentions.buttons[i]["end_y"]
                ):
                    if dimentions.buttons[i]["text"] == "regenerate maze":
                        self.maze_addr.set_color_to_image(
                            800, 800, dimentions.colors[0]["background"]
                        )
                        self.maze.reset_maze()
                        self.maze.my_42()
                        if self.maze.algo == "wilson":
                            self.maze.wilson_algo()
                        else:
                            self.maze.dsf_algorith()
                        self.maze.not_perfect()
                        self.currentx = 0
                        self.currenty = 0
                        self.is_animating = True
                        break
                    elif dimentions.buttons[i]["text"] == "change color":
                        self.maze_addr.set_color_to_image(
                            800, 800, dimentions.colors[0]["background"]
                        )
                        self.color = random.choice(
                            dimentions.colors[3]["wall_colors"])
                        self.currentx = 0
                        self.currenty = 0
                        self.is_animating = True
                        break
                    elif dimentions.buttons[i]["text"] == "show or hide path":
                        if self.maze.is_path_draw is True:
                            self.draw_maze_without_animation()
                            self.maze.is_path_draw = False
                        else:
                            self.path_draw()
                            self.maze.is_path_draw = True
                    elif dimentions.buttons[i]["text"] == "change algorithm":
                        self.maze_addr.set_color_to_image(
                            800, 800, dimentions.colors[0]["background"]
                        )
                        self.maze.reset_maze()
                        self.maze.my_42()
                        if self.maze.algo == "dfs":
                            self.maze.algo = "wilson"
                            self.maze.wilson_algo()
                        else:
                            self.maze.algo = "dfs"
                            self.maze.dsf_algorith()
                        self.maze.not_perfect()
                        self.currentx = 0
                        self.currenty = 0
                        self.is_animating = True
                        break
            i += 1


def check_entry_exit(maze: Maze) -> int:
    """Verify that the entry and exit points do
    not overlap with the 42 pattern."""
    x_entry, y_entry = maze.entry
    x_exit, y_exit = maze.exit
    entry = [True for t in maze.fourty_two
             if t.row == x_entry and t.column == y_entry]
    exit = [True for t in maze.fourty_two
            if t.row == x_exit and t.column == y_exit]
    if entry.__len__() != 0:
        print("entry point is in the 42 !!")
        return 0
    elif exit.__len__() != 0:
        print("exit point is in the 42 !!")
        return 0
    return 1


def maze_draw(maze: Maze) -> int:
    """Set up and launch the maze application, running the MLX event loop."""
    maze.my_42()
    if check_entry_exit(maze):
        mazeApp = MazeApp(maze)
        mazeApp.maze.dsf_algorith()
        mazeApp.maze.not_perfect()
        mazeApp.mlx_ptr.mlx_hook(
            mazeApp.win, 33, 0, mazeApp.destroy_win, None)
        mazeApp.mlx_ptr.mlx_loop_hook(
            mazeApp.mlx, mazeApp.upade_image_maze, None)
        mazeApp.mlx_ptr.mlx_mouse_hook(
            mazeApp.win, mazeApp.clicked_button, None)
        mazeApp.mlx_ptr.mlx_loop(mazeApp.mlx)
    return 0
