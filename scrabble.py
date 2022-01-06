import sys
import re
import random
import os
from tkinter import *
from functools import partial

class Player:
    """
    The Player class is the default structure used for keeping information
    strictly related to a player (like score, name, rack etc.) in one place.
    """
    def __init__(self, name="scrabble"):
        """
        Constructor function.
        Takes a string as name (default is "scrabble") to differentiate between objects of this class. 

        :param name: string to be assigned as name (default is "scrabble")
        """
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

def getWordValue(i1, j1, i2, j2):
    """
    Function for returning a word value.
    
    :param i1: position on the X axis for the first letter of the word
    :param j1: position on the Y axis for the first letter of the word
    :param i2: position on the X axis for the last letter of the word
    :param j2: position on the Y axis for the last letter of the word
    :return: the value of the word if it is correct, 0 otherwise
    """
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
            # print(lv)
            # print(board[i1][j]['text'].upper())
    
    if doubleWordValue:
        return 2 * value
    if tripleWordValue:
        return 3 * value
    return value

def colorCorrections():
    """
    Internal function used for coloring the game board.
    """
    global board
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

def canUnlock(i, j):
    """
    Unlocks only the buttons on the board that represent a right placement for the next letter (top-down or right-left).

    :param i: the position on the X axis for the button that is checked
    :param j: the position on the Y axis for the button that is checked
    :return: True if it can be placed, False otherwise
    """

    global currentWord

    size = len(currentWord)

    # If no letter was written, it can be placed anywhere
    if size == 0:
        return True

    if size == 1:
        ii = currentWord[0]['posI']
        jj = currentWord[0]['posJ']

        # Left to right
        if ii == i:
            # Return True only if there are no empty spaces from the last placed letter of the word to the current position
            for _ in range(jj, j):
                if board[ii][_]['text'] == ' ':
                    return False
            
            return True
        
        # Top to bottom
        if jj == j:
            for _ in range(ii, i):
                if board[_][jj]['text'] == ' ':
                    return False
            return True
        return False
    
    # Last added letter
    ii = currentWord[size - 1]['posI']
    jj = currentWord[size - 1]['posJ']

    # First added letter
    iii = currentWord[0]['posI']
    jjj = currentWord[0]['posJ']

    # Left to right
    if ii == i and iii == i:
        # Return True only if there are no empty spaces from the last placed letter of the word to the current position
        for _ in range(jj, j):
            if board[ii][_]['text'] == ' ':
                return False
        
        return True
    
    # Top to bottom
    if jj == j and jjj == j:
        for _ in range(ii, i):
            if board[_][jj]['text'] == ' ':
                return False
        return True
    return False

def selectLetter(buttonIndex):
    """
    Callback function for the rack buttons.

    It's called when a letter is selected.
    :param buttonIndex: the index for which button in the rack was pressed
    """
    global valueSelected, applyButton, randomButton, skipButton, players, currentPlayerIndex
    # Get the selected value
    valueSelected = letterButtons[buttonIndex]['text']
    # valueSelected = players[currentPlayerIndex].letters[buttonIndex]

    # Hide the button
    letterButtons[buttonIndex].grid_forget()
    
    # Delete the letter
    players[currentPlayerIndex].letters[buttonIndex] = ''

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

    # print(f"Selected value {valueSelected} from button index {buttonIndex}")

def putLetter(buttonIndexI, buttonIndexJ):
    """
    Internal function for updating a value on the board.

    It's called after a letter was selected from the rack and a button on the board was pressed.
    :param buttonIndexI: index of the button on the X axis
    :param buttonIndexJ: index of the button on the Y axis
    """
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
        
    # print(f"Applied value {valueSelected} to button[{buttonIndexI}][{buttonIndexJ}]")

def checkWord():
    """
    Callbacak function for when 'Apply word' is clicked.

    :return: if the word is correct (alongside all the other words formed), it returns a score,
                otherwise returns the letters to the rack.
    """
    global acceptedWords, infoLabel, currentWord, randomButton, skipButton, previousScore, turns

    # Enable Random/Skip buttons
    randomButton['state'] = 'normal'
    skipButton['state'] = 'normal'

    def returnGameBoard():
        global currentWord

        # Return all the game pieces to the player's board
        for e, widget in enumerate(letterButtons):
            if not widget.winfo_ismapped():
                widget.grid(row=0, column=e, padx=10)
            
            # Remake the original letter list
            players[currentPlayerIndex].letters[e] = letterButtons[e]['text']

        
            
        # Remove the pieces from the game board
        for e in range(len(currentWord)):
            board[currentWord[e]['posI']][currentWord[e]['posJ']]['text'] = ' '
        
        # Clear the current word variable
        currentWord = []

    # The first word must be at least 2 letters in length
    if turns == 0 and len(currentWord) < 2:
        infoLabel['text'] = 'First word must be at least 2 letters in length!'
        returnGameBoard()
        return

    # H8 must be covered! (from the first round)
    if board[7][7]['text'] == ' ':
        infoLabel['text'] = 'You must cover the central square!'
        returnGameBoard()
        return

    # If it is not the first word, it can be at least 1 letter in length
    if len(currentWord) < 1:
        infoLabel['text'] = 'To apply a word it needs to have at least 2 letters!'
        returnGameBoard()
        return

    # All words except the first one MUST be adjucent
    if turns > 0:
        hasWordNextToIt = False

        # A list representing the letters of the current word by a simple (i, j) tuple
        currentLetterPositions = []

        # Get current letters
        for i in range(len(currentWord)):
            posI = currentWord[i]['posI']
            posJ = currentWord[i]['posJ']
            currentLetterPositions.append((posI, posJ))
 
        # For each letter of the word, test if it has another adjucent letter that IS NOT in the current letters list
        for k in range(len(currentWord)):
            
            i = currentWord[k]['posI']
            j = currentWord[k]['posJ']

            # Test up
            if i > 0 and (i - 1, j) not in currentLetterPositions and board[i - 1][j]['text'] != ' ':
                hasWordNextToIt = True
            
            # Test down
            if i < 14 and (i + 1, j) not in currentLetterPositions and board[i + 1][j]['text'] != ' ':
                hasWordNextToIt = True
            
            # Test left
            if j > 0 and (i, j - 1) not in currentLetterPositions and board[i][j - 1]['text'] != ' ':
                hasWordNextToIt = True
            
            # Test right
            if j < 14 and (i, j + 1) not in currentLetterPositions and board[i][j + 1]['text'] != ' ':
                hasWordNextToIt = True

        # Cannot be a single word (not surrounded by at least one other word)
        if not hasWordNextToIt:
            infoLabel['text'] = 'Words must be adjucent to each other'
            returnGameBoard()
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
                if len(word) >= 2:
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
                if len(word) >= 2:
                    wordsOnBoard.append((word, startI, startJ, endI, endJ))
                word = ''

    currentScore = 0

    print(f"[DEBUG] Words on board: {wordsOnBoard}")

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
            returnGameBoard()
            return
    
    # Clear the current word variable
    currentWord = []

    # If the word was correct, end the turn
    endTurn(currentScore - previousScore)
    previousScore = currentScore

def getRandomBoard():
    """
    Callback function for the "Random" button.

    Updates the board of the current player if at least 7 letters remain in the bag, otherwise returns nothing.
    """
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

def getRandomLetter():
    """
    Returns a random letter from the bag.

    :return: a random letter iff there are any left in the bag, None otherwise
    """
    global bag

    if len(bag) == 0:
        return None

    random.shuffle(bag)
    return bag.pop()

def endTurn(score = 0):
    """
    Function called by all buttons after they finished their specific callbacks.

    Ends the current turn and updates the GUI for the next player (playerLabel, letterButtons and infoLabel).
    """
    global currentPlayerIndex, letterButtons, turns

    print(f"[DEBUG] Player {players[currentPlayerIndex].name} ended his turn!")
    print(f"[DEBUG] Ended turn {turns}!")

    # Save the score
    players[currentPlayerIndex].score += score

    # Save the current board for the current player
    # First, remove the used letters (marked as null - '')
    players[currentPlayerIndex].letters = [e for e in players[currentPlayerIndex].letters if e != '']

    # The player played all his letters and the bag is empty - the game ends
    if len(players[currentPlayerIndex].letters) == 0 and len(bag) == 0:
        endGameGUI()
        return

     # Secord, make sure there are 7 letters on the board
    while len(players[currentPlayerIndex].letters) < 7:
        if len(bag) != 0:
            players[currentPlayerIndex].letters.append(getRandomLetter())
            print(f"[DEBUG] Added letter {players[currentPlayerIndex].letters[-1]} to the list!")
        else:
            print(f"[DEBUG] No more letters in bag for player {players[currentPlayerIndex].name}!")
            break

    print(f"[DEBUG] Player {players[currentPlayerIndex].name} got score {score} for this round!")

    turns += 1
    print(f"[DEBUG] Started turn {turns}!")
    

    # Display the next player
    currentPlayerIndex = (currentPlayerIndex + 1) % len(players)

    # Display the label
    playerLabel['text'] = f"Player {players[currentPlayerIndex].name} board"

    # Display the letters
    for i in range(7):
        # Update the letters
        letterButtons[i]['text'] = players[currentPlayerIndex].letters[i]

        # Make all of them visible
        if not letterButtons[i].winfo_ismapped():
            letterButtons[i].grid(row=0, column=i, padx=10)

    # Info label
    # infoLabel['text'] = f'Info label for player {currentPlayerIndex}'
    infoLabel['text'] = f'Current score for Player {players[currentPlayerIndex].name}: {players[currentPlayerIndex].score}'

if __name__ == "__main__":

    # Check command line
    if len(sys.argv) != 2:
        print(f"[FAIL] USAGE: python3 scrabble.py dict.txt")
        exit(0)

    # Parse the dictionary specified as parameter
    with open(sys.argv[1], "r") as fin:
        acceptedWords = [s[:-1] if s[-1:] == '\n' else s for s in fin.readlines()]
        reg = re.compile(r'^[a-z]+$')
        for s in acceptedWords:
            if not reg.match(s):
                print(f"[WARNING] Word '{s}' from dict is not a word!")
                exit(0)
    
    # print("Dictionary:")
    # print(acceptedWords)

    # Get number of players
    while True:
        try:
            s = input("Number of players (2, 3 or 4): ")
            numberOfPlayers = int(s)
            if numberOfPlayers in [2, 3, 4]:
                print(f"Selected {numberOfPlayers} players! The game will begin shortly...")
                break
            else:
                raise Exception   
        except:
            print(f"Invalid input '{s}'. Try again!")

    # Create the players
    players = []
    alreadyChosen = ["scrabble"]
    for i in range(numberOfPlayers):
        
        # Execute until a name that is not used was given
        while True:
            name = input(f"Name for player {i + 1}: ")
            if name not in alreadyChosen:
                break
            print(f"Name {name} already exists!")

        # Append the chosen name
        alreadyChosen.append(name)

        # Create the player
        if name != "":
            players.append(Player(name))
        else:
            players.append(Player())
    
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

    colorCorrections()

    # Frame displaying the current player
    framePlayer = Frame(root, pady=20)
    playerLabel = Label(framePlayer, text=f"Player {players[0].name} board", font=('Arial', 25))
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
    infoLabel = Label(frameInfo, text=f'Current score for Player {players[0].name}: 0', font=('Arial', 15))
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
            print(f"[INFO] Player {players[i].name} scored {players[i].score}!")
        root.destroy()

    def endGameGUI():
        root.destroy()

        endWindow = Tk()
        endWindow.title("Game ended!")
        endWindow.geometry("300x300")

        playerLabels = []
        winner = 0
        for i in range(len(players)):
            playerLabels.append(Label(endWindow, text=f"Player {players[i].name} has a score of {players[i].score}!", font=('Arial', 13), pady=5))

            # Get the winner
            if players[winner].score < players[i].score:
                winner = i

        Label(endWindow, text=f"Hurray! Player {players[winner].name} won!", font=("Arial", 15), pady=40).pack()
        for _ in playerLabels:
            _.pack()
        
    root.protocol("WM_DELETE_WINDOW", endGameGUI)
    root.mainloop()