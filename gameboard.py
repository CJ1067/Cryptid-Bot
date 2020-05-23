#!/usr/bin/python
"""gameboard.py: Includes class declaration for a board space with proper attributes. Also has logic to load the
gameboard based on the order of map pieces and structures."""
__author__ = "Christopher Lehman"
__email__ = "lehman40@purdue.edu"

import pickle


class BoardSpace:
    def __init__(self, terrain, territory=None):
        self.terrain = terrain
        self.territory = None
        if territory:
            self.territory = territory
        self.b_color = None
        self.b_type = None

    def add_building(self, b_color, b_type):
        self.b_color = b_color
        self.b_type = b_type

    def __repr__(self):
        if self.territory and self.b_color:
            return self.terrain + ' ' + self.territory + ' (' + self.b_color + ', ' + self.b_type + ')'
        elif self.territory:
            return self.terrain + ' ' + self.territory
        elif self.b_color:
            return self.terrain + ' (' + self.b_color + ', ' + self.b_type + ')'
        else:
            return self.terrain


# Map piece 1
one = [[BoardSpace('water'), BoardSpace('water'), BoardSpace('water'), BoardSpace('water'), BoardSpace('forest'), BoardSpace('forest')],
       [BoardSpace('swamp'), BoardSpace('swamp'), BoardSpace('water'), BoardSpace('desert'), BoardSpace('forest'), BoardSpace('forest')],
       [BoardSpace('swamp'), BoardSpace('swamp'), BoardSpace('desert'), BoardSpace('desert', 'bear'), BoardSpace('desert', 'bear'), BoardSpace('forest', 'bear')]]

# Map piece 2
two = [[BoardSpace('swamp', 'cougar'), BoardSpace('forest', 'cougar'), BoardSpace('forest', 'cougar'), BoardSpace('forest'), BoardSpace('forest'), BoardSpace('forest')],
       [BoardSpace('swamp'), BoardSpace('swamp'), BoardSpace('forest'), BoardSpace('desert'), BoardSpace('desert'), BoardSpace('desert')],
       [BoardSpace('swamp'), BoardSpace('mountain'), BoardSpace('mountain'), BoardSpace('mountain'), BoardSpace('mountain'), BoardSpace('desert')]]

# Map piece 3
three = [[BoardSpace('swamp'), BoardSpace('swamp'), BoardSpace('forest'), BoardSpace('forest'), BoardSpace('forest'), BoardSpace('water')],
         [BoardSpace('swamp', 'cougar'), BoardSpace('swamp', 'cougar'), BoardSpace('forest'), BoardSpace('mountain'), BoardSpace('water'), BoardSpace('water')],
         [BoardSpace('mountain', 'cougar'), BoardSpace('mountain'), BoardSpace('mountain'), BoardSpace('mountain'), BoardSpace('water'), BoardSpace('water')]]

# Map piece 4
four = [[BoardSpace('desert'), BoardSpace('desert'), BoardSpace('mountain'), BoardSpace('mountain'), BoardSpace('mountain'), BoardSpace('mountain')],
        [BoardSpace('desert'), BoardSpace('desert'), BoardSpace('mountain'), BoardSpace('water'), BoardSpace('water'), BoardSpace('water', 'cougar')],
        [BoardSpace('desert'), BoardSpace('desert'), BoardSpace('desert'), BoardSpace('forest'), BoardSpace('forest'), BoardSpace('forest', 'cougar')]]

# Map piece 5
five = [[BoardSpace('swamp'), BoardSpace('swamp'), BoardSpace('swamp'), BoardSpace('mountain'), BoardSpace('mountain'), BoardSpace('mountain')],
        [BoardSpace('swamp'), BoardSpace('desert'), BoardSpace('desert'), BoardSpace('water'), BoardSpace('mountain'), BoardSpace('mountain', 'bear')],
        [BoardSpace('desert'), BoardSpace('desert'), BoardSpace('water'), BoardSpace('water'), BoardSpace('water', 'bear'), BoardSpace('water', 'bear')]]

# Map piece 6
six = [[BoardSpace('desert', 'bear'), BoardSpace('desert'), BoardSpace('swamp'), BoardSpace('swamp'), BoardSpace('swamp'), BoardSpace('forest')],
       [BoardSpace('mountain', 'bear'), BoardSpace('mountain'), BoardSpace('swamp'), BoardSpace('swamp'), BoardSpace('forest'), BoardSpace('forest')],
       [BoardSpace('mountain'), BoardSpace('water'), BoardSpace('water'), BoardSpace('water'), BoardSpace('water'), BoardSpace('forest')]]

pieces = [one, two, three, four, five, six]


# for a map piece that goes upside-down
def flip_piece(piece):
    return [row[::-1] for row in piece[::-1]]


def load_board(board, debug=None, debug2=None):
    # debug options are lists that can be passed in with the piece order and structure locations to skip the user input
    if not debug:
        print("Enter map piece numbers in column major order followed by an f if the piece is flipped e.g 2, 4f")
    for i in range(6):
        if not debug:
            piece = input("Input piece #" + str(i + 1) + ': ')
        else:
            piece = debug[i]
        while len(piece) > 2 or len(piece) < 1 or not piece[0].isnumeric() or int(piece[0]) < 1 or int(piece[0]) > 6:
            piece = input("Invalid. Please enter again. ")
        num = int(piece[0])
        if len(piece) == 2 and piece[1] == 'f':
            p = flip_piece(pieces[num - 1])
        else:
            p = pieces[num - 1]

        startcol = 0
        if i > 2:
            startcol = 6

        # Place spaces into the corresponding spaces in the board
        for ro, r in enumerate(range((i % 3) * 3, (i % 3) * 3 + 3)):
            for co, c in enumerate(range(startcol, startcol + 6)):
                board[r][c] = p[ro][co]

    # Load structures into the spaces
    if debug2:  # If preset options were sent in
        loc = debug2[0]
        board[int(loc[0])][int(loc[1])].add_building('green', 'stone')
        loc = debug2[1]
        board[int(loc[0])][int(loc[1])].add_building('green', 'shack')
        loc = debug2[2]
        board[int(loc[0])][int(loc[1])].add_building('blue', 'stone')
        loc = debug2[3]
        board[int(loc[0])][int(loc[1])].add_building('blue', 'shack')
        loc = debug2[4]
        board[int(loc[0])][int(loc[1])].add_building('white', 'stone')
        loc = debug2[5]
        board[int(loc[0])][int(loc[1])].add_building('white', 'shack')
        if len(debug2) < 7:
            return
        loc = debug2[6]
        board[int(loc[0])][int(loc[1])].add_building('black', 'stone')
        loc = debug2[7]
        board[int(loc[0])][int(loc[1])].add_building('black', 'shack')
    else:  # normal input
        print("Enter locations as 'row col' e.g '4 5', '0, 11'")
        loc = input("Input location of green stone: ").split()
        board[int(loc[0])][int(loc[1])].add_building('green', 'stone')

        loc = input("Input location of green shack: ").split()
        board[int(loc[0])][int(loc[1])].add_building('green', 'shack')

        loc = input("Input location of blue stone: ").split()
        board[int(loc[0])][int(loc[1])].add_building('blue', 'stone')

        loc = input("Input location of blue shack: ").split()
        board[int(loc[0])][int(loc[1])].add_building('blue', 'shack')

        loc = input("Input location of white stone: ").split()
        board[int(loc[0])][int(loc[1])].add_building('white', 'stone')

        loc = input("Input location of white shack: ").split()
        board[int(loc[0])][int(loc[1])].add_building('white', 'shack')

        loc = input("Input location of black stone: (if playing normal mode, just hit enter) ").split()
        if loc:
            board[int(loc[0])][int(loc[1])].add_building('black', 'stone')

        loc = input("Input location of black shack: (if playing normal mode, just hit enter) ").split()
        if loc:
            board[int(loc[0])][int(loc[1])].add_building('black', 'shack')
        print_board(board)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def print_board(board):
    for b in board:
        print(b)

