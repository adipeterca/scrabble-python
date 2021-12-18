from tkinter import *
from functools import partial
import sys
import re

# Gameboard for Scrabble (15x15)
board = [ [None] * 15 for i in range(15)]

# List of available letters for the current turn
letters = []

# Actual letter values
letterValue = {'a' : 1,
               'b' : 3,
               'c' : 3,
               'd' : 2,
               'e' : 1,
               'f' : 4,
               'g' : 2,
               'h' : 4,
               'i' : 1,
               'j' : 8,
               'k' : 5,
               'l' : 1,
               'm' : 3,
               'n' : 1,
               'o' : 1,
               'p' : 3,
               'q' : 10,
               'r' : 1,
               's' : 1,
               't' : 1,
               'u' : 1,
               'v' : 4,
               'w' : 4,
               'x' : 8,
               'y' : 4,
               'z' : 10}

# For use in selecting a letter and placing it on the board
valueSelected = ''

# Current word
# It is a list of dicts: 'letter', 'posI', 'posJ'
currentWord = []

# Words list
acceptedWords = []

# Returns the word value
def getWordValue(i1, j1, i2, j2):

    global letterValue

    doubleWordValue = False
    tripleWordValue = False
    
    value = 0

    # Top-to-bottom words
    if i1 < i2:
        for i in range(i1, i2 + 1):
            lv = letterValue[board[i][j1]['text'].lower()]

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
            lv = letterValue[board[i1][j]['text'].lower()]

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
            print(board[i1][j]['text'].lower())
    
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
    global valueSelected
    # Get the selected value
    valueSelected = letters[buttonIndex]['text']

    # Hide the button
    letters[buttonIndex].grid_forget()

    # Make all other buttons unclickable and make the board clickable
    for i in range(len(letters)):
        letters[i]['state'] = 'disabled'
    
    for i in range(15):
        for j in range(15):
            # Unlock only the free ones
            if board[i][j]['text'] == ' ' and canUnlock(i, j):
                board[i][j]['state'] = 'normal'

    # Should also make the 'apply word' and 'skip turn' buttons disabled
    print(f"Selected value {valueSelected} from button index {buttonIndex}")

# Actually puts the letter on the board
def putLetter(buttonIndexI, buttonIndexJ):
    global valueSelected, currentWord

    board[buttonIndexI][buttonIndexJ]['text'] = valueSelected

    # Store the value selected in the currentWord variable
    currentWord.append({'letter':valueSelected, 'posI': buttonIndexI, 'posJ':buttonIndexJ})

    # After we put the letter, we revert to the original state of buttons
    for i in range(len(letters)):
        letters[i]['state'] = 'normal'
    
    for i in range(15):
        for j in range(15):
            board[i][j]['state'] = 'disabled'
        
    print(f"Applied value {valueSelected} to button[{buttonIndexI}][{buttonIndexJ}]")

# Called when 'Apply word' is clicked
# If the word is correct (alongside all the other words formed), it returns a score
# If the word is not correct, it returns the letters from the game board to the player's board
def checkWord():
    global acceptedWords, info, currentWord

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

    # Check each word on the board with the words from the provided dictionary
    for wordEntry in wordsOnBoard:
        exists = False
        # Get only the word
        s1 = wordEntry[0]
        for s2 in acceptedWords:
            if s1.lower() == s2.lower():
                exists = True
                # print(f"Found word {s2} with score {getWordValue(wordEntry[1], wordEntry[2], wordEntry[3], wordEntry[4])}")
                info['text'] = f"Found word {s2} with score {getWordValue(wordEntry[1], wordEntry[2], wordEntry[3], wordEntry[4])}"
                break

        if not exists:
            # print(f"Word '{s1}' does not exist in the dictionary!")
            info['text'] = f"Word '{s1}' does not exist in the dictionary!"

            # Return all the game pieces to the player's board
            for e, widget in enumerate(letters):
                if not widget.winfo_ismapped():
                    widget.grid(row=0, column=e, padx=10)
            # Remove the pieces from the game board
            for e in range(len(currentWord)):
                board[currentWord[e]['posI']][currentWord[e]['posJ']]['text'] = ' '
            return


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
    player = Label(framePlayer, text="Player 1 board", font=('Arial', 25))
    player.pack()

    # Frame containing the letters
    frameLetters = Frame(root)

    for i in range(7):
        # Create the callback function
        action = partial(selectLetter, i)

        letters.append(Button(frameLetters, text=chr(65 + i), height=2, width=5, font=('Arial', 10), command=action))
        letters[i].grid(row=0, column=i, padx=10)

    # Information box for different messages
    frameInfo = Frame(root, pady=20)
    info = Label(frameInfo, text='Info box', font = ('Arial', 15))
    info.pack()
    
    # Apply word button which checks if the word is good
    applyButton = Button(root, text='Apply word', command=checkWord)
    applyButton.pack()
    
    # Pack everything else
    frameBoard.pack()
    framePlayer.pack()
    frameLetters.pack()
    frameInfo.pack()

    root.mainloop()