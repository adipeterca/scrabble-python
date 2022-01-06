# scrabble-python

Python implementation with GUI for Scrabble

## What is Scrabble?
Scrabble is a multiplayer board game in which players must make words on a 15x15 board of boxes. Each word is formed by placing letters on the game board, either from top-down or left-right. The goal is to accumulate as many points as possible!

## How to play?  
First, create a **dictionary** of words (or make one using the provided *dictMaker.py* script) or select one from the available ones. Then, run the script using the command **python3 scrabble.py dict.txt** and the game will start!

## What rules are there?
The main rules are as follows:
1. The first move **must** cover the central box (where the diagonals meet)
2. A move is valid iff:
	- all words formed exist in the provided dictionary (even the not-intended-to-be-created ones!)
	- all words are connected (no "island" words)
	- a move can be skipped (with 0 score)
	- a move can randomize the whole current player's rack (with 0 score)
	- all letters placed on a move must be for the same word (you cannot create 2 different words on the same turn!)
3. The game ends iff:
	- one player has no more letters on the rack
	- one player decides to end the game

### References:

https://en.wikipedia.org/wiki/Scrabble

https://ro.wikipedia.org/wiki/Scrabble

https://en.wikipedia.org/wiki/Scrabble_letter_distributions