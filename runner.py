#!/usr/bin/python
"""runner.py: Includes the main class for controlling the flow of the game. Input move updates and the bot displays
information about its and others' turns."""
__author__ = "Christopher Lehman"
__email__ = "lehman40@purdue.edu"

from cluechecker import check_space_with_clue, get_clue_dict, check_all_spaces_with_clue, check_all_clues_with_space, get_fp2
import pandas as pd
import itertools
import random
import time
import datetime


def play():
    fr = open("lastGameRead.txt", "r")
    fw = open("lastGameWrite.txt", "a", 1)  # Prepare new file for saving the inputs of this game
    lines = fr.readlines()
    lines = [l[:-1] for l in lines]

    # Get where the fp left off in gameboard
    fp = get_fp2()
    if fp < len(lines):
        players = int(lines[fp])
        fp += 1
    else:
        players = int(input('How many players? '))
    fw.write(str(players) + '\n')
    names = []
    for i in range(2, players + 1):
        if fp < len(lines):
            names.append(lines[fp])
            fp += 1
        else:
            names.append(input("Enter player " + str(i) + "'s name: "))
        fw.write(names[-1] + '\n')
    if fp < len(lines):
        mode = int(lines[fp])
        fp += 1
    else:
        mode = int(input('Which mode? \n1 - Normal \n2 - Advanced\n'))
    fw.write(str(mode) + '\n')
    clue_book = pd.read_csv("ClueReferenceSheet.csv")
    if fp < len(lines):
        book = lines[fp]
        fp += 1
    else:
        book = input('Which book is my clue? ').title()
    fw.write(book + '\n')
    if fp < len(lines):
        number = int(lines[fp])
        fp += 1
    else:
        number = int(input('Which number is my clue? '))
    fw.write(str(number) + '\n')


    # ideal_prop represents the proportion of clues the bot would learn about a player's clue when questioning. We want
    # this around 30% (varies with player number) so that the player is likely to place a disc. Or if they place a cube,
    # we learn a lot about their clue (but have to place one of our own)
    if players == 5:
        ideal_prop = .25
    elif players == 4:
        ideal_prop = .3
    else:
        ideal_prop = .35
    my_clue = clue_book.loc[number - 1, book]
    my_clue_text = get_clue_dict()[my_clue]
    spots_to_avoid = []
    # print(my_clue_text)

    # which clues other players think it could have
    my_possible = list(range(1, 49) if mode == 2 else list(range(1, 24)))
    # which spaces have pieces on them, should avoid for asking
    non_satisfied_spaces = list(set(range(1, 109)) - set(check_all_spaces_with_clue(my_clue)))

    # which clues other players could have
    others_remaining = [list(range(1, 49) if mode == 2 else list(range(1, 24))) for _ in range(players - 1)]

    # If its clue is a two terrain one, can eliminate some clues from others's possibilities
    if my_clue < 11:
        terrains = (my_clue_text.split()[1], my_clue_text.split()[3])
        for i in range(1, 11):
            if terrains[0] not in get_clue_dict()[i] and terrains[1] not in get_clue_dict()[i]:
                for o in others_remaining:
                    o.remove(i)
    # If its clue is a 'not', the inverse is not possible for the others
    if my_clue > 24:
        for o in others_remaining:
            o.remove(my_clue - 24)
    # The others cannot have its clue
    for o in others_remaining:
        o.remove(my_clue)

    # Read from file if available, or takes input
    if fp < len(lines):
        target = lines[fp]
        fp += 1
    else:
        target = input("Who goes first? (Type the name of the player. If it's the bot, type anything else)").title()
    # Write the input to save
    fw.write(target + '\n')
    turn = names.index(target) + 2 if target in names else 1
    while True:
        if turn > players:
            turn = 1
        if turn == 1:  # Bot is player 1
            print("It's my turn!")
            all_possible_spaces = set()

            # If the total combination of others possible clues is reasonably small. Compute all the combinations that
            # only lead to one space, otherwise, that combination is invalid
            if total_comb(others_remaining) < 2500:
                others_possibilities = [set() for _ in range(players - 1)]
                for possible in itertools.product(*others_remaining):
                    working_spaces = set.intersection(*[set(check_all_spaces_with_clue(p)) for p in possible],
                                                      set(check_all_spaces_with_clue(my_clue)))
                    # Check if just one space works and this possible set of clues are all distinct
                    if len(working_spaces) == 1 and len(set(possible)) == len(possible):
                        all_possible_spaces.add(working_spaces.pop())
                        for i, p in enumerate(possible):
                            others_possibilities[i].add(p)
                # Update the possible remaining with only the clues that led to once space
                others_remaining = [list(o) for o in others_possibilities]

            # Check if there was only one possible space or a search is reasonable (see method check_to_search below)
            if len(all_possible_spaces) == 1 or check_to_search(all_possible_spaces, my_possible, others_remaining):
                if len(all_possible_spaces) == 1:
                    space = max(all_possible_spaces)
                else:
                    # determine the best space to search of the possible ones based on how much it reveals from its clue
                    # by placing a piece and the likelihood of the player to the left placing a disc (means you get
                    # extra information)
                    candidates = []
                    for space in all_possible_spaces:
                        if (len(check_all_clues_with_space(space, my_possible)) / len(my_possible) > .55) and (
                                len(check_all_clues_with_space(space, others_remaining[0])) / len(
                                others_remaining[0]) > .65):
                            candidates.append(space)
                    if fp < len(lines):
                        space = int(lines[fp])
                        fp += 1
                    else:
                        space = random.choice(candidates)
                    fw.write(str(space) + '\n')
                row = (space - 1) // 12
                col = (space - 1) % 12
                time.sleep(1)
                # Make the search
                print("I think it's at row " + str(row) + " and column " + str(col))
                # Loop through only players or until a cube is placed
                for i in range(2, players + 1):
                    current = i
                    if fp < len(lines):
                        found = int(lines[fp])
                        fp += 1
                    else:
                        time.sleep(1)
                        found = int(input('Did ' + names[current - 2] + ' place a disc?\n1 - Yes \n2 - No\n'))
                    fw.write(str(found) + '\n')

                    if found == 1:
                        others_remaining[current - 2] = update_disc(others_remaining[current - 2], row, col)
                        if current == players:
                            print("I win.")
                            print("My clue was:", my_clue_text)
                            new_file = open(
                                "Game-" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M").replace(':', '-') + ".txt",
                                "w")
                            fw.close()
                            with open("lastGameWrite.txt", "r") as f:
                                new_file.write(f.read())
                            new_file.close()
                            print("Game saved at:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                            return
                    else:
                        others_remaining[current - 2] = update_cube(others_remaining[current - 2], row, col)
                        break
            else:
                # Not enough info to search, so will question a player
                lengths = [len(o) for o in others_remaining]
                # Asks player with most possible remaining clues (decides randomly in a tie)
                players_to_ask = []
                for i, length in enumerate(lengths):
                    if length == max(lengths):
                        players_to_ask.append(i)
                if fp < len(lines):
                    player_to_ask = int(lines[fp])
                    fp += 1
                else:
                    player_to_ask = random.choice(players_to_ask)
                fw.write(str(player_to_ask) + '\n')
                proportions = []
                # For every space, track the proportion of remaining clues the targeted player would reveal if a disc
                # was placed
                spaces = []
                for space in range(1, 109):
                    row = (space - 1) // 12
                    col = (space - 1) % 12
                    if (row, col) not in spots_to_avoid:
                        proportions.append(1 - (len(check_all_clues_with_space(space, others_remaining[player_to_ask]))
                                                / len(others_remaining[player_to_ask])))
                        spaces.append(space)
                # Reset to how close proportions are to the ideal that was set
                proportions = [abs(p - ideal_prop) for p in proportions]
                candidates = []
                for i, p in enumerate(proportions):
                    if p == min(proportions):
                        candidates.append(spaces[i])
                if fp < len(lines):
                    space = int(lines[fp])
                    fp += 1
                else:
                    space = random.choice(candidates)
                # Chose a random space from all the closest ones (more than one if a tie)
                fw.write(str(space) + '\n')
                row = (space - 1) // 12
                col = (space - 1) % 12

                # Prepare the question
                if fp < len(lines):
                    found = int(lines[fp])
                    fp += 1
                else:
                    time.sleep(3)
                    found = int(input(names[player_to_ask] + ", could it be at row " + str(row) + " and column " + str(col) + "?\n1 - Yes \n2 - No\n"))
                fw.write(str(found) + '\n')

                spots_to_avoid.append((row, col))
                if found == 1:
                    # It could be there, update info
                    others_remaining[player_to_ask] = update_disc(others_remaining[player_to_ask], row, col)
                else:
                    # It can't be there, update info and prepare to place a cube
                    others_remaining[player_to_ask] = update_cube(others_remaining[player_to_ask], row, col)
                    show_cube = []
                    spaces = []
                    for space in non_satisfied_spaces:
                        row = (space - 1) // 12
                        col = (space - 1) % 12
                        if (row, col) not in spots_to_avoid:
                            # track how many clues placing a cube on each space would reveal
                            show_cube.append(len(my_possible) - len(check_all_clues_with_space(space, my_possible)))
                            spaces.append(space)
                    candidates = []
                    for i, spot in enumerate(show_cube):
                        if spot == min(show_cube):
                            candidates.append(i)
                    space_to_place = spaces[random.choice(candidates)]
                    row = (space_to_place - 1) // 12
                    col = (space_to_place - 1) % 12
                    spots_to_avoid.append((row, col))
                    time.sleep(2)
                    print("Ok. For me it can't be at row " + str(row) + " and column " + str(col) + ". Could you place a cube for me as I have no arms?")
                    time.sleep(1)
                    my_possible = update_cube(my_possible, row, col)

        else:
            print("It's " + names[turn - 2] + "'s turn")
            if fp < len(lines):
                move = int(lines[fp])
                fp += 1
            else:
                move = int(input('Which move type did they take? \n1 - Question \n2 - Search\n'))
            fw.write(str(move) + '\n')
            if move == 1:
                if fp < len(lines):
                    target = lines[fp]
                    fp += 1
                else:
                    target = input("Who was asked? Type the name of the player. If it's the bot, type anything else").title()
                fw.write(target + '\n')
                asked = names.index(target) + 2 if target in names else 1
                if asked == 1:
                    if fp < len(lines):
                        loc = lines[fp]
                        fp += 1
                    else:
                        loc = input("Where was I asked? ")
                    fw.write(loc + '\n')
                    row = int(loc.split()[0])
                    col = int(loc.split()[1])
                    spots_to_avoid.append((row, col))
                    print("Let me check my clue...")
                    # Checks its clue for that space
                    print("It could be there!" if check_space_with_clue(row * 12 + col + 1, my_clue) else "No such luck!")
                    if check_space_with_clue(row * 12 + col + 1, my_clue):
                        my_possible = update_disc(my_possible, row, col)
                    else:
                        my_possible = update_cube(my_possible, row, col)
                        # Can't be there so they other player must place a cube
                        if fp < len(lines):
                            loc = lines[fp]
                            fp += 1
                        else:
                            loc = input("Where did " + names[turn - 2] + " place the cube? ")
                        fw.write(loc + '\n')
                        row = int(loc.split()[0])
                        col = int(loc.split()[1])
                        others_remaining[turn - 2] = update_cube(others_remaining[turn - 2], row, col)
                else:
                    if fp < len(lines):
                        loc = lines[fp]
                        fp += 1
                    else:
                        loc = input("Where were they asked? ")
                    fw.write(loc + '\n')
                    row = int(loc.split()[0])
                    col = int(loc.split()[1])
                    spots_to_avoid.append((row, col))
                    if fp < len(lines):
                        found = int(lines[fp])
                        fp += 1
                    else:
                        found = int(input('Could it be there?\n1 - Yes \n2 - No\n'))
                    fw.write(str(found) + '\n')
                    if found == 1:
                        others_remaining[asked - 2] = update_disc(others_remaining[asked - 2], row, col)
                    else:
                        others_remaining[asked - 2] = update_cube(others_remaining[asked - 2], row, col)
                        if fp < len(lines):
                            loc = lines[fp]
                            fp += 1
                        else:
                            loc = input("Where did " + names[turn - 2] + " place the cube? ")
                        fw.write(loc + '\n')
                        row = int(loc.split()[0])
                        col = int(loc.split()[1])
                        spots_to_avoid.append((row, col))
                        others_remaining[turn - 2] = update_cube(others_remaining[turn - 2], row, col)
            else:
                # A player searched a specific place
                if fp < len(lines):
                    loc = lines[fp]
                    fp += 1
                else:
                    loc = input("Where was searched? ")
                fw.write(loc + '\n')
                row = int(loc.split()[0])
                col = int(loc.split()[1])
                spots_to_avoid.append((row, col))
                if fp < len(lines):
                    real_loc = lines[fp]
                    fp += 1
                else:
                    real_loc = input("Put the other location if the disc had to be placed elsewhere, otherwise enter: ")
                fw.write(real_loc + '\n')
                if len(real_loc) > 1:
                    rrow = int(real_loc.split()[0])
                    rcol = int(real_loc.split()[1])
                    spots_to_avoid.append((rrow, rcol))
                    others_remaining[turn - 2] = update_disc(others_remaining[turn - 2], rrow, rcol)
                else:
                    others_remaining[turn - 2] = update_disc(others_remaining[turn - 2], row, col)
                current = turn
                for i in range(1, players):
                    # Loop through all other players
                    current += 1
                    if current > players:
                        current = 1
                    if current == 1:
                        print("Let me check if it could be there...")
                        time.sleep(1)
                        print("It could be there!" if check_space_with_clue(row * 12 + col + 1,
                                                                            my_clue) else "No such luck!")
                        if check_space_with_clue(row * 12 + col + 1, my_clue):
                            my_possible = update_disc(my_possible, row, col)
                        else:
                            # Bot placed the cube
                            my_possible = update_cube(my_possible, row, col)
                            break
                        if current == turn - 1:
                            # Everyone placed a disc
                            print("I am defeated, well played.")
                            print("My clue was:", my_clue_text)
                            new_file = open(
                                "Game-" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M").replace(':', '-') + ".txt",
                                "w")
                            with open("lastGameWrite.txt", "r") as f:
                                new_file.write(f.read())
                            new_file.close()
                            print("Game saved at:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                            return
                    else:
                        if fp < len(lines):
                            found = int(lines[fp])
                            fp += 1
                        else:
                            found = int(input('Did ' + names[current - 2] + ' place a disc?\n1 - Yes \n2 - No\n'))
                        fw.write(str(found) + '\n')
                        if found == 1:
                            others_remaining[current - 2] = update_disc(others_remaining[current - 2], row, col)
                            if current == turn - 1:
                                # Everyone placed a disc
                                print("I am defeated, well played.")
                                print("My clue was:", my_clue_text)
                                new_file = open("Game-" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M").replace(':', '-') + ".txt",
                                                "w")
                                with open("lastGameWrite.txt", "r") as f:
                                    new_file.write(f.read())
                                new_file.close()
                                print("Game saved at:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                return
                        else:
                            # Cube was placed
                            others_remaining[current - 2] = update_cube(others_remaining[current - 2], row, col)
                            break
        turn += 1


# Calculate the total possible combinations of others' remaining clues
def total_comb(others_remaining):
    t = 1
    for o in others_remaining:
        t *= len(o)
    return t


# Updates a list of clues by removing clues that don't work with the space a disc was placed
def update_disc(remaining, r, c):
    return [clue for clue in remaining if check_space_with_clue(r * 12 + c + 1, clue)]


# Updates a list of clues by removing clues that do work with the space a cube was placed
def update_cube(remaining, r, c):
    return [clue for clue in remaining if not check_space_with_clue(r * 12 + c + 1, clue)]


# Check if a search is warranted
def check_to_search(all_possible, my_possible, others_remaining):
    # Not worth it if there are too many spaces that could work
    if len(all_possible) > 4:
        return False
    # Not worth it if its clue is almost known
    if len(my_possible) < 5:
        return False
    # Check if there is at least one space of the possible that doesn't reveal too much about the bot's clue (55%) and
    # there is a good enough chance the player to the left places a disc (65%)
    for space in all_possible:
        # print(len(check_all_clues_with_space(space, my_possible)) / len(my_possible))
        # print(len(check_all_clues_with_space(space, others_remaining[0])) / len(others_remaining[0]))
        if (len(check_all_clues_with_space(space, my_possible)) / len(my_possible) > .55) and (len(check_all_clues_with_space(space, others_remaining[0])) / len(others_remaining[0]) > .65):
            return True
    return False


play()
