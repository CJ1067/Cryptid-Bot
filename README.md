# Cryptid Bot

Cryptid Bot is a bot that can be used to play the deduction based board game Cryptid against other human players while receiving input about updates of the game from other players. Learn more about the game here: https://boardgamegeek.com/boardgame/246784/cryptid

### Installing

Download latest version of Python 3: https://www.python.org/downloads/
Run CMD and input command ```pip3 install -r requirements.txt```

### Usage

The bot plays alongside human players on a set up game board by receiving input about game events and updating the players with its actions on its turn.

## Setting up

- Start the main program with ```python runner.py```
- Input the order of game pieces in column major order 
- Input the locations of the structures

## Gameplay

- Enter locations of game events and follow the instructions for each player's turn
- The bot will say the location of its turn 

## Game Storage

- Records of the user inputs to a game will automatically be stored in lastGameWrite.txt as the program is run
- After the game, a copy of this will be stored in the 'Game Records' directory
- At the beginning of the game, user will be given the option to load the previous game which will load the contents of lastGameWrite.txt

### Example

See the sample three player game as it playes out for the setup below:
