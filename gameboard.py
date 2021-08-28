#!/usr/bin/python
"""gameboard.py: Includes class declaration for a board space with proper attributes. Also has logic to load the
gameboard based on the order of map pieces and structures."""
__author__ = "Christopher Lehman"
__email__ = "lehman40@purdue.edu"

import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import base64
import time
import cv2
import os
from openpyxl import load_workbook
import traceback


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


start_time = time.time()
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

# players = int(input('How many players? '))
players = 4
# Prepare contents of last game to be read
new_file = open("lastGameRead.txt", "w")
with open("lastGameWrite.txt", "r") as f:
    new_file.write(f.read())
new_file.close()
fr = open("lastGameRead.txt", "r")
fw = open("lastGameWrite.txt", "w", 1)  # Prepare new file for saving the inputs of this game
fp = 0
loc_to_pos = {
    (30, 0): 0,
    (30, 146): 1,
    (30, 290): 2,
    (30, 291): 2,
    (275, 0): 3,
    (275, 146): 4,
    (275, 290): 5,
    (275, 291): 5
}

row_range = {
    (0, 46): 0,
    (47, 90): 1,
    (91, 136): 2,
    (147, 193): 3,
    (194, 237): 4,
    (238, 283): 5,
    (291, 337): 6,
    (338, 383): 7,
    (384, 429): 8
}

col_range = {
    (30, 70): 0,
    (71, 110): 1,
    (111, 148): 2,
    (149, 188): 3,
    (189, 227): 4,
    (228, 268): 5,
    (275, 315): 6,
    (316, 355): 7,
    (356, 395): 8,
    (396, 434): 9,
    (435, 474): 10,
    (475, 515): 11
}

clues_text = []


# for a map piece that goes upside-down
def flip_piece(piece):
    return [row[::-1] for row in piece[::-1]]


def load_board(board):
    try:
        chrome_options = Options()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=chrome_options)
        # driver.maximize_window()
        driver.set_window_position(0, 0)
        driver.set_window_size(1024, 768)

        driver.get("https://ospreypublishing.com/playcryptid/")

        time.sleep(2)
        numplayers = Select(driver.find_element_by_id('ngfPlayers'))
        numplayers.select_by_value(str(players))

        # sound = driver.find_elements_by_class_name('slider.round')[1]
        # sound.click()

        advanced = driver.find_elements_by_class_name('slider.round')[2]
        advanced.click()

        start = driver.find_element_by_id('ngfStart')
        start.click()
        # numplayers = driver.find_element_by_xpath('//*[@id="ngfPlayers"]/option[@value=\'' + str(players) + '\']')

        time.sleep(2)
        canvas = driver.find_element_by_id('mapCanvas')

        # get the canvas as a PNG base64 string
        canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)

        # decode
        canvas_png = base64.b64decode(canvas_base64)

        cookies_button = driver.find_element_by_class_name('cc-btn.cc-allow')
        cookies_button.click()

        time.sleep(1)

        clue_button = driver.find_element_by_id('clueButton')
        clue_button.click()
        time.sleep(1)
        clue_text = driver.find_element_by_id('clueText')
        clues_text.append(clue_text.text)
        for i in range(players - 1):
            clue_button.click()
            time.sleep(.5)
            clue_button.click()
            time.sleep(.5)
            clues_text.append(clue_text.text)

        # save to a file
        with open(r"canvas.png", 'wb') as f:
            f.write(canvas_png)

        iter_pieces = iter(os.listdir("Online_Board_Pieces"))
        piece_order = [0] * 6

        for filename in iter_pieces:
            flip_filename = next(iter_pieces)
            origLoc, origS = match_img('Online_Board_Pieces/' + filename)
            flipLoc, flipS = match_img('Online_Board_Pieces/' + flip_filename)
            if origLoc not in loc_to_pos:
                # print('earlyflip')
                piece_order[loc_to_pos[flipLoc]] = flip_filename[:flip_filename.index('.')]
            elif flipLoc not in loc_to_pos:
                # print('early')
                piece_order[loc_to_pos[origLoc]] = filename[:filename.index('.')]
            elif origS < flipS:
                # print('late')
                piece_order[loc_to_pos[origLoc]] = filename[:filename.index('.')]
            else:
                # print('lateflip')
                piece_order[loc_to_pos[flipLoc]] = flip_filename[:flip_filename.index('.')]
        print(piece_order)
        load_pieces(board, piece_order)
        for filename in os.listdir("Online_Board_IMGs"):
            loc, _ = match_img('Online_Board_IMGs/' + filename)
            cloc, rloc = loc
            for crange in col_range:
                low, high = crange
                if low <= cloc <= high:
                    col = col_range[crange]
                    break
            if col % 2 == 1:
                rloc -= 25
            for rrange in row_range:
                low, high = rrange
                if low <= rloc <= high:
                    row = row_range[rrange]
                    break

            color, b_type = filename[:filename.index('.')].split('_')

            load_structure(color, b_type, board, row, col)

        driver.close()
    except:
        traceback.print_exc()
        workbook = load_workbook(filename="Cryptid_Logs.xlsx")
        sheet = workbook.active
        for cell in sheet["A"]:
            if cell.value is None:
                next_row = cell.row
                break
        else:
            next_row = cell.row + 1
        sheet['A' + str(next_row)] = 'false'
        sheet['B' + str(next_row)] = players
        workbook.save(filename="Cryptid_Logs.xlsx")
    # print_board(board)


def match_img(filename):
    online_board = cv2.imread('canvas.png')
    small_image = cv2.imread(filename)

    result = cv2.matchTemplate(online_board, small_image, cv2.TM_SQDIFF, mask=small_image)

    # We want the minimum squared difference
    mn, _, mnLoc, _ = cv2.minMaxLoc(result)

    # print(filename)
    # print(mnLoc)
    # print(mn / 1000000)

    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx, MPy = mnLoc

    # # Step 2: Get the size of the template. This is the same size as the match.
    # trows, tcols = small_image.shape[:2]
    #
    # # Step 3: Draw the rectangle on large_image
    # cv2.rectangle(online_board, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 0, 255), 2)
    #
    # # Display the original image with the rectangle around the match.
    # cv2.imshow('output', online_board)
    #
    # cv2.waitKey(0)

    return mnLoc, mn


def get_fp():
    return fp


def load_pieces(board, pieces_order):
    for i in range(6):
        startcol = 0
        if i > 2:
            startcol = 6

        piece = pieces_order[i]
        num = int(piece[0])
        if len(piece) == 2 and piece[1] == 'f':
            p = flip_piece(pieces[num - 1])
        else:
            p = pieces[num - 1]

        # Place spaces into the corresponding spaces in the board
        for ro, r in enumerate(range((i % 3) * 3, (i % 3) * 3 + 3)):
            for co, c in enumerate(range(startcol, startcol + 6)):
                board[r][c] = p[ro][co]


def load_structure(color, b_type, board, row, col):
    board[row][col].add_building(color, b_type)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def get_players():
    return players


def get_clues():
    return clues_text


def get_start_time():
    return start_time

def print_board(board):
    print('Game Board:')
    for b in board:
        print(b)

