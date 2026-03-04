window_x = 1200
window_y = 800

image_maze_x = 800
image_maze_y = 800

image_button_x = 400
image_button_y = 800

sep_top_button = 140
sep_button = 140
button_hight = 70

buttons = [
    {
        "text": "regenerate maze",
        "start_x": image_maze_x + 70,
        "end_x": image_maze_x + 330,
    },
    {
        "text": "show or hide path",
        "start_x": image_maze_x + 70,
        "end_x": image_maze_x + 330,
    },
    {
        "text": "change color",
        "start_x": image_maze_x + 70,
        "end_x": image_maze_x + 330,
    },
    {
        "text": "change algorithm",
        "start_x": image_maze_x + 70,
        "end_x": image_maze_x + 330,
    },
]

colors = [
    {"background": 0x0F0F0F},  # Almost black
    {"button_bg": 0x2A2A2A},  # Dark gray
    {"base_wall_color": 0x00FF00},  # White
    {
        "wall_colors": [
            0x00FF00,  # 1. Neon green (Matrix style)
            0xFF00FF,  # 2. Magenta (electric)
            0x00FFFF,  # 3. Cyan (bright aqua)
            0xFF1493,  # 4. Deep pink (hot!)
            0xFFFF00,  # 5. Yellow (super bright)
            0xFF4500,  # 6. Orange red (fiery)
            0x7FFF00,  # 7. Chartreuse (lime punch)
            0x00E5FF,  # 8. Bright cyan (laser blue)
            0xB537F2,  # 9. Electric purple
            0xFF6600,  # 10. Bright orange (sunset)
        ]
    },
    {"entry": 0xFB542B},
    {"exit": 0x0000FF},
    {"path_color": 0xFFFFFF},
]

font = {
    "A": ["  X  ", " X X ", "XXXXX", "X   X", "X   X"],
    "B": ["XXXX ", "X   X", "XXXX ", "X   X", "XXXX "],
    "C": [" XXX ", "X   X", "X    ", "X   X", " XXX "],
    "D": ["XXXX ", "X   X", "X   X", "X   X", "XXXX "],
    "E": ["XXXXX", "X    ", "XXXX ", "X    ", "XXXXX"],
    "F": ["XXXXX", "X    ", "XXXX ", "X    ", "X    "],
    "G": [" XXX ", "X    ", "X XXX", "X   X", " XXX "],
    "H": ["X   X", "X   X", "XXXXX", "X   X", "X   X"],
    "I": [" XXX ", "  X  ", "  X  ", "  X  ", " XXX "],
    "J": ["  XXX", "   X ", "   X ", "X  X ", " XX  "],
    "K": ["X   X", "X  X ", "XXX  ", "X  X ", "X   X"],
    "L": ["X    ", "X    ", "X    ", "X    ", "XXXXX"],
    "M": ["X   X", "XX XX", "X X X", "X   X", "X   X"],
    "N": ["X   X", "XX  X", "X X X", "X  XX", "X   X"],
    "O": [" XXX ", "X   X", "X   X", "X   X", " XXX "],
    "P": ["XXXX ", "X   X", "XXXX ", "X    ", "X    "],
    "Q": [" XXX ", "X   X", "X   X", "X  XX", " XXXX"],
    "R": ["XXXX ", "X   X", "XXXX ", "X  X ", "X   X"],
    "S": [" XXXX", "X    ", " XXX ", "    X", "XXXX "],
    "T": ["XXXXX", "  X  ", "  X  ", "  X  ", "  X  "],
    "U": ["X   X", "X   X", "X   X", "X   X", " XXX "],
    "V": ["X   X", "X   X", "X   X", " X X ", "  X  "],
    "W": ["X   X", "X   X", "X X X", "XX XX", "X   X"],
    "X": ["X   X", " X X ", "  X  ", " X X ", "X   X"],
    "Y": ["X   X", " X X ", "  X  ", "  X  ", "  X  "],
    "Z": ["XXXXX", "   X ", "  X  ", " X   ", "XXXXX"],
    "0": [" XXX ", "X  XX", "X X X", "XX  X", " XXX "],
    "1": ["  X  ", " XX  ", "  X  ", "  X  ", " XXX "],
    "2": [" XXX ", "X   X", "   X ", "  X  ", "XXXXX"],
    "3": ["XXXXX", "   X ", " XXX ", "   X ", "XXXXX"],
    "4": ["X   X", "X   X", "XXXXX", "    X", "    X"],
    "5": ["XXXXX", "X    ", "XXXX ", "    X", "XXXX "],
    "6": [" XXX ", "X    ", "XXXX ", "X   X", " XXX "],
    "7": ["XXXXX", "   X ", "  X  ", " X   ", "X    "],
    "8": [" XXX ", "X   X", " XXX ", "X   X", " XXX "],
    "9": [" XXX ", "X   X", " XXXX", "    X", " XXX "],
    " ": ["     ", "     ", "     ", "     ", "     "],
}
