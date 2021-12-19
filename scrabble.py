from tkinter import *
from functools import partial
import sys
import re
import random
import os

class Player:
    def __init__(self, name = 0):
        # Set the initial score
        self.score = 0

        # Set the name (usually an index)
        self.name = name

        # List of letters
        self.letters = []
        for i in range(7):
            self.letters.append(getRandomLetter())

# Gameboard for Scrabble (15x15)
board = [ [None] * 15 for i in range(15)]

# The number of turns played
turns = 0

# List of available letter buttons for the current turn
letterButtons = []

# Actual letter values
letterValue = {'A' : 1,
               'B' : 3,
               'C' : 3,
               'D' : 2,
               'E' : 1,
               'F' : 4,
               'G' : 2,
               'H' : 4,
               'I' : 1,
               'J' : 8,
               'K' : 5,
               'L' : 1,
               'M' : 3,
               'N' : 1,
               'O' : 1,
               'P' : 3,
               'Q' : 10,
               'R' : 1,
               'S' : 1,
               'T' : 1,
               'U' : 1,
               'V' : 4,
               'W' : 4,
               'X' : 8,
               'Y' : 4,
               'Z' : 10}

# For use in selecting a letter and placing it on the board
valueSelected = ''

# Initial bag
bag = ['A'] * 9 + \
      ['B'] * 2 + \
      ['C'] * 2 + \
      ['D'] * 4 + \
      ['E'] * 12 + \
      ['F'] * 2 + \
      ['G'] * 3 + \
      ['H'] * 2 + \
      ['I'] * 9 + \
      ['J'] * 1 + \
      ['K'] * 1 + \
      ['L'] * 4 + \
      ['M'] * 2 + \
      ['N'] * 6 + \
      ['O'] * 8 + \
      ['P'] * 2 + \
      ['Q'] * 1 + \
      ['R'] * 6 + \
      ['S'] * 4 + \
      ['T'] * 6 + \
      ['U'] * 4 + \
      ['V'] * 2 + \
      ['W'] * 2 + \
      ['X'] * 1 + \
      ['Y'] * 2 + \
      ['Z'] * 1

# Current word
# It is a list of dicts: 'letter', 'posI', 'posJ'
currentWord = []

# Words list
acceptedWords = []

# Used in calculating the current score of the words formed
previousScore = 0

# Returns the word value
def getWordValue(i1, j1, i2, j2):

    global letterValue

    doubleWordValue = False
    tripleWordValue = False
    
    value = 0

    # Top-to-bottom words
    if i1 < i2:
        for i in range(i1, i2 + 1):
            lv = letterValue[board[i][j1]['text'].upper()]

            # Double the letter's value?
            if board[i][j1]['bg'] == '#5e79ff':
                lv = 2 * lv
            
            # Triple the letter's value?
            if board[i][j1]['bg'] == '#1130cf':
                lv = 3 * lv

            # Double the word's value?
            if board[i][j1]['bg'] == '#ff4fc4':
                doubleWordValue = True
            
            # Triple the word's value?
            if board[i][j1]['bg'] == '#f00c4d':
                tripleWordValue = True
        
            value += lv
    else:
        for j in range(j1, j2 + 1):
            lv = letterValue[board[i1][j]['text'].upper()]

            # Double the letter's value?
            if board[i1][j]['bg'] == '#5e79ff':
                lv = 2 * lv
            
            # Triple the letter's value?
            if board[i1][j]['bg'] == '#1130cf':
                lv = 3 * lv

            # Double the word's value?
            if board[i1][j]['bg'] == '#ff4fc4':
                doubleWordValue = True
            
            # Triple the word's value?
            if board[i1][j]['bg'] == '#f00c4d':
                tripleWordValue = True
        
            value += lv
            print(lv)
            print(board[i1][j]['text'].upper())
    
    if doubleWordValue:
        return 2 * value
    if tripleWordValue:
        return 3 * value
    return value

# Color corrections
#   Light red : double word value #ff4fc4
#   Dark red : triple word value #f00c4d
#   Light blue : double letter value #5e79ff
#   Dark blue : triple letter value #1130cf
def colorCorrections(board):
    board[0][0]['bg'] = '#f00c4d'
    board[0][7]['bg'] = '#f00c4d'
    board[0][14]['bg'] = '#f00c4d'
    board[7][0]['bg'] = '#f00c4d'
    board[7][14]['bg'] = '#f00c4d'
    board[14][0]['bg'] = '#f00c4d'
    board[14][7]['bg'] = '#f00c4d'
    board[14][14]['bg'] = '#f00c4d'

    board[1][1]['bg'] = '#ff4fc4'
    board[1][13]['bg'] = '#ff4fc4'
    board[2][2]['bg'] = '#ff4fc4'
    board[2][12]['bg'] = '#ff4fc4'
    board[3][3]['bg'] = '#ff4fc4'
    board[3][11]['bg'] = '#ff4fc4'
    board[4][4]['bg'] = '#ff4fc4'
    board[4][10]['bg'] = '#ff4fc4'
    board[7][7]['bg'] = '#ff4fc4'
    board[10][4]['bg'] = '#ff4fc4'
    board[10][10]['bg'] = '#ff4fc4'
    board[11][3]['bg'] = '#ff4fc4'
    board[11][11]['bg'] = '#ff4fc4'
    board[12][2]['bg'] = '#ff4fc4'
    board[12][12]['bg'] = '#ff4fc4'
    board[13][1]['bg'] = '#ff4fc4'
    board[13][13]['bg'] = '#ff4fc4'
    
    board[1][5]['bg'] = '#1130cf'
    board[1][9]['bg'] = '#1130cf'
    board[5][1]['bg'] = '#1130cf'
    board[5][5]['bg'] = '#1130cf'
    board[5][9]['bg'] = '#1130cf'
    board[5][13]['bg'] = '#1130cf'
    board[9][1]['bg'] = '#1130cf'
    board[9][5]['bg'] = '#1130cf'
    board[9][9]['bg'] = '#1130cf'
    board[9][13]['bg'] = '#1130cf'
    board[13][5]['bg'] = '#1130cf'
    board[13][9]['bg'] = '#1130cf'

    board[0][3]['bg'] = '#5e79ff'
    board[0][11]['bg'] = '#5e79ff'
    board[2][6]['bg'] = '#5e79ff'
    board[2][8]['bg'] = '#5e79ff'
    board[3][0]['bg'] = '#5e79ff'
    board[3][7]['bg'] = '#5e79ff'
    board[3][14]['bg'] = '#5e79ff'
    board[6][2]['bg'] = '#5e79ff'
    board[6][6]['bg'] = '#5e79ff'
    board[6][8]['bg'] = '#5e79ff'
    board[6][12]['bg'] = '#5e79ff'
    board[7][3]['bg'] = '#5e79ff'
    board[7][11]['bg'] = '#5e79ff'
    board[8][2]['bg'] = '#5e79ff'
    board[8][6]['bg'] = '#5e79ff'
    board[8][8]['bg'] = '#5e79ff'
    board[8][12]['bg'] = '#5e79ff'
    board[11][0]['bg'] = '#5e79ff'
    board[11][7]['bg'] = '#5e79ff'
    board[11][14]['bg'] = '#5e79ff'
    board[12][6]['bg'] = '#5e79ff'
    board[12][8]['bg'] = '#5e79ff'
    board[0][3]['bg'] = '#5e79ff'
    board[14][3]['bg'] = '#5e79ff'
    board[14][11]['bg'] = '#5e79ff'

# Unlocks only the buttons on the board that represent a right placement for the next letter (top-down or right-left)
def canUnlock(i, j):
    global currentWord

    size = len(currentWord)

    # If no letter was written, it can be placed anywhere
    if size == 0:
        return True

    # If only a letter was placed, it can be either top-bottom or right-left
    if size == 1:
        return currentWord[0]['posI'] == i and currentWord[0]['posJ'] + 1 == j or currentWord[0]['posI'] + 1 == i and currentWord[0]['posJ'] == j

    # Top-down
    if currentWord[size - 1]['posJ'] == currentWord[size - 2]['posJ']:
        return currentWord[size - 1]['posJ'] == j and currentWord[size - 1]['posI'] + 1 == i
    # Right-left
    return currentWord[size - 1]['posI'] == i and currentWord[size - 1]['posJ'] + 1 == j

# Select a letter from the available ones
def selectLetter(buttonIndex):
    global valueSelected, applyButton, randomButton, skipButton, letterSelectionStarted
    # Get the selected value
    valueSelected = letterButtons[buttonIndex]['text']

    # Hide the button
    letterButtons[buttonIndex].grid_forget()

    # Make all other buttons unclickable and make the board clickable
    for i in range(len(letterButtons)):
        letterButtons[i]['state'] = 'disabled'
    
    # Disable Apply/Random/Skip buttons
    applyButton['state'] = 'disabled'
    randomButton['state'] = 'disabled'
    skipButton['state'] = 'disabled'
    
    for i in range(15):
        for j in range(15):
            # Unlock only the free ones
            if board[i][j]['text'] == ' ' and canUnlock(i, j):
                board[i][j]['state'] = 'normal'

    print(f"Selected value {valueSelected} from button index {buttonIndex}")

# Actually puts the letter on the board
def putLetter(buttonIndexI, buttonIndexJ):
    global valueSelected, currentWord, applyButton

    board[buttonIndexI][buttonIndexJ]['text'] = valueSelected

    # Store the value selected in the currentWord variable
    currentWord.append({'letter':valueSelected, 'posI': buttonIndexI, 'posJ':buttonIndexJ})

    # After we put the letter, we revert to the original state of buttons
    for i in range(len(letterButtons)):
        letterButtons[i]['state'] = 'normal'
    
    # Apply word set to normal, Random/Skip buttons still disabled
    applyButton['state'] = 'normal'
    
    for i in range(15):
        for j in range(15):
            board[i][j]['state'] = 'disabled'
        
    print(f"Applied value {valueSelected} to button[{buttonIndexI}][{buttonIndexJ}]")

# Called when 'Apply word' is clicked
# If the word is correct (alongside all the other words formed), it returns a score
# If the word is not correct, it returns the letters from the game board to the player's board
def checkWord():
    global acceptedWords, infoLabel, currentWord, randomButton, skipButton, previousScore, turns

    # Enable Random/Skip buttons
    randomButton['state'] = 'normal'
    skipButton['state'] = 'normal'

    # The first word must be at least 2 letters in length
    if turns == 0 and len(currentWord) < 2:
        infoLabel['text'] = 'First word must be at least 2 letters in length!'

        # Return all the game pieces to the player's board
        for e, widget in enumerate(letterButtons):
            if not widget.winfo_ismapped():
                widget.grid(row=0, column=e, padx=10)
        # Remove the pieces from the game board
        for e in range(len(currentWord)):
            board[currentWord[e]['posI']][currentWord[e]['posJ']]['text'] = ' '
        
        # Clear the current word variable
        currentWord = []
        return

    # H8 must be covered! (from the first round)
    if board[7][7]['text'] == ' ':
        infoLabel['text'] = 'You must cover H8!'

        # Return all the game pieces to the player's board
        for e, widget in enumerate(letterButtons):
            if not widget.winfo_ismapped():
                widget.grid(row=0, column=e, padx=10)
        # Remove the pieces from the game board
        for e in range(len(currentWord)):
            board[currentWord[e]['posI']][currentWord[e]['posJ']]['text'] = ' '
        
        # Clear the current word variable
        currentWord = []
        return

    # If it is not the first word, it can be at least 1 letter in length
    if len(currentWord) < 1:
        infoLabel['text'] = 'To apply a word it needs to have at least 2 letters!'

        # Return all the game pieces to the player's board
        for e, widget in enumerate(letterButtons):
            if not widget.winfo_ismapped():
                widget.grid(row=0, column=e, padx=10)
        # Remove the pieces from the game board
        for e in range(len(currentWord)):
            board[currentWord[e]['posI']][currentWord[e]['posJ']]['text'] = ' '
        
        # Clear the current word variable
        currentWord = []
        return

    # All words except the first one MUST be adjucent
    if turns > 0:
        hasWordNextToIt = False

        # Special case: 1 letter words
        if len(currentWord) == 1:
            i = currentWord[0]['posI']
            j = currentWord[0]['posJ']
            if i - 1 >= 0 and board[i - 1][j]['text'] != ' ' or \
                i + 1 <= 14 and board[i + 1][j]['text'] != ' ' or \
                j - 1 >= 0 and board[i][j - 1]['text'] != ' ' or \
                j + 1 <= 14 and board[i][j + 1]['text'] != ' ':
                hasWordNextToIt = True
        else:
            # Get word direction
            if currentWord[0]['posI'] == currentWord[1]['posI']: # Right to left word

                # Has letter at the beginning or at the end?
                #
                # For example, let's consider word X X X X
                # Does it have A X X X X B ? 

                lastIdx = len(currentWord) - 1
                if currentWord[0]['posJ'] - 1 >= 0 and board[currentWord[0]['posI']][currentWord[0]['posJ'] - 1] != ' ' or \
                    currentWord[lastIdx]['posJ'] + 1 <= 14 and board[currentWord[lastIdx]['posI']][currentWord[lastIdx]['posJ'] + 1] != ' ':
                    hasWordNextToIt = True
                
                # Does the word have something like this (letters above/below):
                # A - B - -
                # X X X X X
                # - C - D -
                else:
                    ii = currentWord[0]['posI']
                    for k in range(currentWord[0]['posJ'], len(currentWord) + currentWord[0]['posJ']):
                        if ii - 1 >= 0 and board[ii - 1][k] != ' ' or \
                            ii + 1 <= 14 and board[ii + 1][k] != ' ':
                            hasWordNextToIt = True
                            break
            else: # Top to bottom
                
                # Has letter at the beginning or at the end?
                #
                # For example, let's consider word X X X X
                # - A -
                # - X -
                # - X -
                # - X -
                # - X -
                # - B -
                # Does it have something like this?
                
                lastIdx = len(currentWord) - 1
                if currentWord[0]['posI'] - 1 >= 0 and board[currentWord[0]['posI'] - 1][currentWord[0]['posJ']] != ' ' or \
                    currentWord[lastIdx]['posI'] + 1 <= 14 and board[currentWord[lastIdx]['posI'] + 1][currentWord[lastIdx]['posJ']] != ' ':
                    hasWordNextToIt = True
                else:
                    # Or does it have something like this?
                    # - X -
                    # - X B
                    # D X C
                    # - X A
                    jj = currentWord[0]['posJ']
                    for k in range(currentWord[0]['posI'], len(currentWord) + currentWord[0]['posI']):
                        if jj - 1 >= 0 and board[k][jj - 1] != ' ' or \
                            jj + 1 <= 14 and board[k][jj + 1] != ' ':
                            hasWordNextToIt = True
                            break


        # Cannot be a single word (not surrounded by at least one other word)
        if not hasWordNextToIt:
            infoLabel['text'] = 'Words must be adjucent to each other'

            # Return all the game pieces to the player's board
            for e, widget in enumerate(letterButtons):
                if not widget.winfo_ismapped():
                    widget.grid(row=0, column=e, padx=10)
            # Remove the pieces from the game board
            for e in range(len(currentWord)):
                board[currentWord[e]['posI']][currentWord[e]['posJ']]['text'] = ' '
            
            # Clear the current word variable
            currentWord = []
            return
    
    # Get a list of all words from the gameboard
    wordsOnBoard = []

    startI = startJ = endI = endJ = 0

    # Get words written left-to-right
    for i in range(15):
        # Check each line for words
        word = ''
        for j in range(15):
            if board[i][j]['text'] != ' ':
                # If it is a blank word (not formed yet)
                if word == '':
                    startI = i
                    startJ = j
                word += board[i][j]['text']
                endI = i
                endJ = j
            else:
                if word != '' and len(word) >= 2:
                    wordsOnBoard.append((word, startI, startJ, endI, endJ))
                    word = ''

    # Get words written top-to-bottom
    for j in range(15):
        word = ''
        for i in range(15):
            if board[i][j]['text'] != ' ':
                # If it is a blank word (not formed yet)
                if word == '':
                    startI = i
                    startJ = j
                word += board[i][j]['text']
                endI = i
                endJ = j
            else:
                if word != '' and len(word) >= 2:
                    wordsOnBoard.append((word, startI, startJ, endI, endJ))
                    word = ''

    currentScore = 0

    # Check each word on the board with the words from the provided dictionary
    for wordEntry in wordsOnBoard:
        exists = False
        # Get only the word
        s1 = wordEntry[0]
        for s2 in acceptedWords:
            if s1.upper() == s2.upper():
                exists = True
                # print(f"Found word {s2} with score {getWordValue(wordEntry[1], wordEntry[2], wordEntry[3], wordEntry[4])}")
                _s = getWordValue(wordEntry[1], wordEntry[2], wordEntry[3], wordEntry[4])
                infoLabel['text'] = f"Found word {s2} with score {_s}"
                currentScore += _s
                break

        if not exists:
            # print(f"Word '{s1}' does not exist in the dictionary!")
            infoLabel['text'] = f"Word '{s1}' does not exist in the dictionary!"

            # Return all the game pieces to the player's board
            for e, widget in enumerate(letterButtons):
                if not widget.winfo_ismapped():
                    widget.grid(row=0, column=e, padx=10)
            # Remove the pieces from the game board
            for e in range(len(currentWord)):
                board[currentWord[e]['posI']][currentWord[e]['posJ']]['text'] = ' '
            
            # Clear the current word variable
            currentWord = []
            return
    
    # Clear the current word variable
    currentWord = []

    # If the word was correct, end the turn
    endTurn(currentScore - previousScore)
    previousScore = currentScore

# Displays the board and other info associated with the selected player
def displayPlayer(playerIndex):
    pass
    # Display player's name

    # Display player's board

# Updates the board of the current player if at least 7 letters remain in the bag
# Else it does nothing
def getRandomBoard():
    global bag, players, currentPlayerIndex
    
    if len(bag) < 7:
        return
    # Shuffle the bag first
    random.shuffle(bag)

    # Pop 7 elements from it
    letters = []
    for i in range(7):
        letters.append(bag.pop())
    
    # Add the current player's letters to the bag
    bag += players[currentPlayerIndex].letters

    # Update the player's letters
    players[currentPlayerIndex].letters = letters

    # Fact: the letters won't show right away, because if you choose to randomize them, it ends your turn so they won't be displayed.

    endTurn()

# Returns a random letter from the bag
def getRandomLetter():
    global bag

    if len(bag) == 0:
        return None

    random.shuffle(bag)
    return bag.pop()

# Ends the current turn and updates the GUI for the next player (playerLabel, letterButtons and infoLabel)
def endTurn(score = 0):
    global currentPlayerIndex, letterButtons, turns

    print(f"Player {currentPlayerIndex} ended his turn!")
    print(f"Ended turn {turns}!")
    turns += 1
    print(f"Started turn {turns}!")
    
    # Save the current board for the current player
    # First, make sure there are 7 letters on the board
    while len(players[currentPlayerIndex].letters) < 7:
        if len(bag) != 0:
            players[currentPlayerIndex].letters.append(getRandomLetter())
            print(f"Added letter {players[currentPlayerIndex].letters[-1]} to the list!")
        else:
            print(f"No more letters in bag for player {currentPlayerIndex}!")
            break

    # Save the score
    players[currentPlayerIndex].score += score
    print(f"Player {currentPlayerIndex} got score {score} for this round!")

    # Display the next player
    currentPlayerIndex = (currentPlayerIndex + 1) % len(players)

    # Display the label
    playerLabel['text'] = f"Player {currentPlayerIndex} board"

    # Display the letters
    for i in range(7):
        # Update the letters
        letterButtons[i]['text'] = players[currentPlayerIndex].letters[i]

        # Make all of them visible
        if not letterButtons[i].winfo_ismapped():
            letterButtons[i].grid(row=0, column=i, padx=10)

    # Info label
    infoLabel['text'] = f'Info label for player {currentPlayerIndex}'

if __name__ == "__main__":

    # Check command line
    if len(sys.argv) != 2:
        print(f"USAGE: python3 scrabble.py dict.txt")
        exit(0)

    # Parse the dictionary specified as parameter
    with open(sys.argv[1], "r") as fin:
        acceptedWords = [s[:-1] if s[-1:] == '\n' else s for s in fin.readlines()]
        reg = re.compile(r'^[a-z]+$')
        for s in acceptedWords:
            if not reg.match(s):
                print(f"Word '{s}' from dict is not a word!")
                exit(0)
    
    print("Dictionary:")
    print(acceptedWords)

    # Create the players
    players = [Player(0), Player(1)]
    currentPlayerIndex = 0

    # Draw the main window
    root = Tk()
    root.title('Scrabble')
    root.geometry('1800x1000')

    # GUI for board
    frameBoard = Frame(root, pady=10)

    # Fill the board with default values
    for i in range(15):
        for j in range(15):
            # Create the callback function
            action = partial(putLetter, i, j)

            # Create the backend 2D array
            board[i][j] = Button(frameBoard, text=' ', height=2, width=5, font=('Arial', 10), bg='#54fa9b', command=action)
            board[i][j].grid(row=i, column=j)

            # At first, all buttons from the board are disabled
            board[i][j]['state'] = 'disabled'

    colorCorrections(board)

    # Frame displaying the current player
    framePlayer = Frame(root, pady=20)
    playerLabel = Label(framePlayer, text="Player 0 board", font=('Arial', 25))
    playerLabel.pack()

    # Frame containing the letters
    frameLetters = Frame(root)

    for i in range(7):
        # Create the callback function
        action = partial(selectLetter, i)

        letterButtons.append(Button(frameLetters, height=2, width=5, font=('Arial', 10), command=action))
        letterButtons[i]['text'] = players[currentPlayerIndex].letters[i]
        letterButtons[i].grid(row=0, column=i, padx=10)

    # Information box for different messages
    frameInfo = Frame(root, pady=20)
    infoLabel = Label(frameInfo, text='Info box', font = ('Arial', 15))
    infoLabel.pack()
    
    # Buttons frame
    frameButtons = Frame(root)

    # Apply word button which checks if the word is good
    applyButton = Button(frameButtons, text='Apply word', command=checkWord)
    applyButton.grid(row=0, column=0, padx=10)

    # Random button - selects 7 others letters from the bag and puts the 7 current ones bag
    randomButton = Button(frameButtons, text='Random', command=getRandomBoard)
    randomButton.grid(row=0, column=1, padx=10)

    # Skip turn button - skips the current turn, scoring nothing
    skipButton = Button(frameButtons, text='Skip', command=endTurn)
    skipButton.grid(row=0, column=2, padx=10)
    
    # Pack everything else
    frameButtons.pack()
    frameBoard.pack()
    framePlayer.pack()
    frameLetters.pack()
    frameInfo.pack()

    # Print scores on exit
    def endGame():
        os.system("cls")
        for i in range(len(players)):
            print(f"Player {i} scored {players[i].score}!")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", endGame)
    root.mainloop()

# Left TODO
# 1. sa poti adauga cuvinte doar daca sunt adiacente cu cele deja existente (aproape facut, trebuie testat bine)
# 2. sa poti pune o litera pentru un cuvant DUPA una deja existenta (de ex, daca scrii [- - - A B c - -] si urmeaza sa pui D, sa o poti face (c deja exista))
# 3. testare foarte detaliata, in rest totul e facut