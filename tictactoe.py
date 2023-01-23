from random import randrange # imports random so it can be used by the computer to choose a cell
import time
import os

def display_board(board): # The function accepts one parameter containing the board's current status and prints it out to the console
    print("+-------" * 3 + "+", sep="") # prints the top line
    for row in range(3): # for 3 iterations, the program will...
        print("|       " * 3, "|", sep="") # print seperators that appear above and below each number
        for col in range(3): # for 3 * 3 iterations, the program will...
            print("|   " + str(board[row][col]) + "   ", end="") # print rows with a number in them
        print("|") # print last wall at end of previous row
        print("|       " * 3, "|", sep="") # print last row before end
        print("+-------" * 3, "+", sep="") # print end row/wall

def enterMove(board): # function that asks the user to enter a move
    global userInput # sets the userInput variable to global so it can be used across functions 
    valid = False # makes the input invalid so the while loop can start

    while not valid: # 'invalid' input starts the while loop
        userMove = input("Enter your move (1-9):") # asks user to enter a cell no.
        valid = len(userMove) == 1 and userMove >= '1' and userMove <= '9' # checks the input was between or equal to 1 and 9

        if not valid: # runs if input was not between or equal to 1 or 9
            print("Your move was outside the board bounds. Try again.") # tells user to reenter their number
            continue # restarts the while loop

        userInput = int(userMove) # userInput becomes an integer version of the user's input
        userMove = int(userMove) - 1 # changes the user input to integer - 1 so the later division works correctly 
        row = userMove // 3 # row = input divided by 3 then rounded down, e.g. original 6 input - 1 // 3 = 1
        col = userMove % 3 # col = remainder of input divided by 3
        sign = board[row][col] # checks if player sign (O) is in that cell
        valid = sign not in ['O', 'X'] # valid = true if there is no sign in that cell

        if not valid: # runs if there is a sign in the cell
            print("Cell occupied, choose another") # tells user of this problem
            continue # restarts while loop

        board[row][col] = 'O' # otherwise, code continues and places the player O in that cell


def make_list_of_free_fields(board, winningSpaces):
    free = [] # create the free spaces array
    for row in range(3): # for 3 iterations, using the variable row, the program will...
        for col in range(3): # creates 3 rows, 3 columns...
            if board[row][col] in ['X']:
                sign = 'X'
                changeToX = row*3+col+1
                checkBoard(winningSpaces, changeToX, sign)
    for row in range(3):
        for col in range(3):
            if board[row][col] not in ['O', 'X']:
                free.append((row,col))
    return free

def victory_for(board, sign): # check who the winner is 
    if sign == 'X': # if winning sign is X...
        winner = 'computer' # set winner to computer
    elif sign == 'O': # if winning sign is O...
        winner = 'player' # set winner to player

    diag1 = diag2 = True

    for cell in range(3): # for 3 iterations the program will...
        if board[cell][0] == sign and board[cell][1] == sign and board[cell][2] == sign: # check the board rows to see if any have a sign three times in a row
            return winner # declare winner
        if board[0][cell] == sign and board[1][cell] == sign and board[2][cell] == sign: # check the board columns to see if any have a sign three times in a row
            return winner # declare winner
        if board[cell][cell] != sign: # check rows diagonally
            diag1 = False 
        if board[2 - cell][cell] != sign: # check rows diagonally, the opposite side
            diag2 = False
    if diag1 or diag2: # else, if all three do contain one sign...
        return winner # declare the winner
    return None # return None if no winner


def drawMove(board): # draws moves for the computer
    global computerInput 
    valid = False
    
    while not valid:
        if turns > 0:
            computerMove = randrange(9)

            valid = computerMove >= 1 and computerMove <= 9
            if not valid:
                continue

            computerInput = computerMove
            computerMove = computerMove - 1
            row = computerMove // 3
            col = computerMove % 3
            sign = board[row][col]
            valid = sign not in ['O', 'X']
        
            if not valid:
                continue
                    
            board[row][col] = 'X'


def checkBoard(winningSpaces, newNumber, sign):
    for element in winningSpaces:
        for i, cell in enumerate(element):
            if cell == newNumber: 
                element[i] = sign
    return winningSpaces

board = [[3 * j + i + 1 for i in range(3)] for j in range(3)] # creates the game board array
winningSpaces = [[1, 5, 9], [3, 5, 7], [1, 2, 3], [1, 4, 7], [2, 5, 8], [3, 6, 9], [4, 5, 6], [7, 8, 9]] # array of cells that can be used to win when all three contain the same sign

board[1][1] = 'X' # set first 'X' in the middle
freeSpaces = make_list_of_free_fields(board, winningSpaces) # calls the function to make free fields

humanTurn = True # allows the human to go after the first X is placed above
global turns
turns = 4

while len(freeSpaces): # while the freeSpaces array has length above 0...
    os.system('clear') # clears the console so only one game board appears at a time      
    display_board(board) # display the current game board

    if humanTurn: # if it's the human's turn...
        sign = "O" # the current playing sign changes to O
        enterMove(board) # the enterMove function is called, allowing the player to choose their placement
        checkBoard(winningSpaces, userInput, sign) # checkBoard is called, with the necessary properties to check if the player has won
        overallWinner = victory_for(board, 'O') # calls victory_for to check the winning spaces against the current game board
    else: # if it's not the human's turn...
        sign = 'X' 
        print("computer is thinking...") # makes the program tell the computer is 'thinking' 
        time.sleep(1) # artificially makes the program stop for a second so the computer can 'think'
        drawMove(board) # drawMove is called by the computer so it can have its turn
        checkBoard(winningSpaces, computerInput, sign)
        overallWinner = victory_for(board, 'X') # victory_for checks the winning spaces against the current game board
        turns -=1
    if overallWinner != None: # if the game has a winner...
        os.system('clear')
        display_board(board) # show the winning placements
        print(overallWinner, "has won!") # tell the player who won
        break # break the loop
    if overallWinner == None and turns == 0:
        os.system('clear')
        display_board(board)
        print("And the game ends in a tie :(")
        exit()

    humanTurn = not humanTurn # after the player has their go, the humanTurn variable is set to False so the computer can go
    freeSpaces = make_list_of_free_fields(board, winningSpaces)