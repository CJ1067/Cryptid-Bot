# Cryptid Bot

Cryptid Bot is a bot that can be used to play the deduction based board game Cryptid against other human players while receiving input about updates of the game from other players. Learn more about the game here: https://boardgamegeek.com/boardgame/246784/cryptid

## Installing

Download latest version of Python 3: https://www.python.org/downloads/
Run CMD and input command ```pip3 install -r requirements.txt```

## Usage

The bot plays alongside human players on a set up game board by receiving input about game events and updating the players with its actions on its turn.

## Setting up

- Start the main program with ```python runner.py```
- Input the order of game pieces in column major order 
- Input the locations of the structures

## Gameplay

- Enter locations of game events and follow the instructions for each player's turn
- The bot will say the location of its turn 

### Game Storage

- Records of the user inputs to a game will automatically be stored in lastGameWrite.txt as the program is run
- After the game, a copy of this will be stored in the 'Game Records' directory
- At the beginning of the game, user will be given the option to load the previous game which will load the contents of lastGameWrite.txt

### Loading a Previous Game

- If you are loading the last run game, your contents should be in lastGameWrite.txt and you are ready to go
- Otherwise copy the file contents of the game to load into lastGameWrite before running the program
- Run the game and select the proper option

## Example

Below is an example game playthrough demonstrating usage of the bot.

### Game Details

The demo below is a 4-player game played in normal mode.
The players are: 
- Bot (Teal)
- Jake (Orange)
- Amy (Purple)
- Charles (Red)

![Program Runthrough](Demos/program_run.gif)
![Full Board Demo](Demos/board_run.gif)

### Video links:

Below are links to the full demos:
- Program Runthrough: https://youtu.be/A6hNMOmuhkY
- Full Board Demo: https://youtu.be/VR4tR5pf48k
