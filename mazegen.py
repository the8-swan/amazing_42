from collections import deque
import random
from config_validation import ErrorInConfigFile
import os


class Maze:
    direction = {
        "N": (0, -1, "N", "S"),
        "S": (0, +1, "S", "N"),
        "W": (-1, 0, "W", "E"),
        "E": (+1, 0, "E", "W"),
    }

    def __init__(self, data: dict):
        self.width = data["WIDTH"]
        self.height = data["HEIGHT"]
        self.entry = data["ENTRY"]
        self.exit = data["EXIT"]
        self.out_file = data["OUTPUT_FILE"]
        self.cell_size = self.calc_cell_size()
        self.wall_size = self.celc_wall_size()
        self.path = []
        self.is_path_draw = False
        self.perfect = data["PERFECT"]
        self.dirs = []
        self.fourty_two = []
        self.draw_42 = True
        self.seed = data["SEED"] if data["SEED"] else None
        # cells[row][col]
        self.cells = self.create_cells(self.width, self.height)
        self.algo = "dfs"

    class Cell:
        def __init__(self, row, column):
            self.row = row
            self.column = column
            self.walls = {"S": True, "N": True, "W": True, "E": True}
            self.is_visited = False

    def create_cells(self, width, height):
        cells = []
        for col in range(height):
            row_data = []
            for row in range(width):
                row_data.append(self.Cell(row, col))
            cells.append(row_data)
        return cells

    def celc_wall_size(self) -> int:
        if self.cell_size <= 10:
            return 1
        return 2

    def calc_cell_size(self) -> int:
        cell_size = 25
        while cell_size * self.width >= 800:
            cell_size -= 1
            if cell_size == 0:
                raise ErrorInConfigFile("cell_size <0")
        while cell_size * self.height >= 800:
            cell_size -= 1
            if cell_size == 0:
                raise ErrorInConfigFile("cell_size <0")
        return cell_size

    def my_42(self):
        if self.width > 15 and self.height > 15:
            cells = max(1, 20 // self.cell_size)
            middle_w = int(self.width / 2)
            middle_h = int(self.height / 2)
            start = max(1, cells // 4)
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

    def dsf_algorith(self):
        stack = []
        x, y = 0, 0

        self.cells[y][x].is_visited = True
        stack.append((x, y))
        while stack:
            x, y = stack[-1]
            key = list(self.direction.keys())
            random.shuffle(key)
            found = False
            i = 0
            while i < 4:
                m_x, m_y, m_dir, n_dir = self.direction[key[i]]
                n_x, n_y = x+m_x, y+m_y
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

    def reset_maze(self):
        for row in self.cells:
            for cell in row:
                cell.is_visited = False
                cell.walls = {"S": True, "N": True, "W": True, "E": True}

    def output_maze(self):
        os.makedirs("output", exist_ok=True)
        with open("output/"+self.out_file, 'w') as f:
            for i in range(self.height):
                for j in range(self.width):
                    count = 0
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
            x, y = self.entry
            m_x, m_y = self.exit
            f.write(f"{x},{y}\n")
            f.write(f"{m_x},{m_y}\n")
            for x in self.dirs:
                f.write(x)

    def not_perfect(self):
        if self.perfect is False:
            unvisited = []
            n_dir = ""
            dirs = ['E', 'W', 'N', 'S']
            w = self.width
            h = self.height

            wall = int(w * h * 0.01)

            for r in range(h):
                for c in range(w):
                    unvisited.append((c, r))

            while wall != 0 and unvisited:
                x, y = random.choice(unvisited)
                unvisited.remove((x, y))

                count = 0
                for i in dirs:
                    if self.cells[y][x].walls[i]:
                        count += 1
                found = True
                i = 0
                while i < 4 and found:
                    m_x, m_y, _, _ = self.direction[dirs[i]]
                    n_x, n_y = m_x+x, m_y+y
                    if 0 <= n_x < w and 0 <= n_y < h:
                        num = 0
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

    def wilson_algo(self):

        unvisited = []
        visited = []

        for r in range(self.height):
            for c in range(self.width):
                if self.cells[r][c].is_visited:
                    visited.append((c, r))

        for r in range(self.height):
            for c in range(self.width):
                if not self.cells[r][c].is_visited:
                    unvisited.append((c, r))

        x, y = random.choice(unvisited)
        self.cells[y][x].is_visited = True
        unvisited.remove((x, y))

        while unvisited:
            path = []
            x, y = random.choice(unvisited)
            path.append((x, y))

            while not self.cells[y][x].is_visited:

                key = random.choice(list(self.direction.keys()))

                d_x, d_y, m_dir, n_dir = self.direction[key]
                n_x, n_y = x + d_x, y + d_y

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

            l_x, l_y = path[0]
            if not self.cells[l_y][l_x].is_visited:
                self.cells[l_y][l_x].is_visited = True
                if (l_x, l_y) in unvisited:
                    unvisited.remove((l_x, l_y))

    def bfs_algo(self):
        for r in range(len(self.cells)):
            for c in range(len(self.cells[0])):
                self.cells[r][c].is_visited = False

        x, y = self.entry
        d_x, d_y = self.exit

        queue = deque()
        queue.append((x, y))
        data = deque()
        self.cells[y][x].is_visited = True

        parent = {}

        found = False

        while queue:
            x, y = queue.popleft()

            if x == d_x and y == d_y:
                found = True
                break

            key = list(self.direction.keys())

            i = 0
            while i < 4:
                n_x, n_y, m_dir, n_dir = self.direction[key[i]]
                m_x, m_y = x + n_x, y + n_y

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

        cur = self.exit

        while cur != self.entry:
            (m_x, m_y), d = parent[cur]

            if (m_x, m_y) != self.entry:
                data.appendleft((m_x, m_y))

            x, y = cur
            self.cells[y][x].path = True
            cur = (m_x, m_y)
            self.dirs.append(d)

        x, y = self.entry
        self.cells[y][x].path = True

        self.dirs.reverse()

        self.path = data
