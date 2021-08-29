#!/usr/bin/python
"""cluechecker.py: Contains methods for checking spaces against clues. Can do one at a time or multiple as implemented
in runner.py"""
__author__ = "Christopher Lehman"
__email__ = "lehman40@purdue.edu"

from gameboard import load_board, print_board, load_obj, get_fp, get_players, get_clues, get_start_time, get_board_config

# Initialize empty board
board = [[None] * 12 for _ in range(9)]
load_board(board)
# load from distances.pkl as created by dcounter.py
distances = load_obj('distances')

# Reference for which numbers correspond to which clues
clue_dict = {
    'The habitat is on forest or desert': 1,
    'The habitat is on water or forest': 2,
    'The habitat is on forest or swamp': 3,
    'The habitat is on forest or mountain': 4,
    'The habitat is on water or desert': 5,
    'The habitat is on desert or swamp': 6,
    'The habitat is on desert or mountain': 7,
    'The habitat is on water or swamp': 8,
    'The habitat is on water or mountain': 9,
    'The habitat is on mountain or swamp': 10,
    'The habitat is within one space of forest': 11,
    'The habitat is within one space of desert': 12,
    'The habitat is within one space of swamp': 13,
    'The habitat is within one space of mountain': 14,
    'The habitat is within one space of water': 15,
    'The habitat is within one space of either animal territory': 16,
    'The habitat is within two spaces of a standing stone': 17,
    'The habitat is within two spaces of a shack': 18,
    'The habitat is within two spaces of a cougar territory': 19,
    'The habitat is within two spaces of bear territory': 20,
    'The habitat is within three spaces of a blue structure': 21,
    'The habitat is within three spaces of a white structure': 22,
    'The habitat is within three spaces of a green structure': 23,
    'The habitat is within three spaces of a black structure': 24,
    'The habitat is not on forest or desert': 25,
    'The habitat is not on water or forest': 26,
    'The habitat is not on forest or swamp': 27,
    'The habitat is not on forest or mountain': 28,
    'The habitat is not on water or desert': 29,
    'The habitat is not on desert or swamp': 30,
    'The habitat is not on desert or mountain': 31,
    'The habitat is not on water or swamp': 32,
    'The habitat is not on water or mountain': 33,
    'The habitat is not on mountain or swamp': 34,
    'The habitat is not within one space of forest': 35,
    'The habitat is not within one space of desert': 36,
    'The habitat is not within one space of swamp': 37,
    'The habitat not is within one space of mountain': 38,
    'The habitat is not within one space of water': 39,
    'The habitat is not within one space of either animal territory': 40,
    'The habitat is not within two spaces of a standing stone': 41,
    'The habitat is not within two spaces of a shack': 42,
    'The habitat is not within two spaces of a cougar territory': 43,
    'The habitat is not within two spaces of bear territory': 44,
    'The habitat is not within three spaces of a blue structure': 45,
    'The habitat is not within three spaces of a white structure': 46,
    'The habitat is not within three spaces of a green structure': 47,
    'The habitat is not within three spaces of a black structure': 48
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

def get_fp2():
    return get_fp()


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
