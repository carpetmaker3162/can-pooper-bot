class SokobanPuzzle:
    def __init__(self, grid, points) -> None:
        self.grid = grid
        self.points = points

class Sokoban:
    def __init__(self, s: SokobanPuzzle, floor = ".", wall = "█", crate = "○", gcrate = "●", player = "&", goal = "X", gplayer = "&") -> None:
        self.floor = floor
        self.wall = wall
        self.crate = crate
        self.ccrate = gcrate
        self.player = player
        self.goal = goal
        self.player_on_goal = gplayer
        
        self.icons = {
            0: self.floor,
            1: self.wall,
            2: self.crate,
            3: self.ccrate,
            4: self.player,
            9: self.goal,
            9.5: self.player_on_goal
        }

        self.grid = s.grid

        players = 0
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 4:
                    players += 1
                    self.player_x = x
                    self.player_y = y
        
        if players != 1:
            raise Exception("Invalid board (too many or too few players, should be 1 player)")

    def move(self, direction):
        if direction == "UP":
            if self.player_y - 1 != abs(self.player_y - 1):
                return -1
            match self.grid[self.player_y - 1][self.player_x]:
                case 0:
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y - 1][self.player_x] = 4
                case 1:
                    return -1
                case 2:
                    if self.player_y - 2 != abs(self.player_y - 2):
                        return -1
                    if self.grid[self.player_y - 2][self.player_x] not in (0, 9):
                        return -1
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y - 1][self.player_x] = 4
                    if self.grid[self.player_y - 2][self.player_x] == 0:
                        self.grid[self.player_y - 2][self.player_x] = 2
                    else:
                        self.grid[self.player_y - 2][self.player_x] = 3
                case 3:
                    if self.player_y - 2 != abs(self.player_y - 2):
                        return -1
                    if self.grid[self.player_y - 2][self.player_x] not in (0, 9):
                        return -1
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y - 1][self.player_x] = 9.5
                    if self.grid[self.player_y - 2][self.player_x] == 0:
                        self.grid[self.player_y - 2][self.player_x] = 2
                    else:
                        self.grid[self.player_y - 2][self.player_x] = 3
                case 4:
                    raise Exception("check board for validity (there seems to be more than 1 player)")
                case 9:
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y - 1][self.player_x] = 9.5
            self.player_y -= 1
        elif direction == "LEFT":
            if self.player_x - 1 != abs(self.player_x - 1):
                return -1
            match self.grid[self.player_y][self.player_x - 1]:
                case 0:
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y][self.player_x - 1] = 4
                case 1:
                    return -1
                case 2:
                    if self.player_x - 2 != abs(self.player_x - 2):
                        return -1
                    if self.grid[self.player_y][self.player_x - 2] not in (0, 9):
                        return -1
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y][self.player_x - 1] = 4
                    if self.grid[self.player_y][self.player_x - 2] == 0:
                        self.grid[self.player_y][self.player_x - 2] = 2
                    else:
                        self.grid[self.player_y][self.player_x - 2] = 3
                case 3:
                    if self.player_x - 2 != abs(self.player_x - 2):
                        return -1
                    if self.grid[self.player_y][self.player_x - 2] not in (0, 9):
                        return -1
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y][self.player_x - 1] = 9.5
                    if self.grid[self.player_y][self.player_x - 2] == 0:
                        self.grid[self.player_y][self.player_x - 2] = 2
                    else:
                        self.grid[self.player_y][self.player_x - 2] = 3
                case 4:
                    raise Exception("check board for validity (there seems to be more than 1 player)")
                case 9:
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y][self.player_x - 1] = 9.5
            self.player_x -= 1
        elif direction == "DOWN":
            if self.player_y + 1 >= len(self.grid):
                return -1
            match self.grid[self.player_y + 1][self.player_x]:
                case 0:
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y + 1][self.player_x] = 4
                case 1:
                    return -1
                case 2:
                    if self.player_y + 2 >= len(self.grid):
                        return -1
                    if self.grid[self.player_y + 2][self.player_x] not in (0, 9):
                        return -1
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y + 1][self.player_x] = 4
                    if self.grid[self.player_y + 2][self.player_x] == 0:
                        self.grid[self.player_y + 2][self.player_x] = 2
                    else:
                        self.grid[self.player_y + 2][self.player_x] = 3
                case 3:
                    if self.player_y + 2 >= len(self.grid):
                        return -1
                    if self.grid[self.player_y + 2][self.player_x] not in (0, 9):
                        return -1
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y + 1][self.player_x] = 9.5
                    if self.grid[self.player_y + 2][self.player_x] == 0:
                        self.grid[self.player_y + 2][self.player_x] = 2
                    else:
                        self.grid[self.player_y + 2][self.player_x] = 3
                case 4:
                    raise Exception("check board for validity (there seems to be more than 1 player)")
                case 9:
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y + 1][self.player_x] = 9.5
            self.player_y += 1
        elif direction == "RIGHT":
            if self.player_x + 1 >= len(self.grid[0]):
                return -1
            match self.grid[self.player_y][self.player_x + 1]:
                case 0:
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y][self.player_x + 1] = 4
                case 1:
                    return -1
                case 2:
                    if self.player_x + 2 >= len(self.grid[0]):
                        return -1
                    if self.grid[self.player_y][self.player_x + 2] not in (0, 9):
                        return -1
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y][self.player_x + 1] = 4
                    if self.grid[self.player_y][self.player_x + 2] == 0:
                        self.grid[self.player_y][self.player_x + 2] = 2
                    else:
                        self.grid[self.player_y][self.player_x + 2] = 3
                case 3:
                    if self.player_x + 2 >= len(self.grid[0]):
                        return -1
                    if self.grid[self.player_y][self.player_x + 2] not in (0, 9):
                        return -1
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y][self.player_x + 1] = 9.5
                    if self.grid[self.player_y][self.player_x + 2] == 0:
                        self.grid[self.player_y][self.player_x + 2] = 2
                    else:
                        self.grid[self.player_y][self.player_x + 2] = 3
                case 4:
                    raise Exception("check board for validity (there seems to be more than 1 player)")
                case 9:
                    if self.grid[self.player_y][self.player_x] == 9.5:
                        self.grid[self.player_y][self.player_x] = 9
                    else:
                        self.grid[self.player_y][self.player_x] = 0
                    self.grid[self.player_y][self.player_x + 1] = 9.5
            self.player_x += 1
        
        for row in self.grid:
            for cell in row:
                if cell == 9:
                    return 0
        
        return 2147483647

SOKOBAN_GAMES = [
    SokobanPuzzle(
    [
        [9, 0, 0, 0],
        [0, 0, 0, 0],
        [9, 2, 4, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 0],
    ], 100),

    
    SokobanPuzzle([
        [1, 1, 0, 0, 0, 1],
        [9, 4, 2, 0, 0, 1],
        [1, 1, 0, 2, 9, 1],
        [9, 1, 1, 2, 0, 1],
        [0, 1, 0, 9, 0, 1],
        [2, 0, 3, 2, 2, 9],
        [0, 0, 0, 9, 0, 0],
    ], 2500),
]

_SOKOBAN_GAMES = iter(SOKOBAN_GAMES)

"""
self.icons = {
            0: self.floor,
            1: self.wall,
            2: self.crate,
            3: self.ccrate,
            4: self.player,
            9: self.goal,
            9.5: self.player_on_goal
        }
"""

"""
def game_via_terminal(s):
    s = Sokoban(s)

    valid_moves = {
        "w": "UP",
        "a": "LEFT",
        "s": "DOWN",
        "d": "RIGHT"
    }

    while True:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        s.print_board()
        user_input = input(">>> ").lower()
        move = valid_moves.get(user_input, "")
        if not move:
            continue
        if s.move(move) == 2147483647:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            s.print_board()
            print("GG you won\nType \"again\" to do another game, type anything else to exit")
            if input(">>> ").lower() == "again":
                game_via_terminal(next(_SOKOBAN_GAMES))
            else:
                exit()
"""