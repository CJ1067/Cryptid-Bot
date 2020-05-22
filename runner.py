#!/usr/bin/python

from cluechecker import check_space_with_clue, get_clue_dict, check_all_spaces_with_clue, check_all_clues_with_space
import pandas as pd
import itertools
import random
import time
import datetime


def play():
    new_file = open("lastGameRead.txt", "w")
    with open("lastGameWrite.txt", "r") as f:
        new_file.write(f.read())
    new_file.close()

    fr = open("lastGameRead.txt", "r")
    fw = open("lastGameWrite.txt", "w", 1)
    lines = fr.readlines()
    lines = [l[:-1] for l in lines]
    fp = 0
    load = int(input("Are you loading the previous game?\n1 - Yes \n2 - No\n"))
    if load == 2:
        fp = len(lines)
    debug = False
    players = 3 if debug else int(input('How many players? '))
    names = []
    for i in range(2, players + 1):
        if fp < len(lines):
            names.append(lines[fp])
            fp += 1
        else:
            names.append(input("Enter player " + str(i) + "'s name: "))
        fw.write(names[-1] + '\n')
    mode = 1 if debug else int(input('Which mode? \n1 - Normal \n2 - Advanced\n'))
    clue_book = pd.read_csv("ClueReferenceSheet.csv")
    book = 'Alpha' if debug else input('Which book is my clue? ').title()
    number = 17 if debug else int(input('Which number is my clue? '))

    if players == 5:
        good_prob = .25
    elif players == 4:
        good_prob = .3
    else:
        good_prob = .35
    my_clue = clue_book.loc[number - 1, book]
    my_clue_text = get_clue_dict()[my_clue]
    spots_to_avoid = []
    # print(my_clue_text)

    my_possible = list(range(1, 49) if mode == 2 else list(range(1, 24)))
    non_satisfied_spaces = list(set(range(1, 109)) - set(check_all_spaces_with_clue(my_clue)))

    others_remaining = [list(range(1, 49) if mode == 2 else list(range(1, 24))) for _ in range(players - 1)]

    if my_clue < 11:
        terrains = (my_clue_text.split()[1], my_clue_text.split()[3])
        for i in range(1, 11):
            if terrains[0] not in get_clue_dict()[i] and terrains[1] not in get_clue_dict()[i]:
                for o in others_remaining:
                    o.remove(i)
    if my_clue > 24:
        for o in others_remaining:
            o.remove(my_clue - 24)
    for o in others_remaining:
        o.remove(my_clue)

    if fp < len(lines):
        target = lines[fp]
        fp += 1
    else:
        target = input('Who goes first? ').title()
    fw.write(target + '\n')
    turn = names.index(target) + 2 if target in names else 1
    while True:
        # print('others:', others_remaining)
        if turn > players:
            turn = 1
        if turn == 1:
            print("It's my turn!")
            all_possible_spaces = set()
            # print("total comb:", total_comb(others_remaining))

            if total_comb(others_remaining) < 2500:
                others_possibilities = [set() for _ in range(players - 1)]
                for possible in itertools.product(*others_remaining):
                    working_spaces = set.intersection(*[set(check_all_spaces_with_clue(p)) for p in possible],
                                                      set(check_all_spaces_with_clue(my_clue)))
                    if len(working_spaces) == 1 and len(set(possible)) == len(possible):
                        all_possible_spaces.add(working_spaces.pop())
                        for i, p in enumerate(possible):
                            others_possibilities[i].add(p)
                others_remaining = [list(o) for o in others_possibilities]
                # print(all_possible_spaces)
                # print('others:', others_remaining)
            if len(all_possible_spaces) == 1 or check_to_search(all_possible_spaces, my_possible, others_remaining):
                if len(all_possible_spaces) == 1:
                    space = max(all_possible_spaces)
                else:
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
                print("I think it's at row " + str(row) + " and column " + str(col))
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
                            new_file = open(
                                "Game-" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M").replace(':', '-') + ".txt",
                                "w")
                            with open("lastGameWrite.txt", "r") as f:
                                new_file.write(f.read())
                            new_file.close()
                            print("Game saved at:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                            return
                    else:
                        others_remaining[current - 2] = update_cube(others_remaining[current - 2], row, col)
                        break
            else:
                lengths = [len(o) for o in others_remaining]
                players_to_ask = []
                for i, l in enumerate(lengths):
                    if l == max(lengths):
                        players_to_ask.append(i)
                if fp < len(lines):
                    player_to_ask = int(lines[fp])
                    fp += 1
                else:
                    player_to_ask = random.choice(players_to_ask)
                fw.write(str(player_to_ask) + '\n')
                proportions = []
                spaces = []
                for space in range(1, 109):
                    row = (space - 1) // 12
                    col = (space - 1) % 12
                    if (row, col) not in spots_to_avoid:
                        proportions.append(1 - (len(check_all_clues_with_space(space, others_remaining[player_to_ask]))
                                                / len(others_remaining[player_to_ask])))
                        spaces.append(space)
                proportions = [abs(p - good_prob) for p in proportions]
                candidates = []
                for i, p in enumerate(proportions):
                    if p == min(proportions):
                        candidates.append(spaces[i])
                if fp < len(lines):
                    space = int(lines[fp])
                    fp += 1
                else:
                    space = random.choice(candidates)
                fw.write(str(space) + '\n')
                row = (space - 1) // 12
                col = (space - 1) % 12

                if fp < len(lines):
                    found = int(lines[fp])
                    fp += 1
                else:
                    time.sleep(3)
                    found = int(input(names[player_to_ask] + ", could it be at row " + str(row) + " and column " + str(col) + "?\n1 - Yes \n2 - No\n"))
                fw.write(str(found) + '\n')

                spots_to_avoid.append((row, col))
                if found == 1:
                    others_remaining[player_to_ask] = update_disc(others_remaining[player_to_ask], row, col)
                else:
                    others_remaining[player_to_ask] = update_cube(others_remaining[player_to_ask], row, col)
                    show_cube = []
                    spaces = []
                    for space in non_satisfied_spaces:
                        row = (space - 1) // 12
                        col = (space - 1) % 12
                        if (row, col) not in spots_to_avoid:
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
                move = int(input('Which move type? \n1 - Question \n2 - Search\n'))
            fw.write(str(move) + '\n')
            if move == 1:
                if fp < len(lines):
                    target = lines[fp]
                    fp += 1
                else:
                    target = input('Who was asked? ').title()
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
                    print("It could be there!" if check_space_with_clue(row * 12 + col + 1, my_clue) else "No such luck!")
                    if check_space_with_clue(row * 12 + col + 1, my_clue):
                        my_possible = update_disc(my_possible, row, col)
                    else:
                        my_possible = update_cube(my_possible, row, col)
                        if fp < len(lines):
                            loc = lines[fp]
                            fp += 1
                        else:
                            loc = input("Where was the cube placed? ")
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
                            loc = input("Where was the additional cube placed? ")
                        fw.write(loc + '\n')
                        row = int(loc.split()[0])
                        col = int(loc.split()[1])
                        spots_to_avoid.append((row, col))
                        others_remaining[turn - 2] = update_cube(others_remaining[turn - 2], row, col)
            else:
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
                    realloc = lines[fp]
                    fp += 1
                else:
                    realloc = input("Put the other location if the search location was elsewhere, otherwise enter: ")
                fw.write(realloc + '\n')
                if len(realloc) > 1:
                    rrow = int(realloc.split()[0])
                    rcol = int(realloc.split()[1])
                    spots_to_avoid.append((rrow, rcol))
                    others_remaining[turn - 2] = update_disc(others_remaining[turn - 2], rrow, rcol)
                else:
                    others_remaining[turn - 2] = update_disc(others_remaining[turn - 2], row, col)
                current = turn
                for i in range(1, players):
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
                            my_possible = update_cube(my_possible, row, col)
                            break
                        if current == turn - 1:
                            print("I am defeated, well played.")
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
                                print("I am defeated, well played.")
                                new_file = open("Game-" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M").replace(':', '-') + ".txt",
                                                "w")
                                with open("lastGameWrite.txt", "r") as f:
                                    new_file.write(f.read())
                                new_file.close()
                                print("Game saved at:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                return
                        else:
                            others_remaining[current - 2] = update_cube(others_remaining[current - 2], row, col)
                            break
        turn += 1


def total_comb(others_remaining):
    t = 1
    for o in others_remaining:
        t *= len(o)
    return t


def update_disc(remaining, r, c):
    return [clue for clue in remaining if check_space_with_clue(r * 12 + c + 1, clue)]


def update_cube(remaining, r, c):
    return [clue for clue in remaining if not check_space_with_clue(r * 12 + c + 1, clue)]


def check_to_search(all_possible, my_possible, others_remaining):
    if len(all_possible) > 4:
        return False
    if len(my_possible) < 5:
        return False
    for space in all_possible:
        # print(len(check_all_clues_with_space(space, my_possible)) / len(my_possible))
        # print(len(check_all_clues_with_space(space, others_remaining[0])) / len(others_remaining[0]))
        if (len(check_all_clues_with_space(space, my_possible)) / len(my_possible) > .55) and (len(check_all_clues_with_space(space, others_remaining[0])) / len(others_remaining[0]) > .65):
            return True
    return False


play()
