#!/usr/bin/python
"""cluechecker.py: Contains methods for checking spaces against clues. Can do one at a time or multiple as implemented
in runner.py"""
__author__ = "Christopher Lehman"
__email__ = "lehman40@purdue.edu"

from gameboard import load_board, print_board, load_obj

# Initialize empty board
board = [[None] * 12 for _ in range(9)]
load_board(board)
print_board(board)
# load from distances.pkl as created by dcounter.py
distances = load_obj('distances')

# print_board(board)

# Reference for which numbers correspond to which clues
clue_dict = {
    1: 'On forest or desert',
    2: 'On forest or water',
    3: 'On forest or swamp',
    4: 'On forest or mountain',
    5: 'On desert or water',
    6: 'On desert or swamp',
    7: 'On desert or mountain',
    8: 'On water or swamp',
    9: 'On water or mountain',
    10: 'On swamp or mountain',
    11: 'Within one space of forest',
    12: 'Within one space of desert',
    13: 'Within one space of swamp',
    14: 'Within one space of mountain',
    15: 'Within one space of water',
    16: 'Within one space of either animal territory',
    17: 'Within two spaces of a standing stone',
    18: 'Within two spaces of an abandoned shack',
    19: 'Within two spaces of cougar territory',
    20: 'Within two spaces of bear territory',
    21: 'Within three spaces of a blue structure',
    22: 'Within three spaces of a white structure',
    23: 'Within three spaces of a green structure',
    24: 'Within three spaces of a black structure',
    25: 'Not on forest or desert',
    26: 'Not on forest or water',
    27: 'Not on forest or swamp',
    28: 'Not on forest or mountain',
    29: 'Not on desert or water',
    30: 'Not on desert or swamp',
    31: 'Not on desert or mountain',
    32: 'Not on water or swamp',
    33: 'Not on water or mountain',
    34: 'Not on swamp or mountain',
    35: 'Not within one space of forest',
    36: 'Not within one space of desert',
    37: 'Not within one space of swamp',
    38: 'Not within one space of mountain',
    39: 'Not within one space of water',
    40: 'Not within one space of either animal territory',
    41: 'Not within two spaces of a standing stone',
    42: 'Not within two spaces of an abandoned shack',
    43: 'Not within two spaces of cougar territory',
    44: 'Not within two spaces of bear territory',
    45: 'Not within three spaces of a blue structure',
    46: 'Not within three spaces of a white structure',
    47: 'Not within three spaces of a green structure',
    48: 'Not within three spaces of a black structure'
}


def get_clue_dict():
    return clue_dict


def check_two_terrain(r, c, terr1, terr2):
    return board[r][c].terrain == terr1 or board[r][c].terrain == terr2


def check_one_within(spacedist, terr):
    if terr == 'animal':
        for i in range(1, 109):
            if spacedist[i] < 2 and board[(i - 1) // 12][(i - 1) % 12].territory:
                return True
        return False
    else:  # Check if one from a specific terrain
        for i in range(1, 109):
            if spacedist[i] < 2 and board[(i - 1) // 12][(i - 1) % 12].terrain == terr:
                return True
        return False


def check_two_within(spacedist, item, animal=False):
    if animal:  # check two from bear or cougar
        for i in range(1, 109):
            if spacedist[i] < 3 and board[(i - 1) // 12][(i - 1) % 12].territory == item:
                return True
        return False
    else:  # check two from standing stone or abandoned shack
        for i in range(1, 109):
            if spacedist[i] < 3 and board[(i - 1) // 12][(i - 1) % 12].b_type == item:
                return True
        return False


def check_three_within(spacedist, color):
    for i in range(1, 109):
        if spacedist[i] < 4 and board[(i - 1) // 12][(i - 1) % 12].b_color == color:
            return True
    return False


def check_space_with_clue(space, clue):
    # get distances to all other spaces from this space
    spacedist = distances[space]
    row = (space - 1) // 12
    col = (space - 1) % 12
    if clue == 1:
        return check_two_terrain(row, col, 'forest', 'desert')
    elif clue == 2:
        return check_two_terrain(row, col, 'forest', 'water')
    elif clue == 3:
        return check_two_terrain(row, col, 'forest', 'swamp')
    elif clue == 4:
        return check_two_terrain(row, col, 'forest', 'mountain')
    elif clue == 5:
        return check_two_terrain(row, col, 'desert', 'water')
    elif clue == 6:
        return check_two_terrain(row, col, 'desert', 'swamp')
    elif clue == 7:
        return check_two_terrain(row, col, 'desert', 'mountain')
    elif clue == 8:
        return check_two_terrain(row, col, 'water', 'swamp')
    elif clue == 9:
        return check_two_terrain(row, col, 'water', 'mountain')
    elif clue == 10:
        return check_two_terrain(row, col, 'swamp', 'mountain')
    elif clue == 11:
        return check_one_within(spacedist, 'forest')
    elif clue == 12:
        return check_one_within(spacedist, 'desert')
    elif clue == 13:
        return check_one_within(spacedist, 'swamp')
    elif clue == 14:
        return check_one_within(spacedist, 'mountain')
    elif clue == 15:
        return check_one_within(spacedist, 'water')
    elif clue == 16:
        return check_one_within(spacedist, 'animal')
    elif clue == 17:
        return check_two_within(spacedist, 'stone')
    elif clue == 18:
        return check_two_within(spacedist, 'shack')
    elif clue == 19:
        return check_two_within(spacedist, 'cougar', animal=True)
    elif clue == 20:
        return check_two_within(spacedist, 'bear', animal=True)
    elif clue == 21:
        return check_three_within(spacedist, 'blue')
    elif clue == 22:
        return check_three_within(spacedist, 'white')
    elif clue == 23:
        return check_three_within(spacedist, 'green')
    elif clue == 24:
        return check_three_within(spacedist, 'black')
    elif clue > 24 and clue < 49:
        # Inverse of the clue
        return not check_space_with_clue(space, clue - 24)


# returns all spaces that work with a clue
def check_all_spaces_with_clue(clue):
    sol = []
    for i in range(1, 109):
        if check_space_with_clue(i, clue):
            sol.append(i)
    return sol


# returns the portion of clues passed to it that work with one space
def check_all_clues_with_space(space, clues):
    sol = []
    for c in clues:
        if check_space_with_clue(space, c):
            sol.append(c)
    return sol
