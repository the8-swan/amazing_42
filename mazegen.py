from collections import deque
import random
from config_validation import ErrorInConfigFile
import os
from typing import Dict, List, Tuple, Optional, Deque, Any


class Maze:
    direction: dict[str, tuple[int, int, str, str]] = {
        "N": (0, -1, "N", "S"),
        "S": (0, +1, "S", "N"),
        "W": (-1, 0, "W", "E"),
        "E": (+1, 0, "E", "W"),
    }

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize the maze with dimensions, entry/exit points,
        and an empty grid of cells."""

        self.width: int = data["WIDTH"]
        self.height: int = data["HEIGHT"]
        self.entry: Tuple[int, int] = data["ENTRY"]
        self.exit: Tuple[int, int] = data["EXIT"]
        self.out_file: str = data["OUTPUT_FILE"]
        self.cell_size: int = self.calc_cell_size()
        self.wall_size: int = self.celc_wall_size()
        self.path: Deque[Tuple[int, int]] = deque()
        self.is_path_draw: bool = False
        self.perfect: bool = data["PERFECT"]
        self.dirs: List[str] = []
        self.fourty_two: List["Maze.Cell"] = []
        self.draw_42: bool = True
        self.seed: Optional[int] = data["SEED"] if data["SEED"] else None
        # cells[row][col]
        self.cells: List[List["Maze.Cell"]] = self.create_cells(self.width,
                                                                self.height)
        self.algo: str = "dfs"
        if self.seed is not None:
            random.seed(self.seed)

    class Cell:
        def __init__(self, row: int, column: int) -> None:
            """Initialize the maze with dimensions, entry/exit points,
            and an empty grid of cells."""
            self.row: int = row
            self.column: int = column
            self.walls: Dict[str, bool] = {"S": True, "N": True,
                                           "W": True, "E": True}
            self.is_visited: bool = False

    def create_cells(self, width: int, height: int) -> List[List["Maze.Cell"]]:
        """Build and return the 2D grid of cells for the maze."""
        cells: List[List["Maze.Cell"]] = []
        for col in range(height):
            row_data: List["Maze.Cell"] = []
            for row in range(width):
                row_data.append(self.Cell(row, col))
            cells.append(row_data)
        return cells

    def celc_wall_size(self) -> int:
        """Determine the wall thickness based on the cell size."""
        if self.cell_size <= 10:
            return 1
        return 2

    def calc_cell_size(self) -> int:
        """Calculate the appropriate cell size so the maze
        fits within the display window."""
        cell_size: int = 25
        while cell_size * self.width >= 800:
            cell_size -= 1
            if cell_size == 0:
                raise ErrorInConfigFile("cell_size <0")
        while cell_size * self.height >= 800:
            cell_size -= 1
            if cell_size == 0:
                raise ErrorInConfigFile("cell_size <0")
        return cell_size

    def my_42(self) -> None:
        """Pre-mark a pattern of cells in the shape of '42'
        at the center of the maze."""
        if self.width > 15 and self.height > 15:
            cells: int = max(1, 20 // self.cell_size)
            middle_w: int = int(self.width / 2)
            middle_h: int = int(self.height / 2)
            start: int = max(1, cells // 4)
            for i in range(start, cells * 4):
                for j in range(cells):
                    self.cells[middle_h + j][middle_w - i].is_visited = True
                    self.cells[middle_h + j][middle_w + i].is_visited = True
                    self.cells[middle_h - (3 * cells) + j][
                        middle_w + i
                    ].is_visited = True
                    self.cells[middle_h + (3 * cells) + j][
                        middle_w + i
                    ].is_visited = True
                    self.fourty_two.append(
                        self.cells[middle_h + j][middle_w - i])
                    self.fourty_two.append(
                        self.cells[middle_h + j][middle_w + i])
                    self.fourty_two.append(
                        self.cells[middle_h - (3 * cells) + j][middle_w + i]
                    )
                    self.fourty_two.append(
                        self.cells[middle_h + (3 * cells) + j][middle_w + i]
                    )

            for i in range(0, 4 * cells):
                for j in range(1, cells + 1):
                    self.cells[middle_h + i][middle_w + j].is_visited = True
                    self.cells[middle_h][middle_w - j].is_visited = True
                    self.cells[middle_h - (3 * cells) + i][
                        middle_w + (3 * cells) + j
                    ].is_visited = True
                    self.cells[middle_h - (3 * cells) + i][
                        middle_w - (3 * cells) - j
                    ].is_visited = True
                    self.fourty_two.append(
                        self.cells[middle_h + i][middle_w + j])
                    self.fourty_two.append(self.cells[middle_h][middle_w - j])
                    self.fourty_two.append(
                        self.cells[middle_h - (3 * cells) + i][
                            middle_w + (3 * cells) + j
                        ]
                    )
                    self.fourty_two.append(
                        self.cells[middle_h - (3 * cells) + i][
                            middle_w - (3 * cells) - j
                        ]
                    )

            for i in range(0, 4 * cells):
                for j in range(1, 1 + cells):
                    self.cells[middle_h + i][middle_w - j].is_visited = True
                    self.fourty_two.append(
                        self.cells[middle_h - i][middle_w - j])
        else:
            print("42 will not be drawn !!")

    def dsf_algorith(self) -> None:
        """Generate the maze using a depth-first search
        algorithm with backtracking."""
        stack: List[Tuple[int, int]] = []
        x: int
        y: int
        x, y = 0, 0

        self.cells[y][x].is_visited = True
        stack.append((x, y))
        while stack:
            x, y = stack[-1]
            key: list[str] = list(self.direction.keys())
            random.shuffle(key)
            found: bool = False
            i: int = 0
            while i < 4:
                m_x: int
                m_y: int
                m_dir: str
                n_dir: str
                m_x, m_y, m_dir, n_dir = self.direction[key[i]]
                n_x: int = x + m_x
                n_y: int = y + m_y
                if 0 <= n_x < self.width and 0 <= n_y < self.height:
                    if not self.cells[n_y][n_x].is_visited:
                        self.cells[y][x].walls[m_dir] = False
                        self.cells[n_y][n_x].walls[n_dir] = False
                        self.cells[n_y][n_x].is_visited = True
                        stack.append((n_x, n_y))
                        found = True
                        break
                i += 1
            if not found:
                stack.pop()

    def reset_maze(self) -> None:
        """Reset all cells to their initial state with all walls
        intact and unvisited."""
        for row in self.cells:
            for cell in row:
                cell.is_visited = False
                cell.walls = {"S": True, "N": True, "W": True, "E": True}

    def output_maze(self) -> None:
        """Write the maze structure, entry, exit,
        and solution path to the output file."""
        os.makedirs("output", exist_ok=True)
        with open("output/"+self.out_file, 'w') as f:
            for i in range(self.height):
                for j in range(self.width):
                    count: int = 0
                    if self.cells[i][j].walls['N']:
                        count += 1
                    if self.cells[i][j].walls['S']:
                        count += 4
                    if self.cells[i][j].walls['E']:
                        count += 2
                    if self.cells[i][j].walls['W']:
                        count += 8
                    h = format(count, "X")
                    f.write(h)
                f.write("\n")
            f.write("\n")
            x: int
            y: int
            x, y = self.entry
            m_x: int
            m_y: int
            m_x, m_y = self.exit
            f.write(f"{x},{y}\n")
            f.write(f"{m_x},{m_y}\n")
            for dir_char in self.dirs:
                f.write(dir_char)

    def not_perfect(self) -> None:
        """Introduce random wall removals to create loops
        and make the maze imperfect."""
        if self.perfect is False:
            unvisited: list[tuple[int, int]] = []
            n_dir: str = ""
            dirs: list[str] = ['E', 'W', 'N', 'S']
            w: int = self.width
            h: int = self.height

            wall: int = int(w * h * 0.01)

            for r in range(h):
                for c in range(w):
                    unvisited.append((c, r))

            while wall != 0 and unvisited:
                x: int
                y: int
                x, y = random.choice(unvisited)
                unvisited.remove((x, y))

                count: int = 0
                for dir_key in dirs:
                    if self.cells[y][x].walls[dir_key]:
                        count += 1
                found: bool = True
                i: int = 0
                while i < 4 and found:
                    m_x: int
                    m_y: int
                    m_x, m_y, _, _ = self.direction[dirs[i]]
                    n_x: int = m_x + x
                    n_y: int = m_y + y
                    if 0 <= n_x < w and 0 <= n_y < h:
                        num: int = 0
                        for j in dirs:
                            if self.cells[n_y][n_x].walls[j]:
                                num += 1
                        if num == 4:
                            found = False
                            n_dir = dirs[i]
                    i += 1

                d = random.choice(dirs)
                if (self.cells[y][x].walls[d]
                        and (x != 0 or d != 'W')
                        and (x != w-1 or d != 'E')
                        and (y != 0 or d != 'N')
                        and (y != h-1 or d != 'S')
                        and 0 < count <= 2):
                    if found or (not found and n_dir != d):

                        self.cells[y][x].walls[d] = False
                        wall -= 1

    def wilson_algo(self) -> None:
        """Generate the maze using Wilson's algorithm with
        loop-erased random walks."""
        unvisited: list[tuple[int, int]] = []
        visited: list[tuple[int, int]] = []

        for r in range(self.height):
            for c in range(self.width):
                if self.cells[r][c].is_visited:
                    visited.append((c, r))

        for r in range(self.height):
            for c in range(self.width):
                if not self.cells[r][c].is_visited:
                    unvisited.append((c, r))
        x: int
        y: int
        x, y = random.choice(unvisited)
        self.cells[y][x].is_visited = True
        unvisited.remove((x, y))

        while unvisited:
            path: list[tuple[int, int]] = []
            x, y = random.choice(unvisited)
            path.append((x, y))

            while not self.cells[y][x].is_visited:

                key: str = random.choice(list(self.direction.keys()))
                d_x: int
                d_y: int
                d_x, d_y, _, _ = self.direction[key]
                n_x: int = x + d_x
                n_y: int = y + d_y

                if 0 <= n_x < self.width and 0 <= n_y < self.height:
                    if (n_x, n_y) not in visited:
                        if (n_x, n_y) in path:
                            index = path.index((n_x, n_y))
                            path = path[:index+1]
                        else:
                            path.append((n_x, n_y))
                        x, y = n_x, n_y

            for i in range(len(path)-1):

                x, y = path[i]
                n_x, n_y = path[i+1]

                if (x+1, y) == (n_x, n_y):
                    self.cells[y][x].walls['E'] = False
                    self.cells[n_y][n_x].walls['W'] = False
                elif (x-1, y) == (n_x, n_y):
                    self.cells[y][x].walls['W'] = False
                    self.cells[n_y][n_x].walls['E'] = False
                elif (x, y+1) == (n_x, n_y):
                    self.cells[y][x].walls['S'] = False
                    self.cells[n_y][n_x].walls['N'] = False
                elif (x, y-1) == (n_x, n_y):
                    self.cells[y][x].walls['N'] = False
                    self.cells[n_y][n_x].walls['S'] = False

                if not self.cells[y][x].is_visited:
                    self.cells[y][x].is_visited = True
                    if (x, y) in unvisited:
                        unvisited.remove((x, y))

            l_x: int
            l_y: int
            l_x, l_y = path[0]
            if not self.cells[l_y][l_x].is_visited:
                self.cells[l_y][l_x].is_visited = True
                if (l_x, l_y) in unvisited:
                    unvisited.remove((l_x, l_y))

    def bfs_algo(self) -> None:
        """Find the shortest path from entry to exit
        using breadth-first search."""
        for r in range(len(self.cells)):
            for c in range(len(self.cells[0])):
                self.cells[r][c].is_visited = False
        x: int
        y: int
        d_x: int
        d_y: int
        x, y = self.entry
        d_x, d_y = self.exit

        queue: deque[tuple[int, int]] = deque()
        queue.append((x, y))
        data: deque[tuple[int, int]] = deque()
        self.cells[y][x].is_visited = True

        parent: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

        found: bool = False

        while queue:
            x, y = queue.popleft()

            if x == d_x and y == d_y:
                found = True
                break

            key: list[str] = list(self.direction.keys())

            i = 0
            while i < 4:
                n_x: int
                n_y: int
                m_dir: str
                n_dir: str
                n_x, n_y, m_dir, n_dir = self.direction[key[i]]
                m_x: int = x + n_x
                m_y: int = y + n_y

                if 0 <= m_x < self.width and 0 <= m_y < self.height:
                    if (not self.cells[y][x].walls[m_dir]
                            and not self.cells[m_y][m_x].walls[n_dir]
                            and not self.cells[m_y][m_x].is_visited):
                        self.cells[m_y][m_x].is_visited = True
                        parent[(m_x, m_y)] = ((x, y), m_dir)
                        queue.append((m_x, m_y))

                i += 1

        if not found:
            return None

        cur: tuple[int, int] = self.exit

        while cur != self.entry:
            (m_x, m_y), d = parent[cur]

            if (m_x, m_y) != self.entry:
                data.appendleft((m_x, m_y))

            x, y = cur
            cur = (m_x, m_y)
            self.dirs.append(d)

        x, y = self.entry

        self.dirs.reverse()

        self.path = data
